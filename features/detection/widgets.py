
import streamlit as st


class Widgets:

    def contact_orientation_radio_button(self):
        orientation = st.radio(
            "Orientation:",
            ('Horizontal', 'Vertical'))

        return orientation

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

    def batch_number_input(self, value):
        # Setup [batch_number] widget and state
        batch_number = st.number_input(
            'Insert batch number', format="%d", value=value, disabled=True, key='batch_number')
        return batch_number
    
    def batch_number_id(self, value):
        # Setup [batch_number] widget and state
        batch_number = st.text(f'Batch ID: {value}')
        return batch_number

    def evaluation_checkbox(self):
        # Setup [model_evaluation] widget and state
        checkbox = st.checkbox('Start Evaluation', key='model_evaluation')
        return checkbox


    def batch_name_input(self, value):
        # Setup [batch_name] widget and state
        batch_name = st.text_input(
            'Batch Name', value=value, key='batch_name')
        return batch_name
    
    def product_model_input(self, value):
        # Setup [product_model] widget and state
        product_model = st.text_input(
            'Product Model', value=value, key='product_model')
        return product_model
    
    def department_input(self, value):
        # Setup [department] widget and state
        department = st.text_input(
            'Department', value=value, key='department')
        return department
    

    # Deprecated
    def init_session_state(self):
        if 'item_batch_count' not in st.session_state:
            st.session_state['item_batch_count'] = 0

    def init_start_session(self):
        if 'start_session' not in st.session_state:
            st.session_state['start_session'] = False
