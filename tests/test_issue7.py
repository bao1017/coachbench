# -*- coding: utf-8 -*-
"""问题7测试：阶段数据记录可删除——左滑露出删除键再点（带确认）"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = Path(r"C:\Users\陈硕腾\Desktop\app\工作生活工作台.html")

def swipe_left(pg, sel):
    # 模拟左滑后的展开态（手势在 headless 下不稳定，直接摆态验证删除流程）
    pg.locator(sel).evaluate("e => e.style.transform='translateX(-76px)'")
    pg.wait_for_timeout(150)

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
        assert pg.is_visible("text=100米 13.5s")

        # 删除按钮默认藏在卡片后面（translateX 为 0）
        t = pg.locator(".swipe-in").first.evaluate("e => getComputedStyle(e).transform")
        assert t in ("none", "matrix(1, 0, 0, 1, 0, 0)"), t

        # 左滑露出
        swipe_left(pg, ".swipe-in")
        pg.click("[data-rec-del]"); pg.wait_for_timeout(150)
        pg.click("#cf-no"); pg.wait_for_timeout(150)
        assert pg.evaluate("state.stageRecords.length") == 1, "取消删除不该删"

        # 左滑→确认
        swipe_left(pg, ".swipe-in")
        pg.click("[data-rec-del]"); pg.wait_for_timeout(150)
        pg.click("#cf-yes"); pg.wait_for_timeout(200)
        assert pg.evaluate("state.stageRecords.length") == 0, "确认后记录还在"

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 问题7：左滑删除")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
