import cv2
import streamlit as st
from image_processor import binary_image_apply_threshold, check_image_is_valid, convert_nd_img_to_gray, crop_img_section, crop_only_contact_sections, image_white_percentage, nd_img_rgb_to_bgr
from model import load_model, predict, evaluate
import io
import numpy as np
from PIL import Image
from features.upload.widgets import Widgets as Upload_Widgets
from features.detection.widgets import Widgets as Detection_Widgets

upload_widgets = Upload_Widgets()
detection_widgets = Detection_Widgets()


def main():
    model = load_model()

    threshold = detection_widgets.binary_threshold_slider()
    st.threshold = threshold

    white_threshold = detection_widgets.white_threshold_slider()
    st.white_threshold = white_threshold

    bs, cl = detection_widgets.preview_radio_button()

    image = None
    image_loader = upload_widgets.upload_image_loader()
    if image_loader is not None:
        image_data = image_loader.getvalue()

        image = Image.open(io.BytesIO(image_data))
        bgr_img = nd_img_rgb_to_bgr(np.asarray(image))

        if (bs):
            gray_img = convert_nd_img_to_gray(bgr_img)
            _, img_bw = binary_image_apply_threshold(gray_img, st.threshold)

            st.image(img_bw)

        elif (cl):

            gray_img = convert_nd_img_to_gray(bgr_img)
            _, img_bw = binary_image_apply_threshold(gray_img, st.threshold)

            masked_center_img = crop_only_contact_sections(
                img_bw, crop_percent=0.1)

            top_wp = image_white_percentage(
                crop_img_section(Image.fromarray(img_bw), 0.1, 'top'))
            bot_wp = image_white_percentage(
                crop_img_section(Image.fromarray(img_bw), 0.1, 'bottom'))

            col1, col2 = st.columns(2)

            with col1:
                st.image(masked_center_img)
            with col2:
                st.image(img_bw)

            st.caption(
                f"""
                Top White Percentage: {top_wp}\n
                Bottom White Percentage: {bot_wp}
                """
            )

        else:
            st.image(image)

    if image is not None:

        print('========= Image Validation ==========')
        print(check_image_is_valid(nd_img_rgb_to_bgr(image), 175))

        result = predict(model, image)
        eval_result = evaluate(model, result)
        label = eval_result['label']
        prob_result = eval_result['probability']

        text_result = f'{prob_result*100:.2f}% {label}'
        if label == 'NO GOOD':
            st.subheader(f':red[{text_result}]')
        else:
            st.subheader(f':green[{text_result}]')


main()
