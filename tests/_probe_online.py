import json
from playwright.sync_api import sync_playwright

URL = "https://chenbaobao-d8ghoabd1c14a8692-1532490077.tcloudbaseapp.com/"
logs, bad = [], []
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    pg = b.new_page()
    pg.on("console", lambda m: logs.append(f"[{m.type}] {m.text}"))
    pg.on("pageerror", lambda e: logs.append(f"[pageerror] {e}"))
    pg.on("response", lambda r: bad.append(f"{r.status} {r.url}") if r.status >= 400 else None)
    pg.goto(URL, wait_until="networkidle", timeout=30000)
    pg.wait_for_timeout(2500)
    try:
        pg.click("text=确定访问", timeout=5000)
        pg.wait_for_timeout(3500)
    except Exception as e:
        print("click gate:", e)
    info = pg.evaluate("""() => ({
        url: location.href,
        hasCloudbase: typeof cloudbase !== 'undefined',
        loginVisible: !!(document.getElementById('login-screen') && getComputedStyle(document.getElementById('login-screen')).display!=='none'),
        bodyText: document.body.innerText.slice(0,160)
    })""")
    print(json.dumps(info, ensure_ascii=False))
    print("---- bad ----")
    for x in bad[:20]: print(x)
    print("---- console ----")
    for l in logs[:40]: print(l)
    b.close()
