
from PIL import Image
import av
import streamlit as st
from streamlit_webrtc import VideoProcessorBase
from db import AppDatabase
from features.models.batch import BatchInsertDTO, insert_new_batch
from features.models.classification_result import save_class_results_to_db
from image_processor import binary_image_apply_threshold,  convert_nd_img_to_gray, crop_img_section_x, crop_img_section_y, crop_only_contact_sections, image_white_percentage
from model import predict, evaluate
import helper



class ClassificationVideoProcessorMaker:
    saved_records = []
    batch_number = None
    database = None

    def __init__(self, database) -> None:
        self.database = database
        [bt_number] = AppDatabase.run_query_one_no_cache(database,"SELECT COUNT(*) FROM Batch")
        btch_number = bt_number + 1
        self.batch_number = btch_number


    def make(self):
        VideoProcessor.batch_number = self.batch_number
        VideoProcessor.database = self.database
        return VideoProcessor


class VideoProcessor(VideoProcessorBase):
    saved_records = {}
    batch_number = None
    end_callback = None
    database = None

    item_counter = 0
    item_visible = False

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:

        display_img = frame.to_ndarray(format='bgr24')[:, ::-1, :]

        gray_img = convert_nd_img_to_gray(display_img)

        _, img_bw = binary_image_apply_threshold(gray_img, st.threshold)

        contact_orientation = st.contact_orientation

        first_part_white_percent = None
        second_part_white_percent = None
        if (contact_orientation == 'Vertical'):
            first_part_white_percent = image_white_percentage(
                crop_img_section_y(Image.fromarray(img_bw), 0.1, 'top'))

            second_part_white_percent = image_white_percentage(
                crop_img_section_y(Image.fromarray(img_bw), 0.1, 'bottom'))
        else:
            first_part_white_percent = image_white_percentage(
                crop_img_section_x(Image.fromarray(img_bw), 0.1, 'left'))

            second_part_white_percent = image_white_percentage(
                crop_img_section_x(Image.fromarray(img_bw), 0.1, 'right'))

        if first_part_white_percent > st.white_threshold and second_part_white_percent > st.white_threshold:
            print("Object detected!")

            if st.model_evaluation == True:
                if self.item_visible == False:
                    self.item_counter += 1
                    self.item_visible = True
                    frame_parsed = frame.to_ndarray(format="rgb24")
                    actual_img = Image.fromarray(frame_parsed, mode='RGB')
                    result = predict(st.model, actual_img)
                    eval_result = evaluate(st.model, result, self.batch_number)
                    self.saved_records[self.item_counter] = eval_result.to_dict(
                    )

                    if self.saved_records[self.item_counter] is None:
                        self.saved_records[self.item_counter] = eval_result.to_dict()

        else:
            print("No object detected.")
            self.item_visible = False

        if (st.contact_lines):
            masked_center_img = crop_only_contact_sections(
                img_bw, crop_percent=0.1, orientation=str(st.contact_orientation))

            return av.VideoFrame.from_ndarray(masked_center_img, format="gray")

        if st.binary_segmentation:
            return av.VideoFrame.from_ndarray(img_bw, format="gray")
        return av.VideoFrame.from_ndarray(display_img, format="bgr24")

    def on_ended(self):
        print('====Video End Callback====')
    
        batch_dto = BatchInsertDTO(
            date=helper.get_mysql_timestamp(),
            batch_name=st.batch_name,
            product_model=st.product_model,
            department=st.department,
            total_items=self.item_counter
        )
        insert_new_batch(batch_dto, self.database)

        save_class_results_to_db(self.saved_records, self.database)

        print('item counter: ', self.item_counter)
        print('====ON END====')
