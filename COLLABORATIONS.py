import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
import smtplib
from email.message import EmailMessage

# Initialize session state values
session_defaults = {
    'count': 1,
    'sender_email': None,
    'receiver_email': []
}
for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

class Collaborate:
    def __init__(self, df):
        try:
            self.client = MongoClient(st.secrets['database']['link'])
            self.db = self.client['Collaborations']
            self.collection = self.db['collaborations']
        except Exception as e:
            st.error(f"Database connection error: {e}")
        self.data = df

    def display(self):
        tab1, tab2, tab3 = st.tabs(["Collaborate", "View", "Learn"])
        with tab1:
            self.collaborate()
        with tab2:
            self.view()
        with tab3:
            pass

    def collaborate(self):
        col1, col2 = st.columns([1, 2])
        with col1:
            radio_options = st.radio("Options", ["Enter Addresses", "Add Data", "Send Mails"])

        if radio_options == "Enter Addresses":
            sender_email = col2.text_input("Enter your email address")
            receiver_addresses = col2.text_area("Enter team members' email addresses (comma ',' separated)")
            collaboration_date = col2.date_input("Select a collaboration date")

            if receiver_addresses:
                receiver_addresses = [email.strip() for email in receiver_addresses.split(',') if email.strip()]
                if not sender_email:
                    col2.warning("Please enter your email address.")
                    return

                if col2.button("Add the data", type='primary', use_container_width=True):
                    st.session_state['sender_email'] = sender_email
                    st.session_state['receiver_email'] = receiver_addresses

                    existing_doc = self.collection.find_one({"sender": sender_email})
                    data_to_add = {
                        "sender": sender_email,
                        "team members": receiver_addresses,
                        "date": str(collaboration_date)
                    }

                    try:
                        if existing_doc:
                            self.collection.update_one({"sender": sender_email}, {"$set": data_to_add})
                            col2.success("Document updated successfully!")
                        else:
                            self.collection.insert_one(data_to_add)
                            col2.success("Data successfully added!")
                    except Exception as e:
                        col2.error(f"Error inserting/updating data: {e}")

        if radio_options == "Add Data":
            key = col2.text_input("Enter the heading")
            description = col2.text_area("Enter description for this data")
            col2.subheader("Your Data")
            col2.dataframe(self.data)

            if col2.button("Add data", type='secondary', use_container_width=True):
                if key and description:
                    data = {
                        "key": key,
                        "description": description,
                        "data": self.data.to_dict(orient='records')
                    }
                    try:
                        self.collection.update_one(
                            {"sender": st.session_state['sender_email']},
                            {"$set": {f"data_{st.session_state['count']}": data}},
                            upsert=True
                        )
                        st.session_state['count'] += 1
                        col2.success("Data successfully added!")
                    except Exception as e:
                        col2.error(f"Error updating data: {e}")

        if radio_options == "Send Mails":
            self.send_mails()

    def view(self):
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.session_state['count'] > 1:
                data_keys = [f"data_{x}" for x in range(1, st.session_state['count'])]
                selected_data = st.radio("Added data in DB", data_keys)
            else:
                col1.info("No data available yet.")
                return

        if selected_data:
            with col2:
                try:
                    retrieved_data = self.collection.find_one(
                        {"sender": st.session_state['sender_email']},
                        {selected_data: 1}
                    )
                    if retrieved_data and selected_data in retrieved_data:
                        data_info = retrieved_data[selected_data]
                        col2.subheader(data_info['key'])
                        col2.text(data_info['description'])
                        col2.dataframe(data_info['data'])

                        if col2.button("Delete Data in DB", use_container_width=True, type='primary'):
                            try:
                                self.collection.update_one(
                                    {"sender": st.session_state['sender_email']},
                                    {"$unset": {selected_data: ""}}
                                )
                                col2.success("Data deleted successfully!")
                                st.session_state['count'] -= 1
                            except Exception as e:
                                col2.error(f"Error deleting data: {e}")
                    else:
                        col2.warning("No data found for the selected key.")
                except Exception as e:
                    col2.error(f"Error retrieving data: {e}")

    def send_mails(self):
        team_members = st.session_state['receiver_email']
        st.subheader("Verify Once")
        st.write(team_members)

        smtp_password = st.text_input("Enter your email password", type='password')

        if st.button("Send Mails", type='secondary', use_container_width=True):
            if not smtp_password:
                st.error("Please enter your email password to proceed.")
                return

            try:
                sender_email = st.session_state['sender_email']
                subject = "Collaboration Invitation"
                body = f"Hello, {sender_email} has shared data with you. Please visit the app to view the details."

                smtp_server = "smtp.gmail.com"
                smtp_port = 587

                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, smtp_password)

                    for recipient in team_members:
                        if '@' in recipient and '.' in recipient:
                            email_message = EmailMessage()
                            email_message["From"] = sender_email
                            email_message["To"] = recipient
                            email_message["Subject"] = subject
                            email_message.set_content(body)

                            server.send_message(email_message)

                    st.success("Emails successfully sent!")
            except Exception as e:
                st.error(f"Error sending emails: {e}")
