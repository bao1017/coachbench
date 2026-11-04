# -*- coding: utf-8 -*-
"""阶段2测试：日历点日期弹表格、保存、翻月"""
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

        pg.click('.nav-item[data-view="calendar"]')
        pg.wait_for_timeout(150)
        today = datetime.date.today().isoformat()
        pg.click(f'.cal-cell[data-date="{today}"]')
        pg.wait_for_timeout(150)
        pg.fill("#pt-normal .pt-c >> nth=0", "下午带短跑组跑间歇")
        pg.click("#pf-save")
        pg.wait_for_timeout(200)
        assert "1" in pg.locator(f'.cal-cell[data-date="{today}"] .mark').inner_text()

        # 翻月按钮
        pg.click("#cal-prev"); pg.wait_for_timeout(100)
        pg.click("#cal-next"); pg.wait_for_timeout(100)
        pg.click("#cal-today"); pg.wait_for_timeout(100)

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 阶段2：日历表格计划")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
