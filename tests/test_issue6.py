# -*- coding: utf-8 -*-
"""问题6测试：计划分两张表 正常/伤病；首页带标签区分"""
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
        pg.click(f'.cal-cell[data-date="{today}"]'); pg.wait_for_timeout(200)
        assert pg.is_visible("text=正常训练计划")
        assert pg.is_visible("text=伤病队员训练计划")

        pg.fill("#pt-normal .pt-c >> nth=0", "全队热身")
        pg.fill("#pt-injured .pt-c >> nth=0", "康复慢跑")
        pg.click("#pf-save"); pg.wait_for_timeout(200)

        # 首页今日计划带两个标签
        pg.click('.nav-item[data-view="home"]'); pg.wait_for_timeout(200)
        assert pg.is_visible("text=全队热身")
        assert pg.is_visible("text=康复慢跑")
        row = pg.locator("[data-hp-done]")
        texts = pg.locator("#view-home .memo-item, #view-home .row").all_inner_texts()
        joined = " ".join(texts)
        assert "正常" in joined and "伤病" in joined, joined

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 问题6：正常/伤病分组计划")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
