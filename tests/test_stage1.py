# -*- coding: utf-8 -*-
"""阶段1测试：localStorage 自动持久化、toast、confirm 弹窗"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = Path(r"C:\Users\陈硕腾\Desktop\app\工作生活工作台.html")

def main():
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(HTML.as_uri())
        pg.wait_for_timeout(200)

        # 1. 写入一条数据并保存 → 刷新后还在
        pg.evaluate("state.memos.push({id:'t1', text:'测试备忘', done:false}); save();")
        pg.reload()
        pg.wait_for_timeout(200)
        n = pg.evaluate("state.memos.length")
        assert n == 1, f"刷新后备忘丢失: {n}"
        txt = pg.evaluate("state.memos[0].text")
        assert txt == "测试备忘", f"备忘内容不对: {txt}"

        # 2. 关闭重开（新 context 模拟重启浏览器）→ 还在
        pg2 = ctx.new_page()
        pg2.goto(HTML.as_uri())
        pg2.wait_for_timeout(200)
        n2 = pg2.evaluate("state.memos.length")
        assert n2 == 1, f"新页面数据丢失: {n2}"
        pg2.close()

        # 3. toast 出现并自动消失
        pg.evaluate("toast('已保存')")
        assert pg.is_visible("#toast"), "toast 没出现"
        pg.wait_for_timeout(2300)
        assert not pg.evaluate("document.getElementById('toast').classList.contains('show')"), "toast 未自动消失"

        # 4. confirm 弹窗：取消不执行
        called = {"v": False}
        pg.evaluate("window.__cf = ()=>{ window.__called=true; }; confirmDialog('删吗？', window.__cf);")
        assert pg.is_visible("#overlay"), "确认弹窗没打开"
        pg.click("#cf-no")
        assert not pg.is_visible("#overlay"), "取消后弹窗没关"
        assert pg.evaluate("window.__called !== true"), "取消不该执行回调"

        # 5. confirm 弹窗：确认执行
        pg.evaluate("confirmDialog('删吗？', window.__cf);")
        pg.click("#cf-yes")
        assert pg.evaluate("window.__called === true"), "确认后没执行回调"

        # 清掉测试数据
        pg.evaluate("localStorage.removeItem('coachbench-v1');")

        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 阶段1：持久化/toast/confirm")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
