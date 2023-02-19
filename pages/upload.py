import torch
import streamlit as st
from model import load_model
from torchvision import transforms
import io
from matplotlib import pyplot as plt
import numpy as np
from torchvision import transforms as T
import torch.nn.functional as F
from PIL import Image, ImageDraw, ImageFont
import cv2


def load_image():
    uploaded_file = st.file_uploader(label='Pick an image')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        return Image.open(io.BytesIO(image_data))
    else:
        return None


def predict(model, image):
    print(type(image))

    IMAGENET_MEAN = 0.485, 0.456, 0.406
    IMAGENET_STD = 0.229, 0.224, 0.225

    def classify_transforms(size=224):
        return T.Compose([T.ToTensor(), T.Resize(size), T.CenterCrop(size), T.Normalize(IMAGENET_MEAN, IMAGENET_STD)])

    transformations = classify_transforms()
    convert_tensor = transformations(image)
    convert_tensor = convert_tensor.unsqueeze(0)

    output = model(convert_tensor)
    return output


def main():
    model = load_model()
    image = load_image()
    if image is not None:
        result = predict(model, image)
        print(type(result))

        pred = F.softmax(result, dim=1)

        for i, prob in enumerate(pred):
            top5i = prob.argsort(0, descending=True)[:1].tolist()
            test_res = top5i[0]
            model_name = model.names[test_res]
            text_result = f'{prob[test_res]*100:.2f}% {model_name}'
            if model_name == 'NO GOOD':
                st.subheader(f':red[{text_result}]')
            else:
                st.subheader(f':green[{text_result}]')


main()
