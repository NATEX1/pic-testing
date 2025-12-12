from ortools.sat.python import cp_model
from db import query, execute

def build_schedule_ai(term="2/2568"):
    # ดึง lesson_plans + ชั่วโมงจาก subjects
    lesson_plans = query("""
        SELECT lp.lesson_plan_id, lp.subject_id, lp.teacher_id, lp.group_id, lp.term, s.hours
        FROM lesson_plans lp
        LEFT JOIN subjects s ON TRIM(lp.subject_id) = TRIM(s.subject_id)
        WHERE lp.term = %s
    """, (term,))

    if not lesson_plans:
        print("ไม่มี lesson plans ในเทอมนี้")
        return

    max_days = 5      # จันทร์-ศุกร์
    max_periods = 12  # 12 คาบต่อวัน
    lunch_period = 5  # คาบ 5 เป็นพักเที่ยง

    model = cp_model.CpModel()

    # สร้างตัวแปร x[lesson_plan_id][day][period] = 1 ถ้าวิชานี้อยู่ slot นั้น
    x = {}
    for plan in lesson_plans:
        lp_id = plan["lesson_plan_id"]
        x[lp_id] = {}
        for d in range(max_days):
            x[lp_id][d] = {}
            for p in range(max_periods):
                if p == lunch_period - 1:
                    continue  # ข้ามพักเที่ยง
                x[lp_id][d][p] = model.NewBoolVar(f"x_{lp_id}_{d}_{p}")

    # constraint: ครบชั่วโมง
    for plan in lesson_plans:
        lp_id = plan["lesson_plan_id"]
        hours = plan["hours"]
        model.Add(sum(x[lp_id][d][p] 
                      for d in range(max_days) 
                      for p in range(max_periods) if p != lunch_period - 1) == hours)

    # constraint: ครูสอนไม่ชนกัน
    for d in range(max_days):
        for p in range(max_periods):
            if p == lunch_period - 1:
                continue
            teachers_in_slot = {}
            for plan in lesson_plans:
                t_id = plan["teacher_id"]
                if t_id not in teachers_in_slot:
                    teachers_in_slot[t_id] = []
                teachers_in_slot[t_id].append(x[plan["lesson_plan_id"]][d][p])
            for t_vars in teachers_in_slot.values():
                model.Add(sum(t_vars) <= 1)

    # constraint: กลุ่มเรียนไม่ชนกัน
    for d in range(max_days):
        for p in range(max_periods):
            if p == lunch_period - 1:
                continue
            groups_in_slot = {}
            for plan in lesson_plans:
                g_id = plan["group_id"]
                if g_id not in groups_in_slot:
                    groups_in_slot[g_id] = []
                groups_in_slot[g_id].append(x[plan["lesson_plan_id"]][d][p])
            for g_vars in groups_in_slot.values():
                model.Add(sum(g_vars) <= 1)

    # solver
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30  # ลดเวลา ถ้า slot เยอะ
    status = solver.Solve(model)

    if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        # ลบตารางเก่า
        execute("""
            DELETE FROM table_results
            WHERE lesson_plan_id IN (SELECT lesson_plan_id FROM lesson_plans WHERE term = %s)
        """, (term,))

        for plan in lesson_plans:
            lp_id = plan["lesson_plan_id"]
            for d in range(max_days):
                for p in range(max_periods):
                    if p == lunch_period - 1:
                        continue
                    if solver.BooleanValue(x[lp_id][d][p]):
                        execute("""
                            INSERT INTO table_results (lesson_plan_id, day, period)
                            VALUES (%s, %s, %s)
                        """, (lp_id, d + 1, p + 1))
        print("ตารางเรียน AI ถูกสร้างสำเร็จ")
    else:
        print("ไม่พบ solution ที่เป็นไปได้")

if __name__ == "__main__":
    build_schedule_ai()
