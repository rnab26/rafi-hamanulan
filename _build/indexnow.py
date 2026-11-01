"""Envoie toutes les URL du sitemap à IndexNow (Bing, Yandex…). Gratuit, sans compte.
Usage : python3 _build/indexnow.py"""
import os, re, json, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "_build/build.py"), encoding="utf-8").read().split("# ==================================================================")[0]
cfg = {"__file__": os.path.join(ROOT, "_build/build.py")}; exec(src, cfg)
site, key = cfg["SITE_URL"], cfg["INDEXNOW_KEY"]
urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "public/sitemap.xml")).read())
body = json.dumps({"host": site.split("//")[1], "key": key, "keyLocation": f"{site}/{key}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("IndexNow :", r.status, "–", len(urls), "URL envoyées pour", site)
