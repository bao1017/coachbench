# -*- coding: utf-8 -*-
"""问题5测试：加计划=弹窗表格；点日历格直接弹窗"""
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
        today = datetime.date.today().isoformat()

        pg.click('.nav-item[data-view="calendar"]'); pg.wait_for_timeout(150)
        pg.click(f'.cal-cell[data-date="{today}"]')
        pg.wait_for_timeout(200)
        assert pg.is_visible("#overlay")
        assert pg.locator("#pt-normal .pt-c").count() >= 1
        for label in ["内容","次数","组数","强度"]:
            assert pg.locator(f"th:text('{label}')").count() >= 1

        pg.fill("#pt-normal .pt-c >> nth=0", "起跑练习")
        pg.click('.pt-add[data-g="normal"]'); pg.wait_for_timeout(100)
        pg.fill("#pt-normal .pt-c >> nth=1", "加速跑")
        pg.click("#pf-save"); pg.wait_for_timeout(200)

        mark = pg.locator(f'.cal-cell[data-date="{today}"] .mark')
        assert "2" in mark.inner_text(), mark.inner_text()

        pg.click('.nav-item[data-view="home"]'); pg.wait_for_timeout(200)
        assert pg.is_visible("text=起跑练习")
        assert pg.is_visible("text=加速跑")
        joined = pg.inner_text("#view-home")
        assert "正常" in joined

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 问题5：计划弹窗表格")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
