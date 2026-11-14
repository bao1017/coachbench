# -*- coding: utf-8 -*-
from pathlib import Path
from playwright.sync_api import sync_playwright
HTML = Path(r"C:\Users\陈硕腾\Desktop\app\工作生活工作台.html")
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    pg = b.new_page(viewport={"width":1440,"height":900})
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(HTML.as_uri()); pg.wait_for_timeout(300)
    pg.screenshot(path=r"C:\Users\陈硕腾\Desktop\app\tests\_desktop_home.png")
    print("ERRORS:", errs)
    b.close()
