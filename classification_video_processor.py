
from PIL import Image
import cv2
import numpy as np
import av
import streamlit as st
from streamlit_webrtc import VideoProcessorBase
from image_processor import binary_image_apply_threshold, convert_frame_to_gray, convert_nd_img_to_gray, crop_img_section, crop_only_contact_sections, image_white_percentage, nd_img_rgb_to_bgr
from model import predict, evaluate
import random
import helper
import json


class ClassificationVideoProcessorMaker:
    saved_records = []
    batch_number = None

    def __init__(self, batch_name) -> None:
        self.batch_number = batch_name

    def make(self):
        VideoProcessor.batch_number = self.batch_number
        return VideoProcessor


class VideoProcessor(VideoProcessorBase):
    saved_records = {}
    batch_number = None
    end_callback = None
    db_enabled = True

    item_counter = 0
    item_visible = False

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:

        display_img = frame.to_ndarray(format='bgr24')[:, ::-1, :]

        gray_img = convert_nd_img_to_gray(display_img)

        _, img_bw = binary_image_apply_threshold(gray_img, st.threshold)

        top_part_white_percent = image_white_percentage(
            crop_img_section(Image.fromarray(img_bw), 0.1, 'top'))

        bottom_part_white_percent = image_white_percentage(
            crop_img_section(Image.fromarray(img_bw), 0.1, 'bottom'))

        if top_part_white_percent > st.white_threshold and bottom_part_white_percent > st.white_threshold:
            print("Object detected!")

            if st.model_evaluation == True:
                if self.item_visible == False:
                    self.item_counter += 1
                    self.item_visible = True
                if self.db_enabled:
                    frame_parsed = frame.to_ndarray(format="rgb24")
                    actual_img = Image.fromarray(frame_parsed, mode='RGB')
                    result = predict(st.model, actual_img)
                    eval_result = evaluate(st.model, result)
                    self.saved_records[self.item_counter] = [eval_result]

                    if self.saved_records[self.item_counter] is None:
                        self.saved_records[self.item_counter] = [eval_result]
                    else:
                        self.saved_records[self.item_counter].append(
                            eval_result)

        else:
            print("No object detected.")
            self.item_visible = False

        if (st.contact_lines):
            masked_center_img = crop_only_contact_sections(
                img_bw, crop_percent=0.1)
                
            return av.VideoFrame.from_ndarray(masked_center_img, format="gray")

        if st.binary_segmentation:
            return av.VideoFrame.from_ndarray(img_bw, format="gray")
        return av.VideoFrame.from_ndarray(display_img, format="bgr24")

    def on_ended(self):
        print('====Video End Callback====')

        if self.db_enabled:
            rand_number = random.randint(100000, 1000000)

            if self.batch_number:
                rand_number = self.batch_number

            json_str = json.dumps(self.saved_records)

            helper.export_to_json(json_str, rand_number)

        print('item counter: ', self.item_counter)
        print('====ON END====')
