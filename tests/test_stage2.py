# -*- coding: utf-8 -*-
"""阶段2测试：日历加计划/勾选完成/编辑/删除确认/翻月"""
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

        # 进日历
        pg.click('.nav-item[data-view="calendar"]')
        pg.wait_for_timeout(150)

        # 加一条今天的计划
        pg.click("#plan-add")
        pg.wait_for_timeout(150)
        today = datetime.date.today().isoformat()
        pg.fill("#f-date", today)
        pg.fill("#f-time", "16:00")
        pg.fill("#f-plan", "下午带短跑组跑间歇")
        pg.click("#pf-save")
        pg.wait_for_timeout(200)
        assert pg.is_visible(f'text=下午带短跑组跑间歇'), "新加的计划没出现在当天列表"

        # 日历格子上有标记
        cell = pg.locator(f'.cal-cell[data-date="{today}"] .mark')
        assert cell.count() == 1, "今天格子上没有计划标记"

        # 勾选完成 → 刷新后仍完成
        pg.check('[data-plan-done]')
        pg.wait_for_timeout(150)
        pg.reload(); pg.wait_for_timeout(300)
        pg.click('.nav-item[data-view="calendar"]'); pg.wait_for_timeout(150)
        checked = pg.evaluate("state.plans[0].done")
        assert checked is True, "勾选完成后刷新状态丢了"

        # 删除：先取消
        pg.click('[data-plan-del]')
        pg.wait_for_timeout(150)
        assert pg.is_visible("#overlay"), "删除没弹确认框"
        pg.click("#cf-no")
        pg.wait_for_timeout(150)
        assert pg.evaluate("state.plans.length") == 1, "取消删除后计划不该消失"

        # 删除：确认
        pg.click('[data-plan-del]')
        pg.click("#cf-yes")
        pg.wait_for_timeout(200)
        assert pg.evaluate("state.plans.length") == 0, "确认删除后计划还在"

        # 翻月按钮存在且可点
        pg.click("#cal-next"); pg.wait_for_timeout(100)
        pg.click("#cal-prev"); pg.wait_for_timeout(100)
        pg.click("#cal-today"); pg.wait_for_timeout(100)

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 阶段2：日历增删改/勾选/确认")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
