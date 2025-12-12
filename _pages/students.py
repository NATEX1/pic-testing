import streamlit as st
import pandas as pd

import db
import time

# fetching data
students = pd.DataFrame(db.query("SELECT * FROM students"))
groups = pd.DataFrame(db.query("SELECT * FROM groups"))

st.title(":red[นักเรียน]")
st.divider()

with open("preview_data/students.csv", "rb") as file:
    st.download_button(
        label="ดาวโหลดไฟล์ตัวอย่าง",
        data=file,
        file_name="student.csv",
        mime="text/csv",
        type="primary"
    )

uploaded_file = st.file_uploader("", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.table(df)

    if st.button("เพิ่มข้อมูล"):

        for _, row in df.iterrows():
            sql= "INSERT INTO `students`(`id_card`, `student_id`, `group_id`, `grade`, `prefix`, `firstname`, `lastname`, `status`) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"
            db.execute(sql, (row['id_card'], row['student_id'], row['group_id'], row['grade'], row['prefix'], row['firstname'], row['lastname'], row['status']))

        st.success("นำเข้าข้อมูลสำเร็จ")
        time.sleep(1.5)
        st.rerun()

# #Filter
filter_df = students.copy()

col1, col2, col3 = st.columns(3)

# with col1:
# st.selectbox("ครู", options=filter_df['student_id'].unique())

table = st.data_editor(students, num_rows="dynamic", column_config={
    "student_id": st.column_config.TextColumn('รหัสนักเรียน', required=True),
    "prefix": st.column_config.SelectboxColumn("คำนำหน้า", required=True, options=['นาย','นาง','นางสาว']),
    "firstname": st.column_config.TextColumn("ชื่อ", required=True),
    "lastname": st.column_config.TextColumn("นามสกุล", required=True),
    "group_id": st.column_config.SelectboxColumn("กลุ่มการเรียน", required=True, options=groups['group_id'].tolist()),
    "grade": st.column_config.SelectboxColumn("ชั้น", required=True, options=['ปวช.1/1','ปวช.1/2','ปวช.2/1','ปวช.2/2','ปวช.3/1','ปวช.3/2']),
    "status": st.column_config.SelectboxColumn("สถานะ", required=True,
                                              options=['กำลังศึกษา','พ้นสภาพ','พักการเรียน','ลาออกจากสถานศึกษา']),

})

if not table.equals(students) and st.button('บันทึกการแก้ไข', type="primary"):
    for _, row in table.iterrows():
        old = students.iloc[_]

        if not row.equals(old):
            db.execute("UPDATE `students` SET `id_card`= %s,`student_id`= %s,`group_id`= %s,`grade`= %s,`prefix`= %s,`firstname`= %s,`lastname`= %s,`status`= %s WHERE `student_id` = %s",
                       (row['id_card'], row['student_id'], row['group_id'], row['grade'], row['prefix'], row['firstname'], row['lastname'], row['status'], row['student_id']))

    st.success("บันทึกสำเร็จ!")
    time.sleep(1.5)
    st.rerun()