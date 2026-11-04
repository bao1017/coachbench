# -*- coding: utf-8 -*-
"""阶段5测试：首页今日计划/备忘/四个摘要格联动"""
import sys, datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = Path(r"C:\Users\陈硕腾\Desktop\app\工作生活工作台.html")

def main():
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(HTML.as_uri())
        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        today = datetime.date.today()
        yest = (today - datetime.timedelta(days=1)).isoformat()
        today = today.isoformat()

        # 造数据：今天一条未完成计划、昨天一条逾期计划、一个剩3节课的学员
        pg.evaluate(f"""
          state.plans.push({{id:'pl1', date:'{today}', title:'今天带训练', type:'training', peopleIds:[], note:'', done:false, time:'16:00'}});
          state.plans.push({{id:'pl2', date:'{yest}', title:'昨天忘了的事', type:'work', peopleIds:[], note:'', done:false, time:''}});
          state.people.push({{id:'pp1', kind:'student', name:'王同学', student:{{remainingClasses:3}}}});
          save();
        """)
        pg.reload(); pg.wait_for_timeout(300)

        # 今日计划出现
        assert pg.is_visible("text=今天带训练"), "首页没显示今天的计划"
        # 逾期
        assert pg.is_visible("text=昨天忘了的事"), "逾期计划没显示"
        # 摘要格：今天未完成 1、本周已测 0、在册人数 1
        nums = pg.locator(".stat-num").all_inner_texts()
        assert nums[0].strip()=="1", f"今日未完成数不对: {nums}"
        assert nums[1].strip()=="0", f"本周已测人数不对: {nums}"
        assert nums[2].strip()=="1", f"在册人数不对: {nums}"

        # 备忘：输入回车贴上
        pg.fill("#memo-input", "下午给家长回电话")
        pg.press("#memo-input", "Enter")
        pg.wait_for_timeout(200)
        assert pg.is_visible("text=下午给家长回电话"), "备忘没贴上"

        # 勾选计划完成 → 摘要数字变 0
        pg.check("[data-hp-done='pl1']")
        pg.wait_for_timeout(200)
        nums = pg.locator(".stat-num").all_inner_texts()
        assert nums[0].strip()=="0", f"勾选后今日未完成没归零: {nums}"

        # 刷新后备忘还在
        pg.reload(); pg.wait_for_timeout(300)
        assert pg.is_visible("text=下午给家长回电话"), "刷新后备忘丢了"

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 阶段5：首页联动")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
