import json
from playwright.sync_api import sync_playwright

URL = "https://chenbaobao-d8ghoabd1c14a8692-1532490077.tcloudbaseapp.com/"
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    pg = b.new_page()
    pg.goto(URL, wait_until="networkidle", timeout=30000)
    pg.wait_for_timeout(2000)
    html = pg.content()
    print("COOKIES:", pg.context.cookies())
    # dump buttons/links
    btns = pg.evaluate("""() => Array.from(document.querySelectorAll('a,button,div[role=button]')).map(e=>({t:e.innerText, href:e.href||'', onclick:(e.onclick||'').toString().slice(0,120)}))""")
    print(json.dumps(btns, ensure_ascii=False, indent=1))
    print("HTMLLEN", len(html))
    print(html[:1500])
    b.close()
