import streamlit as st
import pandas as pd
import ast
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
    edited_data=col2.data_editor(self.dataset,num_rows="dynamic",hide_index=False)
    if col2.button("Conform These Changes",use_container_width=True,type='primary'):
      st.session_state['allData']["Stage - Updates - Edited Datframe - Manually"]=edited_data
  def single_value_edit(self,col2):
    try:
      edited_dataframe=self.dataset.copy(deep=True)
      selected_column=col2.selectbox("Selecte a column",self.dataset.columns.tolist())
      selected_row=int(col2.number_input("Select row to edit value (index value)"))
      entered_value=ast.literal_eval(col2.text_input("Enter value to be replaced"))
      col2.warning(f"Present Value - {edited_dataframe[selected_column][selected_row]}")
      if col2.button("Confirm Update",use_container_width=True,type='primary'):
        edited_dataframe.iat[selected_row, self.dataset.columns.get_loc(selected_column)] = entered_value
        col2.dataframe(edited_dataframe[:][selected_row])
        st.session_state['allData'][f'Stage - Updates - Edit Single Value - {selected_column} - {selected_row} - {entered_value}']=edited_dataframe
    except Exception as e:
      col2.error(e)
  def multi_edit(self,col2):
    pass
  def multi_edit_condition(self,col2):
    pass
