import streamlit as st
from image_processor import check_image_is_valid, nd_img_rgb_to_bgr
from model import load_model, predict, evaluate
import io
import numpy as np
from PIL import Image


def load_image():
    uploaded_file = st.file_uploader(label='Pick an image')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        return Image.open(io.BytesIO(image_data))
    else:
        return None


def main():
    model = load_model()
    image = load_image()
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
