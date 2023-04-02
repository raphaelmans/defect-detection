
import streamlit as st


def init_widgets():

    # Setup [batch_number] widget and state
    st.number_input(
        'Insert batch number', format="%d", value=1001, step=1, key='batch_number')
    st.batch_number = st.session_state['batch_number']

    # Setup [threshold] widget and state
    st.slider("Black Binary Threshold",
              value=175, max_value=255, min_value=1, key='threshold')
    st.threshold = st.session_state['threshold']

    # Setup [white_threshold] widget and state
    st.slider(
        "White Percentage Threshold",
        value=5, max_value=100, min_value=1, key='white_threshold')
    st.white_threshold = st.session_state['white_threshold']

    # Setup [binary_segmentation] widget and state
    st.checkbox('Preview Binary Segmentation', key='binary_segmentation')
    st.binary_segmentation = st.session_state['binary_segmentation']

    # Setup [contact_lines] widget and state
    st.checkbox('Preview Contact Lines', key='contact_lines')
    st.contact_lines = st.session_state['contact_lines']

    # Setup [model_evaluation] widget and state
    st.checkbox('Start Evaluation', key='model_evaluation')
    st.model_evaluation = st.session_state['model_evaluation']

    if 'item_batch_count' not in st.session_state:
        st.session_state['item_batch_count'] = 0


def init_session_state():
    if 'item_batch_count' not in st.session_state:
        st.session_state['item_batch_count'] = 0
