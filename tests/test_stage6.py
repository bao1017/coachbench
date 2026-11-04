# -*- coding: utf-8 -*-
"""阶段6测试：导出备份/导入恢复/清空保护"""
import sys, json, tempfile, os
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

        # 造数据
        pg.evaluate("""
          state.people.push({id:'p1', kind:'student', name:'张伟', student:{remainingClasses:8}});
          state.plans.push({id:'pl1', date:'2099-01-01', title:'保留测试', type:'work', peopleIds:[], note:'', done:false, time:''});
          save();
        """)
        pg.click('.nav-item[data-view="settings"]'); pg.wait_for_timeout(200)

        # 导出备份
        with pg.expect_download() as dl_info:
            pg.click("#btn-export")
        dl = dl_info.value
        tmp = os.path.join(tempfile.gettempdir(), "wb_backup.json")
        dl.save_as(tmp)
        data = json.load(open(tmp, encoding="utf-8"))
        assert data["people"][0]["name"] == "张伟", "导出文件内容不对"

        # 清空保护：按钮一开始禁用
        assert pg.is_disabled("#btn-clear"), "清空按钮一开始就可点"
        pg.fill("#clear-input", "错错")
        assert pg.is_disabled("#btn-clear"), "没输入'清空'按钮不该可点"
        pg.fill("#clear-input", "清空")
        assert pg.is_enabled("#btn-clear"), "输入'清空'后按钮应可用"

        # 不点清空（避免 reload 麻烦），改测导入闭环：
        # 先删 localStorage 模拟数据丢了，再用刚导出的文件恢复
        pg.evaluate("localStorage.removeItem('coachbench-v1'); location.reload();")
        pg.wait_for_timeout(300)
        assert pg.evaluate("state.people.length") == 0, "清空后不该还有人"
        pg.click('.nav-item[data-view="settings"]'); pg.wait_for_timeout(200)
        pg.set_input_files("#import-file", tmp)
        pg.wait_for_timeout(300)
        # 弹确认 → 确认
        assert pg.is_visible("#overlay"), "导入前该弹覆盖确认"
        pg.click("#cf-yes")
        pg.wait_for_timeout(400)
        n = pg.evaluate("state.people.length")
        assert n == 1, f"导入后人数不对: {n}"
        t = pg.evaluate("state.plans[0].title")
        assert t == "保留测试", f"导入后计划不对: {t}"

        os.remove(tmp)
        assert not errors, f"控制台报错: {errors}"
        b.close()
    print("PASS 阶段6：备份/恢复/清空保护")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("FAIL:", e); sys.exit(1)
