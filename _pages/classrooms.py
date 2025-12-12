import streamlit as st
import pandas as pd
from altair.theme import options

import db
import time

# fetching data
classrooms = pd.DataFrame(db.query("SELECT * FROM classrooms"))

st.title(":red[ห้องเรียน]")
st.divider()

with open("preview_data/classrooms.csv", "rb") as file:
    st.download_button(
        label="ดาวโหลดไฟล์ตัวอย่าง",
        data=file,
        file_name="classroom.csv",
        mime="text/csv",
        type="primary"
    )

uploaded_file = st.file_uploader("", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.table(df)

    if st.button("เพิ่มข้อมูล"):

        for _, row in df.iterrows():
            sql = "INSERT INTO classrooms(classroom_id, name) VALUES (%s, %s)"
            db.execute(sql, (row['classroom_id'], row['name']))

        st.success("นำเข้าข้อมูลสำเร็จ")
        time.sleep(1.5)
        st.rerun()

# #Filter
filter_df = classrooms.copy()

col1, col2, col3 = st.columns(3)

# with col1:
# st.selectbox("ครู", options=filter_df['classroom_id'].unique())

table = st.data_editor(classrooms, num_rows="dynamic", column_config={
    "classroom_id": st.column_config.NumberColumn('รหัสห้องเรียน', required=True),
    "name": st.column_config.TextColumn("ห้องเรียน", required=True),
    "type": st.column_config.SelectboxColumn("ประเภท", required=True, options=['ห้องเรียน','ห้องปฏิบัติการ','อาคารอเนกประสงค์']),
    "capacity": st.column_config.NumberColumn("ความจุห้อง", required=True, min_value=0),
})

if not table.equals(classrooms) and st.button('บันทึกการแก้ไข', type="primary"):
    for _, row in table.iterrows():
        old = classrooms.iloc[_]

        if not row.equals(old):
            db.execute("UPDATE `classrooms` SET `classroom_id`='[value-1]',`name`='[value-2]',`type`='[value-3]',`capacity`='[value-4]' WHERE `classroom_id`='[value-1]'"
                       (row['name'], row['classroom_id']))

    st.success("บันทึกสำเร็จ!")
    time.sleep(1.5)
    st.rerun()