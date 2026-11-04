# -*- coding: utf-8 -*-
"""阶段4测试：阶段汇总页的目标倒计时、最近两次数据对比（进步绿/退步红）"""
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
        d2 = today.isoformat()
        soon = (today + datetime.timedelta(days=5)).isoformat()

        # 造数据：一个队员，两次100米（13.5→13.2 进步），一个5天后到期的目标
        pg.evaluate(f"""
          state.people.push({{id:'p1', kind:'athlete', name:'李强', athlete:{{group:'甲组', specialty:'短跑'}}}});
          state.stageRecords.push({{id:'r1', personId:'p1', date:'{d1}', metrics:{{sprint100:13.5, squat:100}}}});
          state.stageRecords.push({{id:'r2', personId:'p1', date:'{d2}', metrics:{{sprint100:13.2, squat:105}}}});
          state.goals.push({{id:'g1', personId:'p1', text:'100米进13秒', deadline:'{soon}', done:false}});
          save();
        """)
        pg.reload(); pg.wait_for_timeout(300)

        pg.click('.nav-item[data-view="stages"]'); pg.wait_for_timeout(200)
        row = pg.locator('[data-person="p1"]')
        assert row.count()==1, "汇总页没有李强这一行"
        # 目标剩5天 → warn-text
        assert row.locator(".warn-text").count()==1, "5天后到期的目标没标红"
        # 100米 13.5→13.2 进步 → up 类
        up = row.locator("span.up")
        assert up.count() >= 1, "进步项没标绿"
        txt = row.inner_text()
        assert "13.5s→13.2s" in txt.replace(" ",""), f"对比数字没出现: {txt}"

        # 退步场景：体重 75→78（dir down，变大=退步红）
        pg.evaluate(f"""
          state.stageRecords.push({{id:'r3', personId:'p1', date:'{d2}', metrics:{{weight:75}}}});
          state.stageRecords.push({{id:'r4', personId:'p1', date:'{d2}', metrics:{{weight:78}}}});
          save();
        """)
        pg.reload(); pg.wait_for_timeout(300)
        pg.click('.nav-item[data-view="stages"]'); pg.wait_for_timeout(200)
        assert pg.locator('[data-person="p1"] span.down').count() >= 1, "体重上升（退步）没标红"

        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 阶段4：阶段汇总/对比方向")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
