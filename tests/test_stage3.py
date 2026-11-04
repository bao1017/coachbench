# -*- coding: utf-8 -*-
"""阶段3测试：加学员/筛选/进档案/加目标/记阶段数据/持久化"""
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

        # 进名单，加学员
        pg.click('.nav-item[data-view="people"]'); pg.wait_for_timeout(150)
        pg.click("#ppl-add"); pg.wait_for_timeout(150)
        pg.select_option("#pf-kind", "student")
        pg.fill("#pf-name", "张伟")
        pg.fill("#pf-left", "8")
        pg.click("#pfc-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=张伟"), "学员没出现在名单"
        assert pg.is_visible("text=剩 8 节课"), "学员关键信息不对"

        # 加队员
        pg.click("#ppl-add"); pg.wait_for_timeout(150)
        pg.select_option("#pf-kind", "athlete")
        pg.fill("#pf-name", "李强")
        pg.fill("#pf-spec", "短跑")
        pg.click("#pfc-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=李强"), "队员没出现在名单"

        # 筛选：只看学员，李强应消失
        pg.click('.filter-btn[data-f="student"]'); pg.wait_for_timeout(150)
        assert pg.is_visible("text=张伟")
        assert pg.locator("text=李强").count() == 0, "学员筛选没生效"
        pg.click('.filter-btn[data-f="all"]'); pg.wait_for_timeout(150)

        # 进张伟的专属页
        pg.click('[data-person] >> text=张伟'); pg.wait_for_timeout(200)
        assert pg.is_visible("#view-person"), "没进人员专属页"

        # 加目标（20天后到期）
        pg.click("#goal-add"); pg.wait_for_timeout(150)
        pg.fill("#gf-text", "期末体测跑进13秒")
        pg.evaluate("document.getElementById('gf-deadline').value = new Date(Date.now()+20*86400000).toISOString().slice(0,10)")
        pg.click("#gf-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=期末体测跑进13秒"), "目标没加上"

        # 记一次阶段数据（学员）
        pg.click("#rec-add"); pg.wait_for_timeout(150)
        pg.fill("#rf-att", "4")
        pg.fill("#rf-test", "13.8")
        pg.fill("#rf-left", "8")
        pg.click("#rf-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=出勤 4 次"), "阶段记录没出现"

        # 刷新后都在
        pg.reload(); pg.wait_for_timeout(300)
        n = pg.evaluate("state.people.length")
        assert n == 2, f"刷新后人数不对: {n}"
        g = pg.evaluate("state.goals.length")
        assert g == 1, f"刷新后目标丢了: {g}"
        r = pg.evaluate("state.stageRecords.length")
        assert r == 1, f"刷新后阶段记录丢了: {r}"

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 阶段3：名单/档案/目标/记录")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
