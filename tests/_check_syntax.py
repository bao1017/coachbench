import re, subprocess, sys, tempfile, os
p = r"C:\Users\陈硕腾\Desktop\app\工作生活工作台.html"
html = open(p, encoding="utf-8").read()
blocks = re.findall(r"<script(?![^>]*src=)[^>]*>(.*?)</script>", html, re.S)
print("inline script blocks:", len(blocks))
tmp = os.path.join(tempfile.gettempdir(), "_app_check.js")
open(tmp, "w", encoding="utf-8").write("\n;\n".join(blocks))
r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
print("exit", r.returncode)
print(r.stderr)
sys.exit(r.returncode)
