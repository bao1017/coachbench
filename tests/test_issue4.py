# -*- coding: utf-8 -*-
"""问题4测试：只留队员；无身份选项/教练备注；记录项含30/60/80/100/200/400/800米/三级跳/铅球，无周训练量"""
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

        pg.click('.nav-item[data-view="people"]'); pg.wait_for_timeout(150)
        # 没有筛选按钮
        assert pg.locator(".filter-btn").count() == 0, "筛选按钮还在"

        # 加人：没有身份选择、没有教练备注
        pg.click("#ppl-add"); pg.wait_for_timeout(150)
        assert pg.locator("#pf-kind").count() == 0, "身份选择还在"
        assert pg.locator("#pf-note").count() == 0, "教练备注还在"
        pg.fill("#pf-name", "王队员")
        pg.fill("#pf-spec", "短跑")
        pg.click("#pfc-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=王队员"), "队员没加上"

        # 进专属页记一次数据
        pg.click('[data-person]'); pg.wait_for_timeout(200)
        pg.click("#rec-add"); pg.wait_for_timeout(150)
        for fid, label in [("rf-m30","30米"),("rf-m60","60米"),("rf-m80","80米"),
                           ("rf-m100","100米"),("rf-m200","200米"),("rf-m400","400米"),
                           ("rf-m800","800米")]:
            assert pg.locator(f"#{fid}").count() == 1, f"缺字段 {label}"
        assert pg.locator('text=三级跳远').count() >= 1, "缺三级跳远"
        assert pg.locator('text=铅球').count() >= 1, "缺铅球"
        assert pg.locator('text=本周训练量').count() == 0, "本周训练量还在"

        pg.fill("#rf-m100", "13.5")
        pg.click("#rf-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=100米 13.5s"), "记录没显示在时间线上"

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 问题4：队员制+专项记录项")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
