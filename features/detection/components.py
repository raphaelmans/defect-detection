
import streamlit as st

def start_session():
    st.write('Session started')
    st.session_state['start_session'] = True
class Components:

    def batch_button_submit(self, batch_number):
        # Handle [item_batch_count] click listener
        if st.button('Submit'):
            st.write('Batch '+str(batch_number)+' would be recorded')
            st.session_state['item_batch_count'] += 1
        else:
            st.write("Submit to record this detection")
    
    def start_session_button(self):
        # Handle [start_session] click listener
        st.button('Start Session', on_click=start_session)
