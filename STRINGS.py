
import streamlit as st
import pandas as pd


class Strings:
  def __init__(self,dataset):
    self.dataset=dataset
  def display(self):
    tab1,tab2,tab3=st.tabs(["Basic String Functions","Advanced String Functions","View Data Here"])
    with tab1:
      col1,col2=st.columns([1,2],border=True)
      option=col1.radio("Select Operations From This Column",["Capitalize","Tiltle","Lower Case","Upper Case","Change Cases","Center String","Count","Ends With","Starts With","find substring strting position from left","find substring starting position from right"])
      try:
        if option=="Capitalize":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[selected_columns+"(Capitalized)"]=self.dataset[selected_columns].str.capitalize()
            col2.dataframe(data)
        elif option =="Tiltle":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data=self.dataset.copy(deep=True)
            data[selected_columns+"(Titled)"]=self.dataset[selected_columns].str.title()
            col2.dataframe(data)
        elif option == "Lower Case":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[selected_columns+"(lower)"]=self.dataset[selected_columns].str.lower()
            col2.dataframe(data)
        elif option == "Upper Case":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[selected_columns+"(upper)"]=self.dataset[selected_columns].str.upper()
            col2.dataframe(data)
        elif option == "Change Cases":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[selected_columns+"(upper)"]=self.dataset[selected_columns].str.swapcase()
            col2.dataframe(data)
        elif option =="Center String":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          total_charcters=int(col2.number_input("Select the total number of characters when the string is centered",1))
          startswith=col2.text_input("Enter deleimeter or any symbol or any character to pand on left and right of the string")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Centered)-{total_charcters}-{startswith}"]=self.dataset[selected_columns].str.center(total_charcters,startswith)
            col2.dataframe(data)
        elif option == "Count":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Sub String To Know Its Frequencies")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(count)-{startswith}"]=self.dataset[selected_columns].str.count(startswith)
            col2.dataframe(data)
        elif option == "Ends With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Suffix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(endswith)-{startswith}"]=self.dataset[selected_columns].str.endswith(startswith)
            col2.dataframe(data)
        elif option == "Starts With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Prefix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Starts With)-{startswith}"]=self.dataset[selected_columns].str.startswith(startswith)
            col2.dataframe(data)
      except Exception as e:
        col2.error(e)
        
