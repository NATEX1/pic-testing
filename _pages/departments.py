import streamlit as st
import pandas as pd
import db

#fetching data
departments = pd.DataFrame(db.query("SELECT * FROM departments"))


st.title(":red[แผนก]")
st.divider()

uploaded_file  = st.file_uploader("", type = ["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.table(df)

    if st.button("เพิ่มข้อมูล"):

        df = pd.read_csv(uploaded_file)

        for rows in df.iterrows():




    st.success("เพิ่มข้อมูลเสร็จสิ้น")

# #Filter
# filter_df = teachers.copy()
#
# col1, col2, col3 = st.columns(3)
#
# with col1:
#     st.selectbox("ครู", options=filter_df['teacher_id'])

table = st.data_editor(departments, num_rows="dynamic" , column_config={
    "department_id": st.column_config.TextColumn('รหัสแผนก', required=True),
    "name": st.column_config.TextColumn("แผนก", required=True),
} )

if table

