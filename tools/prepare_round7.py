# -*- coding: utf-8 -*-
"""截取新增 4 个案例站：PC 首屏 / PC 内页 / 手机首屏 / 手机内页"""
import os
from playwright.sync_api import sync_playwright

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
OUT = os.path.join(ROOT, "assets", "cases")
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

SITES = [
    ("case-jianzhuo", "https://www.dgjzkj.com/"),
    ("case-guanxiang", "https://www.touzs.com/"),
    ("case-niling", "https://www.365ls.cn/"),
    ("case-leiyiming", "https://www.oals.cn/"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=EDGE, headless=True,
                                args=["--no-sandbox", "--disable-gpu"])
    for stem, url in SITES:
        pg = browser.new_page(viewport={"width": 1440, "height": 940})
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=45000)
            pg.wait_for_timeout(2600)
            pg.evaluate("window.scrollTo(0, 0)")
            pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(OUT, stem + ".png"))
            pg.evaluate("window.scrollTo(0, 950)")
            pg.wait_for_timeout(1300)
            pg.screenshot(path=os.path.join(OUT, stem + "-pc2.jpg"), type="jpeg", quality=80)
            print("OK", stem, "PC")
        except Exception as exc:
            print("FAIL", stem, "PC", repr(exc)[:140])
        pg.close()

        m = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1,
                             is_mobile=True, has_touch=True)
        try:
            m.goto(url, wait_until="domcontentloaded", timeout=45000)
            m.wait_for_timeout(2600)
            m.evaluate("window.scrollTo(0, 0)")
            m.wait_for_timeout(400)
            m.screenshot(path=os.path.join(OUT, stem + "-m1.jpg"), type="jpeg", quality=80)
            m.evaluate("window.scrollTo(0, 760)")
            m.wait_for_timeout(1300)
            m.screenshot(path=os.path.join(OUT, stem + "-m2.jpg"), type="jpeg", quality=80)
            print("OK", stem, "mobile")
        except Exception as exc:
            print("FAIL", stem, "mobile", repr(exc)[:140])
        m.close()
    browser.close()
