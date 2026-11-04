# -*- coding: utf-8 -*-
"""阶段3测试：加队员/搜索/进档案/加目标/记阶段数据/持久化（按新需求：只队员）"""
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
        pg.fill("#pf-name", "李强")
        pg.fill("#pf-spec", "短跑")
        pg.click("#pfc-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=李强"), "队员没出现在名单"
        assert pg.is_visible("text=主项：短跑"), "队员关键信息不对"

        pg.click("#ppl-add"); pg.wait_for_timeout(150)
        pg.fill("#pf-name", "赵队员")
        pg.click("#pfc-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=赵队员")

        # 搜索
        pg.fill("#ppl-q", "李强"); pg.wait_for_timeout(150)
        assert pg.is_visible("text=李强")
        assert pg.locator("text=赵队员").count() == 0, "搜索没生效"
        pg.fill("#ppl-q", ""); pg.wait_for_timeout(150)

        # 进李强专属页
        pg.click('[data-person] >> text=李强'); pg.wait_for_timeout(200)
        assert pg.is_visible("#view-person")

        # 加目标
        pg.click("#goal-add"); pg.wait_for_timeout(150)
        pg.fill("#gf-text", "100米进13秒")
        pg.evaluate("document.getElementById('gf-deadline').value = new Date(Date.now()+20*86400000).toISOString().slice(0,10)")
        pg.click("#gf-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=100米进13秒")

        # 记阶段数据
        pg.click("#rec-add"); pg.wait_for_timeout(150)
        pg.fill("#rf-m100", "13.8")
        pg.click("#rf-save"); pg.wait_for_timeout(200)
        assert pg.is_visible("text=100米 13.8s"), "阶段记录没出现"

        # 刷新持久化
        pg.reload(); pg.wait_for_timeout(300)
        assert pg.evaluate("state.people.length") == 2
        assert pg.evaluate("state.goals.length") == 1
        assert pg.evaluate("state.stageRecords.length") == 1

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 阶段3：名单/档案/目标/记录")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
