# -*- coding: utf-8 -*-
"""用 Edge 无头浏览器截取三个案例站首屏，作为案例卡片配图"""
import os
from playwright.sync_api import sync_playwright

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
OUT = os.path.join(ROOT, "assets", "cases")
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

SITES = [
    ("case-shanghui", "https://www.zyyous.com/"),
    ("case-cailie", "https://www.91cailie.com/"),
    ("case-baydea", "https://www.baydea.com/"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=EDGE, headless=True,
                                args=["--no-sandbox", "--disable-gpu"])
    for name, url in SITES:
        page = browser.new_page(viewport={"width": 1440, "height": 940},
                                device_scale_factor=1)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(2800)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(400)
            page.screenshot(path=os.path.join(OUT, name + ".png"))
            print("OK", name, url)
        except Exception as exc:
            print("FAIL", name, repr(exc)[:200])
        finally:
            page.close()
    browser.close()
