import streamlit as st
from google import genai

st.set_page_config(page_title='CST1510 CW2')
st.title("ASK ME ANYTHING")

client = genai.Client(api_key="AIzaSyA9jO0XEesIeNLdpNVa3OmqOVjPnq-Fm3s")
query = st.text_input("Enter your query:")
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=query
)
st.write(response.text)
