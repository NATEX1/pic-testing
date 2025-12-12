import streamlit as st
from streamlit_cookies_controller import CookieController
import db
import time

controller = CookieController()

if not (controller.get('username') and controller.get('role')):
    
    st.header("เข้าสู่ระบบ")
    
    tab1, tab2, tab3 = st.tabs(["นักศึกษา", "อาจารย์", "ผุ้ดูแล"])
    
    with tab3:
        
        with st.form('admin_form'):
            username = st.text_input(label='ชื่อผู้ใช้')
            password = st.text_input(label='รหัสผ่าน')
            
            if st.form_submit_button('เข้าสู่ระบบ', type="primary"):
                if username == "admin" and password == "123456":
                    controller.set("username", "admin")
                    controller.set("role", "admin")
                    
                    time.sleep(1.5)
                    st.rerun()
                    
                    
else: 
    
    if controller.get("role") and controller.get("role") == "admin":
        
        pages = [
            st.Page("_pages/home.py"),
            st.Page("_pages/students.py"),
            st.Page("_pages/teachers.py"),

        ]
        pg = st.navigation(pages, position="hidden")
        pg.run()
        
        with st.sidebar:
            st.page_link(st.Page("_pages/home.py"), label="หน้าแรก",  icon=":material/home:")
            st.page_link(st.Page("_pages/students.py"), label="นักศึกษา",  icon=":material/people:")
            st.page_link(st.Page("_pages/teachers.py"), label="ครู",  icon=":material/people:")


