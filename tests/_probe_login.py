import json
from playwright.sync_api import sync_playwright

URL = "https://chenbaobao-d8ghoabd1c14a8692-1532490077.tcloudbaseapp.com/"
logs, reqs = [], []
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    pg = b.new_page()
    pg.on("console", lambda m: logs.append(f"[{m.type}] {m.text}"))
    pg.on("pageerror", lambda e: logs.append(f"[pageerror] {e}"))
    def on_resp(r):
        if "auth" in r.url or "login" in r.url or "signin" in r.url:
            try: body = r.text()[:300]
            except Exception: body = "<no body>"
            reqs.append(f"{r.status} {r.request.method} {r.url}\n  body={body}")
    pg.on("response", on_resp)
    pg.goto(URL, wait_until="networkidle", timeout=30000)
    pg.wait_for_timeout(2500)
    try:
        pg.click("text=确定访问", timeout=5000); pg.wait_for_timeout(2500)
    except Exception as e:
        print("gate:", e)
    pg.fill("#login-user", "chen1017")
    pg.fill("#login-pass", "wrongpass_probe_123")
    pg.click("#login-btn")
    pg.wait_for_timeout(5000)
    err = pg.evaluate("() => (document.getElementById('login-err')||{}).innerText")
    print("ERR:", err)
    print("---- auth requests ----")
    for x in reqs: print(x)
    print("---- console ----")
    for l in logs[:40]: print(l)
    b.close()
