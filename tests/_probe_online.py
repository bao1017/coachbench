import json
from playwright.sync_api import sync_playwright

URL = "https://chenbaobao-d8ghoabd1c14a8692-1532490077.tcloudbaseapp.com/index.html"
logs, bad = [], []
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    pg = b.new_page()
    pg.on("console", lambda m: logs.append(f"[{m.type}] {m.text}"))
    pg.on("pageerror", lambda e: logs.append(f"[pageerror] {e}"))
    pg.on("response", lambda r: bad.append(f"{r.status} {r.url}") if r.status >= 400 else None)
    pg.goto(URL, wait_until="networkidle", timeout=30000)
    pg.wait_for_timeout(2000)
    try:
        pg.click("text=我是开发", timeout=4000)
        pg.wait_for_timeout(3000)
    except Exception as e:
        print("click interstitial:", e)
    info = pg.evaluate("""() => ({
        url: location.href,
        hasCloudbase: typeof cloudbase !== 'undefined',
        loginVisible: !!(document.getElementById('login-screen') && getComputedStyle(document.getElementById('login-screen')).display!=='none'),
        bodyText: document.body.innerText.slice(0,200)
    })""")
    print(json.dumps(info, ensure_ascii=False))
    print("---- bad responses ----")
    for x in bad[:20]: print(x)
    print("---- console ----")
    for l in logs[:40]: print(l)
    b.close()
