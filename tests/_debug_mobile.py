# -*- coding: utf-8 -*-
import sys, datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = Path(r"C:\Users\陈硕腾\Desktop\app\工作生活工作台.html")

def main():
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge")
        pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(HTML.as_uri())
        pg.wait_for_timeout(400)

        sw = pg.evaluate("({w: innerWidth, sw: document.documentElement.scrollWidth, bodySw: document.body.scrollWidth})")
        print("VIEWPORT:", sw)
        overflow = sw["sw"] > sw["w"] + 1
        print("HORIZONTAL_OVERFLOW:", overflow)

        # 各视图切换，检查溢出
        for view in ["home","calendar","people","stages","settings"]:
            pg.click(f'.nav-item[data-view="{view}"]')
            pg.wait_for_timeout(150)
            o = pg.evaluate("({w: innerWidth, sw: document.documentElement.scrollWidth})")
            print(view, o, "OVERFLOW" if o["sw"]>o["w"]+1 else "ok")

        pg.click('.nav-item[data-view="home"]'); pg.wait_for_timeout(150)
        pg.screenshot(path=r"C:\Users\陈硕腾\Desktop\app\tests\_mobile_home.png")
        print("ERRORS:", errors)
        b.close()

if __name__ == "__main__":
    main()
