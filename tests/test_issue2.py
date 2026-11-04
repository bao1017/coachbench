# -*- coding: utf-8 -*-
"""问题2回归：计划弹窗里不再有标题/类型/关联人员；日历格加高"""
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

        today = datetime.date.today().isoformat()
        pg.click(f'.cal-cell[data-date="{today}"]'); pg.wait_for_timeout(150)
        assert pg.locator("#f-title").count() == 0, "标题字段还在"
        assert pg.locator("#f-type").count() == 0, "类型字段还在"
        assert pg.locator(".ppl-cb").count() == 0, "关联人员还在"

        h = pg.locator(".cal-cell").first.evaluate("e => e.offsetHeight")
        assert h >= 120, f"日历格子不够高: {h}"

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 问题2回归：精简表单+高日历")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
