import streamlit as st
import pandas as pd
import db

#fetching data
teachers = pd.DataFrame(db.query("SELECT * FROM teachers"))
classrooms = pd.DataFrame(db.query("SELECT * FROM classrooms"))
departments = pd.DataFrame(db.query("SELECT * FROM departments"))


st.title(":red[ครู]")
st.divider()

file_upload = st.file_uploader("เพิ่มข้อมูล", type = ["csv", "xlsx"])

if file_upload and st.button("เพิ่มข้อมูล"):
    st.success("เพิ่มข้อมูลเสร็จสิ้น")

# #Filter
# filter_df = teachers.copy()
#
# col1, col2, col3 = st.columns(3)
#
# with col1:
#     st.selectbox("ครู", options=filter_df['teacher_id'])

table = st.data_editor(teachers, num_rows="dynamic" , column_config={
    "teacher_id": st.column_config.TextColumn('รหัสครู', required=True),
    "prefix": st.column_config.SelectboxColumn("คำนำหน้า", options=['นาย','นาง','นางสาว'], required=True),
    "firstname": st.column_config.TextColumn("ชื่อ", required=True),
    "lastname": st.column_config.TextColumn("นามสกุล", required=True),
    "position": st.column_config.TextColumn("ตำแหน่ง", required=True),
    "hours_per_week": st.column_config.NumberColumn("ชั่วโมงสอนต่อสัปดาห์", required=True, max_value=28),
    "id_card": st.column_config.TextColumn("รหัสบัตรประชาชน", required=True, max_chars=13),
    "classroom_id": st.column_config.SelectboxColumn("ห้องประจำ", required=True, options=classrooms['classroom_id'].tolist()),
    "deparment_id": st.column_config.SelectboxColumn("แผนก", required=True, options=departments['deparment_id'].tolist()),
} )



