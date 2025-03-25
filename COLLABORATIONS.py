import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

class Collaborate:
    def __init__(self, df):
        try:
            self.client = MongoClient(st.secrets['database']['link'])
        except Exception as e:
            st.error(f"Database connection error: {e}")
        self.data = df
        
    def display(self):
        tab1, tab2 = st.tabs(["Add Data", "View Data"])
        
        with tab1:
            col1, col2 = st.columns([1, 2],border=True)
            
            with col1:
                option = st.radio("Select Operation", 
                                 ["Connect To Data Base", "Add Collections", "Add Data"])
                
            with col2:
                if option == "Connect To Data Base":
                    self._connect_database_ui()
                elif option == "Add Collections":
                    self._add_collections_ui()
                elif option == "Add Data":
                    self._add_data_ui()
                    
        with tab2:
            self._view_data_ui()
    
    def _connect_database_ui(self):
        st.subheader("Connect to Database")
        db_name = st.text_input("Database Name")
        password = st.text_input("Password", type="password")
        
        if st.button("Connect"):
            if not db_name:
                st.error("Please enter a database name")
                return
                
            try:
                db = self.client[db_name]
                authenticator = db['Authenticator']
                
                # Check if database exists
                if db_name in self.client.list_database_names():
                    # Verify password
                    auth_doc = authenticator.find_one()
                    if auth_doc and auth_doc.get('password') == password:
                        st.session_state['database'] = db
                        st.success("Successfully connected to existing database")
                    else:
                        st.error("Password does not match. Connection failed.")
                else:
                    # Create new database
                    authenticator.insert_one({'password': password})
                    st.session_state['database'] = db
                    st.success("New database created successfully")
                    
            except Exception as e:
                st.error(f"Error connecting to database: {e}")
    
    def _add_collections_ui(self):
        st.subheader("Add Collections")
        
        if 'database' not in st.session_state:
            st.warning("Please connect to a database first")
            return
            
        collection_name = st.text_input("Collection Name")
        
        if st.button("Add Collection"):
            if not collection_name:
                st.error("Please enter a collection name")
                return
                
            try:
                if collection_name in st.session_state['database'].list_collection_names():
                    st.warning(f"Collection '{collection_name}' already exists")
                else:
                    st.session_state['database'].create_collection(collection_name)
                    st.success(f"Collection '{collection_name}' created successfully")
            except Exception as e:
                st.error(f"Error creating collection: {e}")
    
    def _add_data_ui(self):
        st.subheader("Add Data to Collection")
        
        if 'database' not in st.session_state:
            st.warning("Please connect to a database first")
            return
            
        if 'allData' not in st.session_state:
            st.warning("No data available in session state")
            return
            
        # Get collections except Authenticator
        collections = [col for col in st.session_state['database'].list_collection_names() 
                      if col != 'Authenticator']
        
        if not collections:
            st.warning("No collections available (except Authenticator)")
            return
            
        selected_collection = st.selectbox("Select Collection", collections)
        
        # Select data from session_state
        data_options = list(st.session_state['allData'].keys())
        selected_data = st.selectbox("Select Data", data_options)
        
        if selected_data:
            st.dataframe(st.session_state['allData'][selected_data])
            
        key = st.text_input("Enter a key for this data")
        description = st.text_area("Enter description")
        
        if st.button("Add Data"):
            if not key or not selected_data:
                st.error("Please provide both a key and select data")
                return
                
            try:
                collection = st.session_state['database'][selected_collection]
                
                # Check if key already exists
                if collection.find_one({'key': key}):
                    st.warning(f"Key '{key}' already exists in this collection")
                    return
                    
                # Prepare document
                doc = {
                    'key': key,
                    'description': description,
                    'data': st.session_state['allData'][selected_data].to_dict('records')
                }
                
                collection.insert_one(doc)
                st.success("Data added successfully to collection")
            except Exception as e:
                st.error(f"Error adding data: {e}")
    
    def _view_data_ui(self):
        col1, col2 = st.columns([1, 2],border=True)
        
        with col1:
            if 'database' not in st.session_state:
                st.warning("Please connect to a database first")
                return
                
            # Get collections except Authenticator
            collections = [col for col in st.session_state['database'].list_collection_names() 
                          if col != 'Authenticator']
            
            if not collections:
                st.warning("No collections available (except Authenticator)")
                return
                
            selected_collection = st.selectbox("Select Collection", collections, key="view_collection")
            view_option = st.radio("View Option", ["View Selected Output", "View All Outputs"])
        
        with col2:
            if view_option == "View Selected Output":
                self._view_selected_output(selected_collection)
            else:
                self._view_all_outputs(selected_collection)
    
    def _view_selected_output(self, collection_name):
        st.subheader("View Selected Output")
        
        collection = st.session_state['database'][collection_name]
        documents = list(collection.find({}, {'key': 1}))
        
        if not documents:
            st.warning("No documents found in this collection")
            return
            
        key_options = [doc['key'] for doc in documents]
        selected_key = st.selectbox("Select Key", key_options)
        
        if selected_key:
            doc = collection.find_one({'key': selected_key})
            
            st.subheader(selected_key, divider='blue')
            st.dataframe(pd.DataFrame(doc['data']))
            st.write("**Description:**", doc.get('description', 'No description available'))
    
    def _view_all_outputs(self, collection_name):
        st.subheader("View All Outputs")
        
        collection = st.session_state['database'][collection_name]
        documents = list(collection.find())
        
        if not documents:
            st.warning("No documents found in this collection")
            return
            
        for doc in documents:
            st.subheader(doc['key'], divider='blue')
            st.dataframe(pd.DataFrame(doc['data']))
            st.write("**Description:**", doc.get('description', 'No description available'))
            st.divider()
