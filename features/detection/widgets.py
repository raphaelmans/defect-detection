
import streamlit as st


class Widgets:

    def preview_radio_button(self):
        preview = st.radio(
            "Preview:",
            ('None', 'Binary Segmentation', 'Contact Sections'))

        binary_segmentation = preview == 'Binary Segmentation'
        contact_lines = preview == 'Contact Sections'

        return binary_segmentation, contact_lines

    def white_threshold_slider(self):
        # Setup [white_threshold] widget and state
        white_threshold = st.slider(
            "White Percentage Threshold",
            value=5, max_value=100, min_value=1, key='white_threshold')
        return white_threshold

    def binary_threshold_slider(self):
        # Setup [threshold] widget and state
        binary_threshold = st.slider("Black Binary Threshold",
                                     value=175, max_value=255, min_value=1, key='threshold')
        return binary_threshold

    def batch_number_input(self):
        # Setup [batch_number] widget and state
        batch_number = st.number_input(
            'Insert batch number', format="%d", value=1001, step=1, key='batch_number')
        return batch_number

    def evaluation_checkbox(self):
        # Setup [model_evaluation] widget and state
        checkbox = st.checkbox('Start Evaluation', key='model_evaluation')
        return checkbox

    def init_session_state(self):
        if 'item_batch_count' not in st.session_state:
            st.session_state['item_batch_count'] = 0