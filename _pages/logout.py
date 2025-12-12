import streamlit as st
from streamlit_cookies_controller import CookieController
import time

controller = CookieController()

if st.button("ออกจากระบบ", type="primary"):
    controller.remove("username")
    controller.remove("role")
    
    st.success("ออกจากระบบเสร็จสิน กรุณารีเฟรช")
