import streamlit as st

class Widgets:
    
    def upload_image_loader(self):
        return st.file_uploader(label='Pick an image')
