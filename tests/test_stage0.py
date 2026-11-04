# -*- coding: utf-8 -*-
"""阶段0测试：页面骨架、导航切换、今日日期、无控制台错误"""
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
        pg.wait_for_timeout(300)

        # 1. 顶部日期显示今天
        today = datetime.date.today()
        date_text = pg.text_content("#top-date")
        assert f"{today.month}月{today.day}日" in date_text, f"顶部日期不对: {date_text}"

        # 2. 初始在首页
        assert pg.is_visible("#view-home"), "首页默认不可见"

        # 3. 逐个切导航
        expect = {
            "calendar": "#view-calendar",
            "people": "#view-people",
            "stages": "#view-stages",
            "settings": "#view-settings",
            "home": "#view-home",
        }
        for view, sel in expect.items():
            pg.click(f'.nav-item[data-view="{view}"]')
            pg.wait_for_timeout(100)
            assert pg.is_visible(sel), f"切到 {view} 后 {sel} 不可见"
            active = pg.get_attribute('.nav-item.active', 'data-view')
            assert active == view, f"导航高亮不对: {active}"

        # 4. 设置在导航最底部
        items = pg.eval_on_selector_all(".nav-item", "els => els.map(e=>e.dataset.view)")
        assert items[-1] == "settings", f"设置不在导航最后: {items}"

        # 5. 无控制台错误
        assert not errors, f"控制台报错: {errors}"

        b.close()
    print("PASS 阶段0：骨架/导航/日期/无报错")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
