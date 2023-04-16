import streamlit as st
import mysql.connector


class AppDatabase:
    # Initialize connection.
    # Uses st.cache_resource to only run once.
    @st.cache_resource
    def init_connection():
        return mysql.connector.connect(**st.secrets["mysql"])
    
    @st.cache_data(ttl=600)
    def run_query(_conn,query):
        with _conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
        
    @st.cache_data(ttl=600)
    def run_query_one(_conn,query):
        with _conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchone()
    




