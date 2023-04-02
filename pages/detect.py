import streamlit as st
from model import load_model
import torch
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from classification_video_processor import ClassificationVideoProcessorMaker


st.header('Defect Detection')


if 'item_batch_count' not in st.session_state:
    st.session_state['item_batch_count'] = 0

if not hasattr(st, 'classifier'):
    torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
    st.model = load_model()

batch_number = st.number_input(
    'Insert batch number', format="%d", value=1001, step=1)


threshold = st.slider(
    "Black Binary Threshold",
    value=175, max_value=255, min_value=1)


white_percentage_threshold = st.slider(
    "White Percentage Threshold",
    value=5, max_value=100, min_value=1)


preview_binary_segmentation = st.checkbox('Preview Binary Segmentation')
bounding_boxes = st.checkbox('Preview Contact Lines')
start_evaluate = st.checkbox('Start Evaluation')

st.preview_binary_segmentation = preview_binary_segmentation
st.bounding_boxes = bounding_boxes
st.start_evaluate = start_evaluate
st.threshold = threshold
st.white_threshold = white_percentage_threshold

if st.button('Submit'):
    st.write('Batch '+str(batch_number)+' would be recorded')
    st.session_state['item_batch_count'] += 1
else:
    st.write("Submit to record this detection")

webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=ClassificationVideoProcessorMaker(
        batch_number).make(),
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)
