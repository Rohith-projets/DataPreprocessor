import streamlit as st
import pandas as pd
import chardet
from io import BytesIO

class COMPARE:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        if 'allData' not in st.session_state:
            st.session_state['allData'] = {}

    def detect_encoding(self, file):
        try:
            rawdata = file.read()
            result = chardet.detect(rawdata)
            file.seek(0)  # Reset file pointer
            return result['encoding']
        except Exception as e:
            st.error(f"Error detecting encoding: {str(e)}")
            return None

    def read_uploaded_file(self, file):
        try:
            encoding = self.detect_encoding(file)
            if file.name.endswith('.csv'):
                return pd.read_csv(file, encoding=encoding)
            elif file.name.endswith(('.xls', '.xlsx')):
                return pd.read_excel(file)
            else:
                st.error("Unsupported file format")
                return None
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            return None

    def parse_input_values(self, input_str):
        try:
            from ast import literal_eval
            values = [literal_eval(x.strip()) for x in input_str.split(',')]
            
            if len(values) == 1:
                return values[0]
            elif len(values) == len(self.dataframe.columns):
                return pd.Series(values, index=self.dataframe.columns)
            elif len(values) == len(self.dataframe.index):
                return pd.Series(values, index=self.dataframe.index)
            else:
                st.error("Number of values must match columns or index length")
                return None
        except:
            values = [x.strip() for x in input_str.split(',')]
            if len(values) == 1:
                return values[0]
            else:
                return values

    def display(self):
        try:
            st.title("DataFrame Comparison Tool")
            
            col1, col2, col3 = st.columns([1, 2, 1], border=True)
            col1.subheader("Operation", divider='blue')
            col2.subheader("Implementation", divider='blue')
            col3.subheader("Configuration", divider='blue')

            with col1:
                operation = st.radio(
                    "Select Operation",
                    ["Value Comparison", "Dataset Comparison", "Compare Outputs", "Compare Selection"],
                    key="operation_select"
                )

            with col3:
                comparison_type = st.radio(
                    "Comparison Type",
                    ["Equal (eq)", "Not Equal (ne)", "Less Than (lt)",
                     "Greater Than (gt)", "Less Equal (le)", "Greater Equal (ge)"],
                    key="comparison_type"
                )
                
                axis = st.selectbox(
                    "Axis",
                    ["columns", "index"],
                    key="axis_select"
                )

            with col2:
                if operation == "Value Comparison":
                    input_values = st.text_input(
                        "Enter comma-separated values:",
                        help="Enter values to compare with the DataFrame"
                    )
                    
                    if st.button("Compare Values"):
                        if input_values:
                            values = self.parse_input_values(input_values)
                            if values is not None:
                                op_map = {
                                    "Equal (eq)": "eq",
                                    "Not Equal (ne)": "ne",
                                    "Less Than (lt)": "lt",
                                    "Greater Than (gt)": "gt",
                                    "Less Equal (le)": "le",
                                    "Greater Equal (ge)": "ge"
                                }
                                op = op_map[comparison_type]
                                try:
                                    result = getattr(self.dataframe, op)(values, axis=axis)
                                    key = f"{op}_with_values_{str(values)[:20]}"
                                    st.session_state['allData'][key] = result
                                    st.success("Comparison completed!")
                                    st.dataframe(result)
                                except Exception as e:
                                    st.error(f"Error during comparison: {str(e)}")

                elif operation == "Dataset Comparison":
                    uploaded_file = st.file_uploader(
                        "Upload dataset (CSV/Excel)",
                        type=['csv', 'xlsx', 'xls'],
                        key="dataset_uploader"
                    )
                    
                    if uploaded_file:
                        other_df = self.read_uploaded_file(uploaded_file)
                        if other_df is not None and st.button("Compare Datasets"):
                            op_map = {
                                "Equal (eq)": "eq",
                                "Not Equal (ne)": "ne",
                                "Less Than (lt)": "lt",
                                "Greater Than (gt)": "gt",
                                "Less Equal (le)": "le",
                                "Greater Equal (ge)": "ge"
                            }
                            op = op_map[comparison_type]
                            try:
                                result = getattr(self.dataframe, op)(other_df)
                                key = f"{op}_with_dataset_{uploaded_file.name[:20]}"
                                st.session_state['allData'][key] = result
                                st.success("Comparison completed!")
                                st.dataframe(result)
                            except Exception as e:
                                st.error(f"Error during comparison: {str(e)}")

                elif operation == "Compare Outputs":
                    if st.session_state['allData']:
                        selected_keys = st.multiselect(
                            "Select outputs to compare",
                            list(st.session_state['allData'].keys()),
                            key="output_select"
                        )
                        
                        if len(selected_keys) == 2 and st.button("Compare Selected"):
                            df1 = st.session_state['allData'][selected_keys[0]]
                            df2 = st.session_state['allData'][selected_keys[1]]
                            try:
                                comparison_result = df1.compare(df2)
                                key = f"comparison_{selected_keys[0]}_vs_{selected_keys[1]}"
                                st.session_state['allData'][key] = comparison_result
                                st.success("Comparison completed!")
                                st.dataframe(comparison_result)
                            except Exception as e:
                                st.error(f"Error during comparison: {str(e)}")
                    else:
                        st.warning("No comparison results available yet")

                elif operation == "Compare Selection":
                    source_columns = st.multiselect(
                        "Select source columns",
                        self.dataframe.columns,
                        key="source_columns"
                    )
                    target_columns = st.multiselect(
                        "Select target columns",
                        self.dataframe.columns,
                        key="target_columns"
                    )
                    
                    if source_columns and target_columns and st.button("Compare Selected Columns"):
                        try:
                            source_df = self.dataframe[source_columns]
                            target_df = self.dataframe[target_columns]
                            op_map = {
                                "Equal (eq)": "eq",
                                "Not Equal (ne)": "ne",
                                "Less Than (lt)": "lt",
                                "Greater Than (gt)": "gt",
                                "Less Equal (le)": "le",
                                "Greater Equal (ge)": "ge"
                            }
                            op = op_map[comparison_type]
                            result = getattr(source_df, op)(target_df)
                            key = f"{op}_source_vs_target_{','.join(source_columns)}_vs_{','.join(target_columns)}"
                            st.session_state['allData'][key] = result
                            st.success("Comparison completed!")
                            st.dataframe(result)
                        except Exception as e:
                            st.error(f"Error during comparison: {str(e)}")

            # Display all stored results without an expander
            if st.session_state['allData']:
                st.subheader("All Comparison Results")
                for key, df in st.session_state['allData'].items():
                    st.subheader(key)
                    st.dataframe(df)
            else:
                st.info("No comparison results yet")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
