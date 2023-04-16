import streamlit as st
from model import load_model
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from classification_video_processor import ClassificationVideoProcessorMaker
from features.detection.widgets import Widgets as DetectionWidgets
from features.detection.components import Components

detection_widgets = DetectionWidgets()
detection_widgets.init_session_state()

components = Components()

st.header('Defect Detection')

batch_number = detection_widgets.batch_number_input()
st.batch_number = batch_number
components.batch_button_submit(batch_number)

threshold = detection_widgets.binary_threshold_slider()
st.threshold = threshold

white_threshold = detection_widgets.white_threshold_slider()
st.white_threshold = white_threshold


contact_orientation = detection_widgets.contact_orientation_radio_button()
st.contact_orientation = contact_orientation

bs, cl = detection_widgets.preview_radio_button()
st.binary_segmentation = bs
st.contact_lines = cl

eva_cb = detection_widgets.evaluation_checkbox()
st.model_evaluation = eva_cb

load_model()

# Setup webrtc Camera Stream
webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=ClassificationVideoProcessorMaker(
        st.batch_number).make(),
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)
