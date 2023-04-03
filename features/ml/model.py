
import streamlit as st
import torch
from model import load_model

def load_widget_model():
    if not hasattr(st, 'model'):
        torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
        st.model = load_model()