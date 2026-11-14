import json
from playwright.sync_api import sync_playwright

URL = "https://chenbaobao-d8ghoabd1c14a8692-1532490077.tcloudbaseapp.com/"
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    pg = b.new_page()
    pg.goto(URL, wait_until="networkidle", timeout=30000)
    pg.wait_for_timeout(2500)
    try:
        pg.click("text=确定访问", timeout=5000); pg.wait_for_timeout(2000)
    except Exception as e:
        print("gate:", e)
    res = pg.evaluate("""async () => {
        const out = {};
        try {
            const app = cloudbase.init({ env: 'chenbaobao-d8ghoabd1c14a8692', region: 'ap-shanghai' });
            const auth = typeof app.auth === 'function' ? app.auth() : app.auth;
            out.methods = Object.getOwnPropertyNames(Object.getPrototypeOf(auth)).filter(m=>/sign|register|password|user/i.test(m));
            if (typeof auth.isUsernameRegistered === 'function') {
                out.usernameRegistered = await auth.isUsernameRegistered('chen1017');
            } else {
                out.isUsernameRegistered = 'missing';
            }
        } catch(e) { out.err = String(e && (e.message||e)); }
        return out;
    }""")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    b.close()
