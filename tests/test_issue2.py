# -*- coding: utf-8 -*-
"""问题2测试：计划弹窗去掉标题/类型/关联人员，备注改计划；当天列表是表格"""
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
        pg.evaluate("localStorage.removeItem('coachbench-v1'); location.reload();")
        pg.wait_for_timeout(300)
        pg.click('.nav-item[data-view="calendar"]'); pg.wait_for_timeout(150)
        pg.click("#plan-add"); pg.wait_for_timeout(150)

        # 旧字段应不存在，新字段存在
        assert pg.locator("#f-title").count() == 0, "标题字段还在"
        assert pg.locator("#f-type").count() == 0, "类型字段还在"
        assert pg.locator(".ppl-cb").count() == 0, "关联人员还在"
        assert pg.locator("#f-plan").count() == 1, "没有'计划'输入框"

        today = datetime.date.today().isoformat()
        pg.fill("#f-date", today)
        pg.fill("#f-time", "17:00")
        pg.fill("#f-plan", "带队员练起跑")
        pg.click("#pf-save"); pg.wait_for_timeout(200)

        # 当天列表是表格且内容在
        table = pg.locator("#view-calendar table")
        assert table.count() == 1, "当天安排不是表格形式"
        assert pg.is_visible("text=带队员练起跑"), "新加计划没出现"

        # 日历格子变高
        h = pg.locator(".cal-cell").first.evaluate("e => e.offsetHeight")
        assert h >= 120, f"日历格子不够高: {h}"

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 问题2：计划表单精简+表格列表")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
