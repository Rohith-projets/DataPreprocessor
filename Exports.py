import pandas as pd
import streamlit as st
import numpy as np
import io

class Exports:
    def __init__(self, df):
        self.dataset = df

    def display(self):
        tab1, tab2 = st.tabs(["View Operations", "View Data"])

        with tab1:
            col1, col2 = st.columns([1, 2], border=True)

            options = col1.radio("Options", [
                "To ORC", "To Parquet", "To Pickle", "To Feather", "To CSV",
                "To SQL", "To HDF5", "To JSON", "To Dict", "To HTML", "To LaTeX", 
                "To Stata", 
                "To Clipboard", "To Markdown"
            ])

            file_buffer = io.BytesIO()  # In-memory storage
            mime_type = None
            file_name = None
            show_inputs = False  # Whether extra inputs are needed

            if options == "To ORC":
                file_name = "exported_data.orc"
                self.dataset.to_orc(file_buffer, engine="pyarrow")
                mime_type = "application/octet-stream"

            elif options == "To Parquet":
                file_name = "exported_data.parquet"
                self.dataset.to_parquet(file_buffer, compression="snappy")
                mime_type = "application/octet-stream"

            elif options == "To Pickle":
                file_name = "exported_data.pkl"
                self.dataset.to_pickle(file_buffer, compression="gzip")
                mime_type = "application/octet-stream"

            elif options == "To Feather":
                file_name = "exported_data.feather"
                self.dataset.to_feather(file_buffer)
                mime_type = "application/octet-stream"

            elif options == "To CSV":
                file_name = "exported_data.csv"
                self.dataset.to_csv(file_buffer, index=False)
                mime_type = "text/csv"

            elif options == "To SQL":
                show_inputs = True
                sql_table_name = col1.text_input("Enter SQL Table Name")
                db_uri = col1.text_input("Enter Database URI")
                if col1.button("Export to SQL"):
                    from sqlalchemy import create_engine
                    engine = create_engine(db_uri)
                    self.dataset.to_sql(sql_table_name, con=engine, if_exists="replace")
                    col2.success(f"Data exported to SQL table: {sql_table_name}")

            elif options == "To HDF5":
                show_inputs = True
                hdf_key = col1.text_input("Enter HDF5 Key")
                file_name = "exported_data.h5"
                if col1.button("Export to HDF5"):
                    self.dataset.to_hdf(file_name, key=hdf_key, mode="w")
                    col2.success(f"Data exported to {file_name}")

            elif options == "To JSON":
                file_name = "exported_data.json"
                self.dataset.to_json(file_buffer, orient="records")
                mime_type = "application/json"

            elif options == "To Dict":
                col2.json(self.dataset.to_dict())

            elif options == "To HTML":
                file_name = "exported_data.html"
                self.dataset.to_html(file_buffer)
                mime_type = "text/html"

            elif options == "To LaTeX":
                file_name = "exported_data.tex"
                self.dataset.to_latex(file_buffer)
                mime_type = "application/x-latex"

            elif options == "To Stata":
                file_name = "exported_data.dta"
                self.dataset.to_stata(file_buffer)
                mime_type = "application/octet-stream"

            elif options == "To String":
                col2.text(self.dataset.to_string())

            elif options == "To Clipboard":
                self.dataset.to_clipboard()
                col2.success("Copied to clipboard!")

            elif options == "To Markdown":
                file_name = "exported_data.md"
                markdown_data = self.dataset.to_markdown()
                file_buffer.write(markdown_data.encode())  # Convert string to bytes
                mime_type = "text/markdown"

            # Show Download Button if applicable
            if file_name and not show_inputs:
                file_buffer.seek(0)  # Reset pointer
                col2.download_button(
                    label="Download File",
                    data=file_buffer,
                    file_name=file_name,
                    mime=mime_type
                )

        with tab2:
            st.subheader("View Data", divider='blue')
            st.dataframe(self.dataset)
