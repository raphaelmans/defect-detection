import streamlit as st
from db import AppDatabase
from features.dashboard.widgets import DashboardWidgets

db_conn = AppDatabase.init_connection()
st.db_conn = db_conn

cursor = db_conn.cursor()
print("=====DB CONNECTED=====")


if 'dirtyItemsCount' not in st.session_state:
    st.session_state['dirtyItemsCount'] = 0

if 'item_batch_count' not in st.session_state:
    st.session_state['item_batch_count'] = 0


def main():
    st.header('Dashboard')


    fig_time_chart = DashboardWidgets.defect_rate_over_time_chart(db_conn)
    st.plotly_chart(fig_time_chart)


    with st.container():
        col1, col2 = st.columns(2)
        fig_rate_per_batch = DashboardWidgets.defect_rate_per_batch_chart(db_conn)

        fig_rate_by_product_model = DashboardWidgets.defect_rate_by_product_model(db_conn)
        with col1:
            st.plotly_chart(fig_rate_per_batch)
        with col2:
            st.plotly_chart(fig_rate_by_product_model)


if __name__ == '__main__':
    main()
