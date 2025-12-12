import streamlit as st
import pandas as pd
import altair as alt

import db

st.title(":red[หน้าหลัก]")
st.divider()

#fetching data
students = pd.DataFrame(db.query("""SELECT s.*, g.department_id as g_department_id,s.group_id as s_group_id, d.name as d_name  FROM students s LEFT JOIN groups g ON s.group_id = g.group_id LEFT JOIN departments d ON g.department_id = d.department_id"""))


teachers = pd.DataFrame(db.query("SELECT * FROM teachers"))
classrooms = pd.DataFrame(db.query("SELECT * FROM classrooms"))
departments = pd.DataFrame(db.query("SELECT * FROM departments"))
subjects = pd.DataFrame(db.query("SELECT * FROM subjects"))
groups = pd.DataFrame(db.query("SELECT * FROM groups"))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("นักศึกษาทั้งหมด", len(students), border=1)

with col2:
    st.metric("นักศึกษาทั้งหมด", len(students), border=1)

with col3:
    st.metric("ห้องเรียนทั้งหมด", len(classrooms), border=1)

with col1:
    st.metric("วิชาทั้งหมด", len(subjects), border=1)

with col2:
    st.metric("กลุ่มการเรียนทั้งหมด", len(groups), border=1)

# นับจำนวน student ตาม department และ group
count_df = students.groupby(['g_department_id', 'd_name', 's_group_id']).size().reset_index(name='count')

# หาลำดับ department ตามจำนวนรวม (มากไปน้อย)
dept_order = count_df.groupby(['g_department_id', 'd_name'])['count'].sum().reset_index()
dept_order = dept_order.sort_values('count', ascending=False)['d_name'].tolist()

# นับจำนวน student ตามแผนก (สำหรับ Pie)
dept_count = students.groupby('d_name').size().reset_index(name='count')
dept_count = dept_count.sort_values('count', ascending=False)

# === Bar Chart ===
bar_chart = alt.Chart(count_df).mark_bar(size=20).encode(
    x=alt.X('d_name:N',
            sort=dept_order,
            title='แผนก',
            ),
    xOffset=alt.XOffset('s_group_id:N'),
    y=alt.Y('count:Q',
            title='จำนวนนักเรียน'),
    color=alt.Color('d_name:N',
                    title='แผนก',
                    scale=alt.Scale(scheme='tableau10')),
    tooltip=[
        alt.Tooltip('d_name:N', title='แผนก'),
        alt.Tooltip('s_group_id:N', title='กลุ่ม'),
        alt.Tooltip('count:Q', title='จำนวนนักเรียน')
    ]
).properties(
    height=400,
    title='จำนวนนักเรียนแยกตามแผนกและกลุ่ม'
)

# === Pie Chart ===
pie_chart = alt.Chart(dept_count).mark_arc(innerRadius=0).encode(
    theta=alt.Theta('count:Q'),
    color=alt.Color('d_name:N',
                    title='แผนก',
                    scale=alt.Scale(scheme='tableau10')),
    tooltip=[
        alt.Tooltip('d_name:N', title='แผนก'),
        alt.Tooltip('count:Q', title='จำนวนนักเรียน')
    ]
).properties(
    height=400,
    title=alt.TitleParams(
        text='สัดส่วนนักเรียนตามแผนก',
        anchor='middle',
        orient='top'
)
)


# === วางข้างกัน 2/3 : 1/3 ===
col1, col2 = st.columns([2, 1])

with col1:
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    st.altair_chart(pie_chart, use_container_width=True)