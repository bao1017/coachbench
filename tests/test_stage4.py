# -*- coding: utf-8 -*-
"""阶段4测试：阶段汇总页的目标倒计时、最近两次数据对比（进步绿/退步红）——新专项字段"""
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
        pg.evaluate("localStorage.removeItem('coachbench-v1');")

        today = datetime.date.today()
        d1 = (today - datetime.timedelta(days=30)).isoformat()
        d2 = (today - datetime.timedelta(days=10)).isoformat()
        d3 = today.isoformat()
        soon = (today + datetime.timedelta(days=5)).isoformat()

        pg.evaluate(f"""
          state.people.push({{id:'p1', kind:'athlete', name:'李强', athlete:{{}}}});
          state.stageRecords.push({{id:'r1', personId:'p1', date:'{d1}', metrics:{{m100:13.5, shotPut:11}}}});
          state.stageRecords.push({{id:'r2', personId:'p1', date:'{d2}', metrics:{{m100:13.2, shotPut:12}}}});
          state.stageRecords.push({{id:'r3', personId:'p1', date:'{d3}', metrics:{{m100:13.8}}}});
          state.goals.push({{id:'g1', personId:'p1', text:'100米进13秒', deadline:'{soon}', done:false}});
          save();
        """)
        pg.reload(); pg.wait_for_timeout(300)
        pg.click('.nav-item[data-view="stages"]'); pg.wait_for_timeout(200)
        row = pg.locator('[data-person="p1"]')
        assert row.locator(".warn-text").count() == 1, "5天内到期目标没标红"
        txt = row.inner_text()
        # m100 最近两次 13.2→13.8 退步红
        assert row.locator("span.down").count() >= 1, "m100 变慢没标红"
        # 铅球 11→12 进步绿
        assert row.locator("span.up").count() >= 1, "铅球进步没标绿"
        assert "13.2s→13.8s" in txt.replace(" ",""), txt

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 阶段4：阶段汇总/对比方向")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
