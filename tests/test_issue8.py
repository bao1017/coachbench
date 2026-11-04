# -*- coding: utf-8 -*-
"""问题8测试：老格式数据（无athlete字段）打开个人页不空白"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = Path(r"C:\Users\陈硕腾\Desktop\app\工作生活工作台.html")

def main():
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(HTML.as_uri())
        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        # 老数据：没有 athlete 字段
        pg.evaluate("state.people.push({id:'old1', kind:'athlete', name:'老队员'}); save();")
        pg.reload(); pg.wait_for_timeout(300)
        pg.click('.nav-item[data-view="people"]'); pg.wait_for_timeout(150)
        pg.click('[data-person]'); pg.wait_for_timeout(200)
        body = pg.inner_text('#view-person')
        assert '老队员' in body, body
        assert '档案' in body, body
        assert not errors, errors
        pg.evaluate("localStorage.removeItem('coachbench-v1');")
        b.close()
    print("PASS 问题8：老数据个人页兼容")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
