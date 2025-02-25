import pandas as pd
import streamlit as st
from sklearn.preprocessing import *

class DataCleaners:
    def __init__(self, df):
        self.dataset = df
    
    def label_binarizer(self, col2):
        columns = col2.multiselect("Select the columns for label binarization", self.dataset.columns.tolist())
        
        if columns:
            if col2.button("Apply Label Binarizer", use_container_width=True, type='primary'):
                dataset = self.dataset.copy()
                
                for col in columns:
                    lb = LabelBinarizer()
                    transformed = lb.fit_transform(dataset[col])
                    
                    if len(lb.classes_) > 2:
                        column_names = [f"{col}_{cls}" for cls in lb.classes_]
                        transformed_df = pd.DataFrame(transformed, columns=column_names, index=dataset.index)
                        dataset = pd.concat([dataset, transformed_df], axis=1)
                    else:
                        dataset[f"{col}_Binarized"] = transformed
                
                st.session_state['allData'][f'Stage - ML - Label Binarizer - {columns}'] = dataset
                col2.dataframe(dataset)
    
    def multi_label_binarizer(self, col2):
        columns = col2.multiselect("Select the columns for multi-label binarization", self.dataset.columns.tolist())
        
        if columns:
            if col2.button("Apply Multi Label Binarizer", use_container_width=True, type='primary'):
                dataset = self.dataset.copy()
                
                for col in columns:
                    mlb = MultiLabelBinarizer()
                    transformed = mlb.fit_transform(dataset[col].astype(str).apply(lambda x: x.split(",")))
                    
                    column_names = [f"{col}_{cls}" for cls in mlb.classes_]
                    transformed_df = pd.DataFrame(transformed, columns=column_names, index=dataset.index)
                    dataset = pd.concat([dataset, transformed_df], axis=1)
                
                st.session_state['allData'][f'Stage - ML - Multi Label Binarizer - {columns}'] = dataset
                col2.dataframe(dataset)
    def binarize(self, col2):
        columns = col2.multiselect("Select the columns to convert continuous data into binary data", self.dataset.columns.tolist())
        dataset = self.dataset
        thresholdValue = col2.number_input("Specify The Threshold Value")

        if col2.button("Apply Binarizer", use_container_width=True, type='primary'):
            # Accessing dataframe columns
            new_data_frame = dataset[columns]

            try:
                binarizer = Binarizer(threshold=thresholdValue)
                values = binarizer.fit_transform(new_data_frame)
                dataset[columns] = values

                st.session_state['allData'][f"Stage - Final - ML - Descritization - Binarizer - {columns}"] = dataset

                col2.subheader("Converted Data", divider=True)
                col2.dataframe(dataset)

            except Exception as e:
                col2.warning(e)
