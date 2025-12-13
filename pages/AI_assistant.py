import streamlit as st
from google import genai

# Page configuration
st.set_page_config(page_title='CST1510 CW2', page_icon="img/mdi.jpg")
st.title("ASK ME ANYTHING")

# Retrieve the private key from Streamlit secrets
api_key = st.secrets["GOOGLE_API_KEY"]

# Initialise the Gemini client with the hidden key
client = genai.Client(api_key=api_key)

# User query
query = st.text_input("Enter your query:")

# Generate the response (only if a query was entered)
if query:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query
    )
    st.write(response.text)
