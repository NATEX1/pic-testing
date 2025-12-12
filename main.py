import streamlit as st
from streamlit_cookies_controller import CookieController

controller = CookieController()

if not (controller.get('username') and controller.get('role')):
    
    tab1, tab2, tab3 = st.tabs(["นักศึกษา", "อาจารย์", "ผุ้ดูแล"])
    

else: 
    
    if controller.get("role") and controller.get("role") == "admin":
        
        pages = [
            
        ]
        pg = st.navigation(pages)
        pg.run()
