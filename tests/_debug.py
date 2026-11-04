# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import pathlib
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto(pathlib.Path(r'C:\Users\陈硕腾\Desktop\app\工作生活工作台.html').as_uri())
    pg.evaluate("localStorage.removeItem('coachbench-v1');")
    pg.evaluate("state.people.push({id:'p1',kind:'athlete',name:'测试',athlete:{group:'A组',specialty:'短跑',joinDate:''}}); save();")
    pg.reload(); pg.wait_for_timeout(300)
    pg.click('.nav-item[data-view=people]'); pg.wait_for_timeout(200)
    pg.click('[data-person]'); pg.wait_for_timeout(300)
    print('LEN:', len(pg.inner_html('#view-person')))
    print('VISIBLE:', pg.is_visible('#view-person'))
    print('TEXT:', pg.inner_text('#view-person')[:200])
    print('ERRORS:', errs)
    import io, sys
    open(r'C:\Users\陈硕腾\Desktop\app\tests\_debug_out.txt','w',encoding='utf-8').write(
      f"LEN={len(pg.inner_html('#view-person'))}\nVIS={pg.is_visible('#view-person')}\nTEXT={pg.inner_text('#view-person')[:300]}\nERRS={errs}")
