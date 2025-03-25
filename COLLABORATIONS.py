import streamlit as st
import pandas as pd
from pymongo import MongoClient

class Collaborate:
    def __init__(self, df):
        try:
            self.client = MongoClient(st.secrets['database']['link'])
        except Exception as e:
            st.error(f"Database connection error: {e}")
        self.data = df
        
    def display(self):
        tab1, tab2, tab3, tab4 = st.tabs(["Add Data", "View Data", "Modify Data", "Delete Data"])
        
        with tab1:
            self._add_data_tab()
                    
        with tab2:
            self._view_data_tab()
            
        with tab3:
            self._modify_data_tab()
            
        with tab4:
            self._delete_data_tab()
    
    def _add_data_tab(self):
        col1, col2 = st.columns([1, 2], border=True)
        
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
    
    def _view_data_tab(self):
        col1, col2 = st.columns([1, 2], border=True)
        
        with col1:
            if 'database' not in st.session_state:
                st.warning("Please connect to a database first")
                return
                
            collections = self._get_collections()
            if not collections:
                return
                
            selected_collection = st.selectbox("Select Collection", collections, key="view_collection")
            view_option = st.radio("View Option", ["View Selected Output", "View All Outputs"])
        
        with col2:
            if view_option == "View Selected Output":
                self._view_selected_output(selected_collection)
            else:
                self._view_all_outputs(selected_collection)
    
    def _modify_data_tab(self):
        col1, col2 = st.columns([1, 2], border=True)
        
        with col1:
            if 'database' not in st.session_state:
                st.warning("Please connect to a database first")
                return
                
            collections = self._get_collections()
            if not collections:
                return
                
            selected_collection = st.radio("Select Collection", collections, key="modify_collection")
        
        with col2:
            if selected_collection:
                self._modify_collection_data(selected_collection)
    
    def _delete_data_tab(self):
        col1, col2 = st.columns([1, 2], border=True)
        
        with col1:
            if 'database' not in st.session_state:
                st.warning("Please connect to a database first")
                return
                
            delete_option = st.radio("Delete Option", 
                                   ["Delete Database", "Delete Collection", "Delete Documents"])
        
        with col2:
            if delete_option == "Delete Database":
                self._delete_database_ui()
            elif delete_option == "Delete Collection":
                self._delete_collection_ui()
            elif delete_option == "Delete Documents":
                self._delete_documents_ui()
    
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
                
                if db_name in self.client.list_database_names():
                    auth_doc = authenticator.find_one()
                    if auth_doc and auth_doc.get('password') == password:
                        st.session_state['database'] = db
                        st.success("Successfully connected to existing database")
                    else:
                        st.error("Password does not match. Connection failed.")
                else:
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
            
        collections = self._get_collections()
        if not collections:
            return
            
        selected_collection = st.selectbox("Select Collection", collections)
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
                
                if collection.find_one({'key': key}):
                    st.warning(f"Key '{key}' already exists in this collection")
                    return
                    
                doc = {
                    'key': key,
                    'description': description,
                    'data': st.session_state['allData'][selected_data].to_dict('records')
                }
                
                collection.insert_one(doc)
                st.success("Data added successfully to collection")
            except Exception as e:
                st.error(f"Error adding data: {e}")
    
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
    
    def _modify_collection_data(self, collection_name):
        st.subheader(f"Modify Data in {collection_name}")
        
        collection = st.session_state['database'][collection_name]
        documents = list(collection.find({}, {'key': 1}))
        
        if not documents:
            st.warning("No documents found in this collection")
            return
            
        key_options = [doc['key'] for doc in documents]
        selected_key = st.selectbox("Select Document to Modify", key_options)
        
        if selected_key:
            doc = collection.find_one({'key': selected_key})
            
            st.subheader("Current Values", divider='blue')
            st.text_input("Current Key", value=doc['key'], disabled=True)
            st.text_area("Current Description", value=doc.get('description', ''), disabled=True)
            st.dataframe(pd.DataFrame(doc['data']), use_container_width=True)
            
            st.subheader("New Values", divider='blue')
            new_key = st.text_input("New Key", value=doc['key'])
            new_description = st.text_area("New Description", value=doc.get('description', ''))
            
            if 'allData' in st.session_state:
                data_options = list(st.session_state['allData'].keys())
                selected_data = st.selectbox("Select New Data (optional)", [""] + data_options)
            else:
                selected_data = ""
            
            if st.button("Update Document"):
                update_data = {}
                
                if new_key != doc['key']:
                    if collection.find_one({'key': new_key}):
                        st.error(f"Key '{new_key}' already exists in this collection")
                        return
                    update_data['key'] = new_key
                
                if new_description != doc.get('description', ''):
                    update_data['description'] = new_description
                
                if selected_data and selected_data != "":
                    update_data['data'] = st.session_state['allData'][selected_data].to_dict('records')
                
                if update_data:
                    collection.update_one({'key': selected_key}, {'$set': update_data})
                    st.success("Document updated successfully")
                else:
                    st.warning("No changes detected")
    
    def _delete_database_ui(self):
        st.subheader("Delete Database")
        
        db_name = st.session_state['database'].name
        st.warning(f"You are about to delete the entire database: {db_name}")
        
        confirmation = st.text_input(f"Type '{db_name}' to confirm")
        
        if st.button("Delete Database", type="primary"):
            if confirmation == db_name:
                try:
                    self.client.drop_database(db_name)
                    del st.session_state['database']
                    st.success(f"Database '{db_name}' deleted successfully")
                except Exception as e:
                    st.error(f"Error deleting database: {e}")
            else:
                st.error("Confirmation name does not match")
    
    def _delete_collection_ui(self):
        st.subheader("Delete Collection")
        
        collections = self._get_collections()
        if not collections:
            return
            
        selected_collections = st.multiselect("Select Collections to Delete", collections)
        
        if st.button("Delete Selected Collections", type="primary"):
            for col_name in selected_collections:
                try:
                    st.session_state['database'].drop_collection(col_name)
                    st.success(f"Collection '{col_name}' deleted successfully")
                except Exception as e:
                    st.error(f"Error deleting collection '{col_name}': {e}")
    
    def _delete_documents_ui(self):
        st.subheader("Delete Documents")
        
        collections = self._get_collections()
        if not collections:
            return
            
        selected_collection = st.selectbox("Select Collection", collections)
        
        if selected_collection:
            collection = st.session_state['database'][selected_collection]
            documents = list(collection.find({}, {'key': 1}))
            
            if not documents:
                st.warning("No documents found in this collection")
                return
                
            document_keys = [doc['key'] for doc in documents]
            selected_docs = st.multiselect("Select Documents to Delete", document_keys)
            
            if st.button("Delete Selected Documents", type="primary"):
                for doc_key in selected_docs:
                    try:
                        collection.delete_one({'key': doc_key})
                        st.success(f"Document '{doc_key}' deleted successfully")
                    except Exception as e:
                        st.error(f"Error deleting document '{doc_key}': {e}")
    
    def _get_collections(self):
        if 'database' not in st.session_state:
            return []
            
        collections = [col for col in st.session_state['database'].list_collection_names() 
                      if col != 'Authenticator']
        
        if not collections:
            st.warning("No collections available (except Authenticator)")
            
        return collections
