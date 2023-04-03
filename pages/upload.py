import streamlit as st
from image_processor import check_image_is_valid, nd_img_rgb_to_bgr
from model import load_model, predict, evaluate
import io
import numpy as np
from PIL import Image
from features.upload.widgets import Widgets as Upload_Widgets
from features.detection.widgets import Widgets as Detection_Widgets

upload_widgets = Upload_Widgets()
detection_widgets = Detection_Widgets()

def handle_loaded_image():
    image_loader = upload_widgets.upload_image_loader()
    if image_loader is not None:
        image_data = image_loader.getvalue()
        st.image(image_data)
        return Image.open(io.BytesIO(image_data))
    else:
        return None


def main():
    model = load_model()
    
    bs, cl = detection_widgets.preview_radio_button()
    st.binary_segmentation = bs
    st.contact_lines = cl

    image = handle_loaded_image()
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
