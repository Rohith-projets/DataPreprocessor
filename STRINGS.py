
import streamlit as st
import pandas as pd


class Strings:
  def __init__(self,dataset):
    self.dataset=dataset
  def display(self):
    tab1,tab2,tab3=st.tabs(["Basic String Functions","Advanced String Functions","View Data Here"])
    with tab1:
      col1,col2=st.columns([1,2],border=True)
      option=col1.radio("Select Operations From This Column",["Convert First Character To Upper Case","Convert Sentece to Tiltle","Lower Case","Upper Case","Change Cases"])
      try:
        if option=="Convert First Character To Upper Case":
          selected_columns=col2.multiselect("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            new_columns=[x+"Capitalized" for x in selected_columns]
            for i in range(len(new_columns)):
              data[new_columns[i]]=self.dataset[selected_column[i]].str.capitalize()
            col2.dataframe(data)
        elif option =="Convert Sentece to Tiltle":
          selected_columns=col2.multiselect("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            new_columns=[x+"Titled" for x in selected_columns]
            for i in range(len(new_columns)):
              data[new_columns[i]]=self.dataset[selected_column[i]].str.title()
            col2.dataframe(data)
        elif option == "Lower Case":
          selected_columns=col2.multiselect("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            new_columns=[x+"Lowered" for x in selected_columns]
            for i in range(len(new_columns)):
              data[new_columns[i]]=self.dataset[selected_column[i]].str.casefold()
            col2.dataframe(data)
        elif option == "Upper Case":
          selected_columns=col2.multiselect("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            new_columns=[x+"Uppered" for x in selected_columns]
            for i in range(len(new_columns)):
              data[new_columns[i]]=self.dataset[selected_column[i]].str.upper()
            col2.dataframe(data)
        elif option == "Change Cases":
          selected_columns=col2.multiselect("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            new_columns=[x+"Swap Cased" for x in selected_columns]
            for i in range(len(new_columns)):
              data[new_columns[i]]=self.dataset[selected_column[i]].str.swapcase()
            col2.dataframe(data)
      except Exception as e:
        col2.error(e)
        
