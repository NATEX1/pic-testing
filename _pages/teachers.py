import streamlit as st
import pandas as pd

import db
import time

# fetching data
teachers = pd.DataFrame(db.query("SELECT * FROM teachers"))
groups = pd.DataFrame(db.query("SELECT * FROM groups"))

st.title(":red[ครู]")
st.divider()

with open("preview_data/teachers.csv", "rb") as file:
    st.download_button(
        label="ดาวโหลดไฟล์ตัวอย่าง",
        data=file,
        file_name="teacher.csv",
        mime="text/csv",
        type="primary"
    )

uploaded_file = st.file_uploader("", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.table(df)

    if st.button("เพิ่มข้อมูล"):

        for _, row in df.iterrows():
            sql= "INSERT INTO `teachers`(`teacher_id`, `prefix`, `firstname`, `lastname`, `position`, `hours_per_week`, `id_card`, `classroom_id`, `department_id`) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)"
            db.execute(sql, (row['teacher_id'], row['prefix'], row['firstname'], row['lastname'], row['position'], row['hours_per_week'], row['id_card'], row['classroom_id'], row['department_id']))

        st.success("นำเข้าข้อมูลสำเร็จ")
        time.sleep(1.5)
        st.rerun()

# #Filter
filter_df = teachers.copy()

col1, col2, col3 = st.columns(3)

# with col1:
# st.selectbox("ครู", options=filter_df['teacher_id'].unique())

table = st.data_editor(teachers, num_rows="dynamic", column_config={
    "teacher_id": st.column_config.TextColumn('รหัสครู', required=True),
    "prefix": st.column_config.SelectboxColumn("คำนำหน้า", required=True, options=['นาย','นาง','นางสาว']),
    "firstname": st.column_config.TextColumn("ชื่อ", required=True),
    "lastname": st.column_config.TextColumn("นามสกุล", required=True),
    "position": st.column_config.TextColumn("ตำแหน่ง", required=True),
    "hours_per_weeks": st.column_config.NumberColumn("ชั่วโมงสอนต่อสัปดาห์", required=True, min_value=1),
    "id_card": st.column_config.TextColumn("บัตรประชาชน", required=True, max_chars=13),
    "classroom_id": st.column_config.NumberColumn("รหัสห้องเรียน", required=True),
    "department_id": st.column_config.TextColumn("รหัสแผนก", required=True, max_chars=5),
})

if not table.equals(teachers) and st.button('บันทึกการแก้ไข', type="primary"):
    for _, row in table.iterrows():
        old = teachers.iloc[_]

        if not row.equals(old):
            db.execute("UPDATE `teachers` SET `teacher_id`=%s,`prefix`= %s,`firstname`= %s,`lastname`= %s,`position`= %s,`hours_per_week`= %s,`id_card`= %s,`classroom_id`= %s,`department_id`= %s, WHERE `teacher_id` = %s",
                       (row['teacher_id'], row['prefix'], row['firstname'], row['lastname'], row['position'], row['hours_per_week'], row['id_card'], row['classroom_id'], row['department_id'],row['teacher_id']))
    st.success("บันทึกสำเร็จ!")
    time.sleep(1.5)
    st.rerun()