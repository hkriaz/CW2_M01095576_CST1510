import streamlit as st
from app.services.user_services import register_user, login_user, migrate_users_from_file

st.set_page_config(page_title='CST1510 CW2'
                    )

def demo_authentication():
    st.subheader("Authentication")

    with st.expander("Sign up"):
        username = st.text_input("Username", key="reg_user")
        password = st.text_input("Password", type="password", key="reg_pass")
        role = st.selectbox("Role", ["analyst", "admin"], key="reg_role")
        if st.button("Register User"):
            success, msg = register_user(username, password, role)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    with st.expander("Login"):
        login_user_input = st.text_input("Username", key="login_user")
        login_pass_input = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            success, msg = login_user(login_user_input, login_pass_input)
            if success:
                st.success(msg)
                st.switch_page("pages/home.py")
            else:
                st.error(msg)


demo_authentication()
