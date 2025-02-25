import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from klib.clean import data_cleaning
from klib import pool_duplicate_subsets
from klib.describe import cat_plot, corr_mat, corr_plot, dist_plot, missingval_plot

class OptimizeData:
    def __init__(self, df):
        self.dataset = df

    def display(self):
        tab1, tab2 = st.tabs(["Perform Operations", "View Data"])

        with tab1:
            col1, col2 = st.columns([1, 2], border=True)
            if col1.toggle("Optimize Data"):
                dataset = self.dataset
                newDataset = data_cleaning(dataset)
                st.session_state['allData']["Stage 1 - Optimize Data - Clean Data(Normal)"] = newDataset
                col2.subheader("Optimized Data", divider='blue')
                col2.dataframe(newDataset)
                col2.subheader("Some Info On How Data Is Cleaned & Optimized", divider='blue')
                col2.text("By applying klib.data_cleaning() the size reduces by about 44 MB (-85.2%)...")
        with tab2:
            st.subheader("View Data", divider='blue')
            st.dataframe(self.dataset)
