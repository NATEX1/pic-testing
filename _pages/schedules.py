import streamlit as st

st.title(":red[ตาราง]")
st.divider()

file_path = "table.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()
    
st.components.v1.html(html, height=800)