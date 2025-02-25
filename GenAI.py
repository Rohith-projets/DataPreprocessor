import streamlit as st
import pandas as pd
import openai
import json

class GenAI:
    def __init__(self, df):
        self.dataset = df

    def query_openai(self, question,apiKey):
        """Uses OpenAI GPT to answer questions about the dataset."""
        openai.api_key = apiKey

        # Convert dataset to a JSON-like format for better AI understanding
        data_sample = self.dataset.head(5).to_json()  # Send only first 5 rows to avoid large payloads

        prompt = f"""
        You are an expert data analyst. Given the following dataset (in JSON format):

        {data_sample}

        Answer the following user query in a concise and insightful way:
        "{question}"
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" for a cheaper alternative
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                          {"role": "user", "content": prompt}],
                temperature=0.5
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"

    def display(self):
        st.subheader("Your Question Here?", divider='blue')
        question = st.text_area("Enter your question about the dataset:")
        apiKey=st.text_input("Enter Your Own API Key Here")
        
        if question:
            st.subheader("Your Answer Here", divider='blue')
            answer = self.query_openai(question,apiKey)
            st.markdown(answer)
