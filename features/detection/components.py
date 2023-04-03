
import streamlit as st



class Components:

    @staticmethod
    def batch_button(batch_number):
        # Handle [item_batch_count] click listener
        if st.button('Submit'):
            st.write('Batch '+str(batch_number)+' would be recorded')
            st.session_state['item_batch_count'] += 1
        else:
            st.write("Submit to record this detection")