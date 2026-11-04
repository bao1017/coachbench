# -*- coding: utf-8 -*-
"""阶段5测试：首页今日计划/备忘/摘要格联动"""
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
        today = datetime.date.today().isoformat()

        pg.evaluate(f"""
          state.plans.push({{id:'pl1', date:'{today}', title:'今天带训练', type:'training', peopleIds:[], note:'', done:false, time:'16:00', group:'normal'}});
          state.people.push({{id:'pp1', kind:'athlete', name:'王队员', athlete:{{}}}});
          save();
        """)
        pg.reload(); pg.wait_for_timeout(300)

        assert pg.is_visible("text=今天带训练"), "首页没显示今天的计划"
        nums = pg.locator(".stat-num").all_inner_texts()
        assert nums[0].strip()=="1", f"今日未完成数不对: {nums}"
        assert nums[2].strip()=="1", f"在册人数不对: {nums}"

        pg.fill("#memo-input", "下午给家长回电话")
        pg.press("#memo-input", "Enter")
        pg.wait_for_timeout(200)
        assert pg.is_visible("text=下午给家长回电话"), "备忘没贴上"

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
