# -*- coding: utf-8 -*-
"""第五轮素材：压缩 6 张商城界面样板图 + 补截三个案例站的 PC/手机页面图"""
import os
import glob
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
MALL = os.path.join(ROOT, "assets", "mall")
CASES = os.path.join(ROOT, "assets", "cases")
os.makedirs(MALL, exist_ok=True)
os.makedirs(CASES, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 1. 商城界面样板（按用户给出的顺序）
srcs = sorted(glob.glob(r"C:\Users\SAMSUNG\.workbuddy\clipboard-images\clipboard-2026-11-08T04-58-20-*.jpg"))
srcs.append(r"C:\Users\SAMSUNG\Documents\xwechat_files\piweih_eab9\temp\RWTemp\2026-11\f042404436df28a8472a0e4b52091203.jpg")
for i, src in enumerate(srcs, 1):
    im = Image.open(src).convert("RGB")
    im.thumbnail((440, 980), Image.LANCZOS)
    out = os.path.join(MALL, "mall-%02d.jpg" % i)
    im.save(out, "JPEG", quality=82, optimize=True)
    print("mall-%02d.jpg" % i, im.size, os.path.getsize(out) // 1024, "KB")

# 2. 案例站：PC 内页 + 手机首屏 + 手机内页
SITES = [
    ("case-shanghui", "https://www.zyyous.com/"),
    ("case-cailie", "https://www.91cailie.com/"),
    ("case-baydea", "https://www.baydea.com/"),
]
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=EDGE, headless=True,
                                args=["--no-sandbox", "--disable-gpu"])
    for stem, url in SITES:
        pg = browser.new_page(viewport={"width": 1440, "height": 940})
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=45000)
            pg.wait_for_timeout(2200)
            pg.evaluate("window.scrollTo(0, 950)")
            pg.wait_for_timeout(1200)
            path = os.path.join(CASES, stem + "-pc2.jpg")
            pg.screenshot(path=path, type="jpeg", quality=80)
            print("OK", os.path.basename(path))
        except Exception as e:
            print("FAIL", stem, "pc2", repr(e)[:120])
        pg.close()

        m = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1,
                             is_mobile=True, has_touch=True)
        try:
            m.goto(url, wait_until="domcontentloaded", timeout=45000)
            m.wait_for_timeout(2200)
            m.evaluate("window.scrollTo(0, 0)")
            m.wait_for_timeout(400)
            path = os.path.join(CASES, stem + "-m1.jpg")
            m.screenshot(path=path, type="jpeg", quality=80)
            m.evaluate("window.scrollTo(0, 760)")
            m.wait_for_timeout(1200)
            path = os.path.join(CASES, stem + "-m2.jpg")
            m.screenshot(path=path, type="jpeg", quality=80)
            print("OK", stem, "m1 / m2")
        except Exception as e:
            print("FAIL", stem, "mobile", repr(e)[:120])
        m.close()
    browser.close()
