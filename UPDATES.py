import streamlit as st
import pandas as pd

class Updates:
  def __init__(self,df):
    self.dataset=df
  def display(self):
    tab1,tab2=st.tabs(["Perform Operations Here","Documentation"])
    with tab1:
      col1,col2=st.columns([1,2],border=True)
      selected_option=col1.radio("Select option",["Edit Manually","Single Value Edit","Multi Edit","Milti Edit Using Condition"])
      if selected_option=="Edit Manually":
        self.edit_manually(col2)
      elif selected_option=="Single Value Edit":
        self.single_value_edit(col2)
      elif selected_option=="Multi Edit":
        self.multi_edit(col2)
      elif option=="Milti Edit Using Condition":
        self.multi_edit_condition(col2)
  def edit_manually(self,col2):
    edited_data=col2.data_editor(self.dataset,num_rows="dynamic")
    if col2.button("Conform These Changes",use_container_width=True,type='primary'):
      st.session_state['allData']["Stage - Updates - Edited Datframe - Manually"]=edited_data
  def single_value_edit(self,col2):
    selected_column=col2.selectbox("Selecte a column",self.dataset.columns.tolist())
    selected_row=col2.selectbox("Select row to edit value",self,dataset.index.tolist())
    entered_value=col2.text_input("Enter value to be replaced")
    if col2.button("Confirm Update",use_container_width=True,type='primary'):
      edited_dataframe=self.dataset.copy(deep=True)
      edited_data[selected_column][selected_row]=entered_value
      col2.dataframe(edited_data[:][selected_row])
      st.session_state['allData'][f'Stage - Updates - Edit Single Value - {selected_column} - {selected_row} - {entered_value}']=edited_data
  def multi_edit(self,col2):
    pass
  def multi_edit_condition(self,col2):
    pass
