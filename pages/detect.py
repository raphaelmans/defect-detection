import streamlit as st
from db import AppDatabase
from model import load_model
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from classification_video_processor import ClassificationVideoProcessorMaker
from features.detection.widgets import Widgets as DetectionWidgets
from features.detection.components import Components

detection_widgets = DetectionWidgets()

components = Components()

st.header('Defect Detection')

[bt_number] = AppDatabase.run_query_one(st.db_conn,"SELECT COUNT(*) FROM Batch")
detection_widgets.batch_number_id(int(bt_number) + 1)
st.batch_number = bt_number + 1

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
