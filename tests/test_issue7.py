# -*- coding: utf-8 -*-
"""问题7测试：阶段数据记录可删除（带确认）"""
import sys
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

        pg.click('.nav-item[data-view="people"]'); pg.wait_for_timeout(150)
        pg.click("#ppl-add"); pg.wait_for_timeout(150)
        pg.fill("#pf-name", "测试队员")
        pg.click("#pfc-save"); pg.wait_for_timeout(200)
        pg.click('[data-person]'); pg.wait_for_timeout(200)

        pg.click("#rec-add"); pg.wait_for_timeout(150)
        pg.fill("#rf-m100", "13.5")
        pg.click("#rf-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=100米 13.5s"), "记录没加上"

        # 删除：先取消
        pg.click("[data-rec-del]"); pg.wait_for_timeout(150)
        pg.click("#cf-no"); pg.wait_for_timeout(150)
        assert pg.evaluate("state.stageRecords.length") == 1, "取消删除不该删"

        # 删除：确认
        pg.click("[data-rec-del]"); pg.wait_for_timeout(150)
        pg.click("#cf-yes"); pg.wait_for_timeout(200)
        assert pg.evaluate("state.stageRecords.length") == 0, "确认后记录还在"

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 问题7：阶段记录可删除")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
