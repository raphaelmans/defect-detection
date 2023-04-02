import streamlit as st
from model import load_model
import torch
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from classification_video_processor import ClassificationVideoProcessorMaker
from features.detection.widgets import init_widgets, init_session_state

st.header('Defect Detection')

init_session_state()
init_widgets()

if not hasattr(st, 'classifier'):
    torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
    st.model = load_model()
    
# Handle [item_batch_count] click listener
if st.button('Submit'):
    st.write('Batch '+str(st.batch_number)+' would be recorded')
    st.session_state['item_batch_count'] += 1
else:
    st.write("Submit to record this detection")

# Setup webrtc Camera Stream
webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=ClassificationVideoProcessorMaker(
        st.batch_number).make(),
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)
