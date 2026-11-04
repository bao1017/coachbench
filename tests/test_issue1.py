# -*- coding: utf-8 -*-
"""问题1测试：首页只保留计划格，新增测试总览、人员总览"""
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
          state.plans.push({{id:'pl1', date:'{today}', title:'训练', type:'training', peopleIds:[], note:'', done:false, time:''}});
          state.people.push({{id:'p1', kind:'athlete', name:'李强', athlete:{{}}}});
          state.stageRecords.push({{id:'r1', personId:'p1', date:'{today}', metrics:{{m100:13.5}}}});
          save();
        """)
        pg.reload(); pg.wait_for_timeout(300)

        labels = pg.locator(".stat-label").all_inner_texts()
        assert len(labels) == 3, f"首页摘要格不是3个: {labels}"
        assert any("计划" in x for x in labels), labels
        assert any("测试总览" in x for x in labels), labels
        assert any("人员总览" in x for x in labels), labels
        # 旧格子不应存在
        assert not any("课时不足" in x for x in labels), labels
        assert not any("到期的目标" in x for x in labels), labels

        nums = pg.locator(".stat-num").all_inner_texts()
        assert nums[0].strip() == "1", f"今日未完成不对: {nums}"
        assert nums[1].strip() == "1", f"本周已测人数不对: {nums}"
        assert nums[2].strip() == "1", f"在册人数不对: {nums}"

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 问题1：首页三格总览")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
