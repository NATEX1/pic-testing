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
            st.Page("_pages/departments.py"),
            st.Page("_pages/subjects.py"),
            st.Page("_pages/classrooms.py"),
            st.Page("_pages/groups.py"),
            st.Page("_pages/schedules.py"),
            st.Page("_pages/study_plans.py"),
            st.Page("_pages/lesson_plans.py")

        ]
        pg = st.navigation(pages, position="hidden")
        pg.run()
        
        with st.sidebar:
            st.page_link(st.Page("_pages/home.py"), label="หน้าแรก",  icon=":material/home:")
            st.page_link(st.Page("_pages/students.py"), label="นักศึกษา",  icon=":material/groups_3:")
            st.page_link(st.Page("_pages/teachers.py"), label="ครู",  icon=":material/people:")
            st.page_link(st.Page("_pages/departments.py"), label="แผนก",  icon=":material/domain:")
            st.page_link(st.Page("_pages/subjects.py"), label="วิชา",  icon=":material/book:")
            st.page_link(st.Page("_pages/classrooms.py"), label="ห้องเรียน",  icon=":material/door_front:")
            st.page_link(st.Page("_pages/groups.py"), label="กลุ่ม",  icon=":material/groups:")
            st.page_link(st.Page("_pages/schedules.py"), label="ตาราง",  icon=":material/table:")
            st.page_link(st.Page("_pages/study_plans.py"), label="แผนการเรียน",  icon=":material/school:")
            st.page_link(st.Page("_pages/lesson_plans.py"), label="แผนการสอน",  icon=":material/dictionary:")
