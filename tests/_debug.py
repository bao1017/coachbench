# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import pathlib
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto(pathlib.Path(r'C:\Users\陈硕腾\Desktop\app\工作生活工作台.html').as_uri())
    pg.wait_for_timeout(500)
    import datetime
    today = datetime.date.today().isoformat()
    pg.evaluate(f"""
      state.plans.push({{id:'p1',date:'{today}',title:'起跑练习',reps:'30',sets:'4',intensity:'大',group:'normal'}});
      state.plans.push({{id:'p2',date:'{today}',title:'康复慢跑',reps:'2',sets:'2',intensity:'低',group:'injured'}});
      save();
    """)
    pg.reload(); pg.wait_for_timeout(300)
    pg.click('.nav-item[data-view=home]'); pg.wait_for_timeout(200)
    home = pg.inner_text('#view-home')
    pg.click('.nav-item[data-view=calendar]'); pg.wait_for_timeout(200)
    info = pg.evaluate(f"""JSON.stringify({{
      sel: document.querySelector('.cal-cell.selected')?.dataset.date,
      all: state.plans.map(p=>({{d:p.date,t:p.title,g:p.group}})),
      filt: state.plans.filter(p=>p.date==='{today}').map(p=>({{g:p.group, m:(p.group||'normal')==='normal'}}))
    }})""")
    pg.click(f'.cal-cell[data-date="{today}"]'); pg.wait_for_timeout(300)
    dom = pg.evaluate("JSON.stringify({ptn: document.getElementById('pt-normal')?.outerHTML?.slice(0,400), pti: document.getElementById('pt-injured')?.outerHTML?.slice(0,200)})")
    txt = pg.inner_text('#modal')
    body = pg.inner_text('#view-home')
    open(r'C:\Users\陈硕腾\Desktop\app\tests\_debug_out.txt','w',encoding='utf-8').write(
      f'INFO={info}\nDOM={dom}\nMODAL_VISIBLE={pg.is_visible("#overlay")}\nMODAL_TEXT={txt[:500]}\nHOME_TEXT={body[:300]}\nERRORS={errs}')
