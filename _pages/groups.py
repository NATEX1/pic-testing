import streamlit as st
import pandas as pd
import db
import time

# fetching data
groups = pd.DataFrame(db.query("SELECT g.group_id as g_group_id, g.name as g_name, d.name as d_name, g.department_id as g_department_id FROM groups g LEFT JOIN departments d ON g.department_id = d.department_id"))
departments = pd.DataFrame(db.query("SELECT * FROM departments"))

st.title(":red[กลุ่ม]")
st.divider()

with open("preview_data/groups.csv", "rb") as file:
    st.download_button(
        label="ดาวโหลดไฟล์ตัวอย่าง",
        data=file,
        file_name="group.csv",
        mime="text/csv",
        type="primary"
    )

uploaded_file = st.file_uploader("", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.table(df)

    if st.button("เพิ่มข้อมูล"):

        for _, row in df.iterrows():
            sql = "INSERT INTO groups(group_id, name) VALUES (%s, %s)"
            db.execute(sql, (row['group_id'], row['name']))

        st.success("นำเข้าข้อมูลสำเร็จ")
        time.sleep(1.5)
        st.rerun()

# #Filter
filter_df = groups.copy()

col1, col2, col3 = st.columns(3)

# with col1:
# st.selectbox("ครู", options=filter_df['group_id'].unique())

table = st.data_editor(groups, num_rows="dynamic", column_order=["g_group_id", "g_name", "g_department_id", "d_name"], column_config={
    "g_group_id": st.column_config.TextColumn('รหัสกลุ่ม', required=True),
    "g_name": st.column_config.TextColumn("กลุ่ม", required=True),
    "g_department_id": st.column_config.TextColumn("รหัสแผนก", required=True),
    "d_name": st.column_config.SelectboxColumn("แผนก", options=departments['name'].tolist(), required=True),

})

if not table.equals(groups) and st.button('บันทึกการแก้ไข', type="primary"):
    for _, row in table.iterrows():
        old = groups.iloc[_]

        if not row.equals(old):
            db.execute("UPDATE groups SET name = %s, WHERE group_id = %s",
                       (row['name'], row['group_id']))

    st.success("บันทึกสำเร็จ!")
    time.sleep(1.5)
    st.rerun()