import streamlit as st
from db import AppDatabase
from model import load_model
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from classification_video_processor import ClassificationVideoProcessorMaker
from features.detection.widgets import Widgets as DetectionWidgets
from features.detection.components import Components
from features.models.batch import BatchInsertDTO


database = AppDatabase.init_connection()

detection_widgets = DetectionWidgets()
detection_widgets.init_start_session()

components = Components()

st.header('Defect Detection')

st.model = load_model()


if (st.session_state['start_session'] == False):
    st.batch_name = detection_widgets.batch_name_input(
        'BATCH-1')
    st.product_model = detection_widgets.product_model_input('PWB-1')
    st.department = detection_widgets.department_input('Wiring Boards')

    components.start_session_button()


elif (st.session_state['start_session'] == True):
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

    # Setup webrtc Camera Stream
    webrtc_ctx = webrtc_streamer(
        key="WYH",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=ClassificationVideoProcessorMaker(
            database).make(),
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )
