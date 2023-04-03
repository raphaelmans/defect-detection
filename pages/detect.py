import streamlit as st
from model import load_model
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from classification_video_processor import ClassificationVideoProcessorMaker
from features.detection.widgets import init_widgets, init_session_state
from features.detection.components import Components


init_session_state()
init_widgets()

load_model()
    
Components.batch_button(st.batch_number)

# Setup webrtc Camera Stream
webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=ClassificationVideoProcessorMaker(
        st.batch_number).make(),
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)
