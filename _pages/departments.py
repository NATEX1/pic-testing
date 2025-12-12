import streamlit as st
import pandas as pd
import db
import time

#fetching data
departments = pd.DataFrame(db.query("SELECT * FROM departments"))


st.title(":red[แผนก]")
st.divider()

with open("preview_data/departments.csv", "rb") as file:
    st.download_button(
        label="ดาวโหลดไฟล์ตัวอย่าง",
        data=file,
        file_name="department.csv",
        mime="text/csv",
        type = "primary"
    )


uploaded_file  = st.file_uploader("", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.table(df)

    if st.button("เพิ่มข้อมูล"):

        for _, row in df.iterrows():
            sql = "INSERT INTO departments(department_id, name) VALUES (%s, %s)"
            db.execute(sql, (row['department_id'], row['name']))
            
        st.success("นำเข้าข้อมูลสำเร็จ")
        time.sleep(1.5)
        st.rerun()

    

# #Filter
filter_df = departments.copy()

col1, col2, col3 = st.columns(3)

# with col1:
    # st.selectbox("ครู", options=filter_df['department_id'].unique())

table = st.data_editor(departments, num_rows="dynamic" , column_config={
    "department_id": st.column_config.TextColumn('รหัสแผนก', required=True),
    "name": st.column_config.TextColumn("แผนก", required=True),
} )

if not table.equals(departments) and st.button('บันทึกการแก้ไข', type="primary"):
    for _, row in table.iterrows():
        old = departments.iloc[_]
        
        if not row.equals(old):
            db.execute("UPDATE departments SET name = %s, WHERE department_id = %s", (row['name'], row['department_id']))
    
    st.success("บันทึกสำเร็จ!")
    time.sleep(1.5)
    st.rerun()