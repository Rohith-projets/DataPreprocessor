import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

if "allData" not in st.session_state:
    st.session_state["allData"] = {}
    
class GenerativeAI:
    def __init__(self, data):
        self.data = data  # Store dataframe
    def display(self):
        tab1,tab2=st.tabs(["Implement Operations","View Data"])
        if self.data is not None:
            with tab1:
                option=st.selectbox("Do You Want To Create Dashboard",["No","Yes"])
                if option=="Yes":
                    st.subheader("Data Profiler",divider='blue')
                    profile = ProfileReport(self.data, explorative=True)
                    st_profile_report(profile)
                else:
                    st.info("Select Yes For Stunning Informative Dashboard")
            with tab2:
                st.subheader("Selected Data Appears Here",divider='blue')
                st.dataframe(self.data)
        else:
            st.info("No data available. Please upload a dataset.")
