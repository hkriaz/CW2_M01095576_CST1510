import streamlit as st

st.set_page_config(page_title='Home')

st.header("Home Page")
st.write("Choose which dashboard you want to be redirected to:")

if st.button("Cyber Incidents"):
    st.switch_page("pages/incidents_dashboard.py")
if st.button("Datasets Metadata"):
    st.switch_page("pages/datasets_dashboard.py")
if st.button("It tickets"):
    st.switch_page("pages/tickets_dashboard.py")
if st.button("AI Assistant"):
    st.switch_page("pages/AI_assistant.py")
