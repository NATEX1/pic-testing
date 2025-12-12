import streamlit as st
import pandas as pd
import db
import time

# fetching data
subjects = pd.DataFrame(db.query("SELECT * FROM subjects"))

st.title(":red[แผนก]")
st.divider()

with open("preview_data/subjects.csv", "rb") as file:
    st.download_button(
        label="ดาวโหลดไฟล์ตัวอย่าง",
        data=file,
        file_name="subjects.csv",
        mime="text/csv",
        type="primary"
    )

uploaded_file = st.file_uploader("", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.table(df)

    if st.button("เพิ่มข้อมูล"):

        for _, row in df.iterrows():
            # เพิ่ม d_name ใน INSERT statement
            sql = "INSERT INTO `subjects`(`subject_id`, `name`, `t_p_c`, `d_name`) VALUES (%s, %s, %s, %s)"
            db.execute(sql, (row['department_id'], row['name'], row['t_p_c'], row['d_name']))

        st.success("นำเข้าข้อมูลสำเร็จ")
        time.sleep(1.5)
        st.rerun()

# #Filter
filter_df = subjects.copy()

col1, col2, col3 = st.columns(3)

# with col1:
# st.selectbox("ครู", options=filter_df['department_id'].unique())

table = st.data_editor(subjects, num_rows="dynamic", column_config={
    "department_id": st.column_config.TextColumn('รหัสแผนก', required=True),
    "name": st.column_config.TextColumn("แผนก", required=True),
})

if not table.equals(subjects) and st.button('บันทึกการแก้ไข', type="primary"):
    for _, row in table.iterrows():
        old = subjects.iloc[_]

        if not row.equals(old):
            db.execute("UPDATE subjects SET name = %s, t_p_c = %s WHERE subject_id = %s",
                       (row['name'], row['t_p_c'], row['subject_id']))

    st.success("บันทึกสำเร็จ!")
    time.sleep(1.5)
    st.rerun()