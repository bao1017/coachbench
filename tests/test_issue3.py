# -*- coding: utf-8 -*-
"""问题3测试：顶部有手动保存按钮，点击后 toast 提示"""
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
        pg.wait_for_timeout(200)

        assert pg.locator("#btn-save").count() == 1, "顶部没有手动保存按钮"
        pg.click("#btn-save")
        pg.wait_for_timeout(200)
        assert pg.is_visible("#toast"), "点保存后没出提示"
        assert "手动保存" in pg.text_content("#toast"), pg.text_content("#toast")

        # 点完刷新数据仍在
        pg.evaluate("state.memos.push({id:'x',text:'a',done:false});")
        pg.click("#btn-save")
        pg.wait_for_timeout(200)
        pg.reload(); pg.wait_for_timeout(200)
        assert pg.evaluate("state.memos.length") == 1, "手动保存没真正写入"

        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 问题3：手动保存按钮")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
