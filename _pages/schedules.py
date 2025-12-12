import streamlit as st
import db

st.title(":red[ตาราง]")
st.divider()

groups = db.query("SELECT group_id, name FROM groups")
group_options = [g["group_id"] for g in groups]  
group = st.selectbox('เลือกรหัสกลุ่ม', options=group_options)
group_data = db.fetch_one("SELECT * FROM groups WHERE group_id = %s", (group))

file_path = "table.html"

rows = db.query("""
    SELECT 
        tr.day,
        tr.period,
        lp.lesson_plan_id,
        s.name AS subject_name,
        s.subject_id as s_id
    FROM table_results tr
    LEFT JOIN lesson_plans lp 
        ON CAST(tr.lesson_plan_id AS SIGNED) = lp.lesson_plan_id
    LEFT JOIN subjects s 
        ON TRIM(lp.subject_id) = TRIM(s.subject_id)
    WHERE TRIM(lp.group_id) = %s
    ORDER BY tr.day, tr.period;
    """
, (group,))

# แปลง day = ตัวเลข → ชื่อวัน
day_map = {
    1: "จันทร์",
    2: "อังคาร",
    3: "พุธ",
    4: "พฤหัส",
    5: "ศุกร์"
}

# เตรียม table_data
table_data = {
    "จันทร์": {i: "" for i in range(1, 13)},
    "อังคาร": {i: "" for i in range(1, 13)},
    "พุธ": {i: "" for i in range(1, 13)},
    "พฤหัส": {i: "" for i in range(1, 13)},
    "ศุกร์": {i: "" for i in range(1, 13)},
}

# ใส่ข้อมูลลงช่องตาราง
for r in rows:
    day_num = int(r["day"])
    day = day_map.get(day_num)
    period = int(r["period"])

    # ข้ามพักเที่ยง
    if period == 5:
        table_data[day][period] = "พักเที่ยง"
        continue

    if day in table_data and period in table_data[day]:
        table_data[day][period] = f"""
        {r["subject_name"]} <br />
        {r["s_id"]}
        """ or "-"

# โหลด HTML template
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# mapping สำหรับ placeholder เช่น mon1, mon2
short_map = {
    "จันทร์": "mon",
    "อังคาร": "tue",
    "พุธ": "wed",
    "พฤหัส": "thu",
    "ศุกร์": "fri",
}

# แทนที่ placeholder
for day in table_data:
    short = short_map[day]

    for period in table_data[day]:
        placeholder = f"{{{{{short}{period}}}}}"
        html = html.replace(placeholder, table_data[day][period])
        
subjects = db.query("""
    SELECT DISTINCT s.name AS subject_name, s.subject_id AS subject_code, s.t_p_c
    FROM lesson_plans lp
    LEFT JOIN subjects s ON TRIM(lp.subject_id) = TRIM(s.subject_id)
    WHERE TRIM(lp.group_id) = %s
    ORDER BY s.subject_id
""", (group,))

# เตรียม list ของ placeholder sub1-sub14
sub_placeholders = [f"sub{i}" for i in range(1, 15)]

for i, placeholder in enumerate(sub_placeholders):
    if i < len(subjects):
        sub_text = f"({subjects[i]['subject_code']}) {subjects[i]['subject_name']} ({subjects[i]['t_p_c']})"
    else:
        sub_text = ""
    html = html.replace(f"{{{{{placeholder}}}}}", sub_text)

html = html.replace(f"{{{{{"term"}}}}}", "2/2568")
html = html.replace(f"{{{{{"group_id"}}}}}", group)
html = html.replace(f"{{{{{"group_name"}}}}}", group_data["name"])

st.components.v1.html(html, height=600)
