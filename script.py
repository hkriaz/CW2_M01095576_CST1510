import streamlit as st

def page_start():
    if st.session_state.logged_in:
        with st.sidebar:
            st.header("Application menu")
            st.write("You are signed on")
        st.title("You are logged in")
        st.write("Logged in content")

def authenticate_user():
    if username =="hamna" and password =="khan":
        st.session_state.logged_in = True
        st.switch_page("pages/chartDisplay.py")
    else:
        st.write("Login failed. Try again")
        st.session_state.logged_in = False


st.title("WELCOME! 👋")

st.set_page_config(page_title='Baked Goods',
                   #page_icon="img/mdi.jpg"
                    )


with st.expander("Contact Details"):
    st.write("Social Media Link")
    st.write("Contact Number")
with st.sidebar:
    st.button("cookie")
    st.button("brownie")
    st.button("cake")


st.write("top secret recipes :)")
username = st.text_input("Username: ")
password = st.text_input("Password: ", type="password")

if st.button("LOGIN"):
    authenticate_user()

with st.expander("Application Settings"):
    st.write("TEST SCREEN!")
    page_start()
