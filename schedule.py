from db import query, execute

def build_schedule(term="2/2568"):
    # 1) ดึงแผนการสอนจาก DB
    lesson_plans = query("SELECT lesson_plan_id, subject_id, teacher_id, group_id, term FROM lesson_plans WHERE term = %s", (term,))

    if not lesson_plans:
        print("ไม่มี lesson plans ในเทอมนี้")
        return

    max_days = 5
    max_periods = 12

    day = 1
    period = 1

    # 2) ลบตารางเดิมก่อน (กันข้อมูลซ้ำ)
    execute("DELETE FROM table_results WHERE lesson_plan_id IN (SELECT lesson_plan_id FROM lesson_plans WHERE term = %s)", (term,))

    # 3) จัดตารางและบันทึกลง DB
    for plan in lesson_plans:

        # บันทึกลง DB
        execute("""
            INSERT INTO table_results (lesson_plan_id, day, period)
            VALUES (%s, %s, %s)
        """, (plan["lesson_plan_id"], day, period))

        # เลื่อนคาบ
        period += 1

        if period > max_periods:
            period = 1
            day += 1

        # ถ้าวันเกิน 5 → กลับไปวันแรก
        if day > max_days:
            day = 1

    print("ตารางเรียนถูกสร้างสำเร็จ")

print(build_schedule())