# -*- coding: utf-8 -*-
"""本地预览校验：截取桌面首页 / 内页 / 手机端首屏"""
import os
from playwright.sync_api import sync_playwright

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
OUT = os.path.join(ROOT, ".tmp", "preview")
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def url(name):
    return "file:///" + os.path.join(ROOT, name).replace("\\", "/")


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=EDGE, headless=True,
                                args=["--no-sandbox", "--disable-gpu"])
    # 桌面首屏
    for name, page_name in [("home", "index.html"), ("pricing", "pricing.html"),
                            ("miniapp", "miniprogram.html"), ("cases", "cases.html"),
                            ("website", "website.html"), ("service", "service.html"),
                            ("contact", "contact.html"), ("sitemap", "sitemap.html")]:
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url(page_name), wait_until="load")
        page.wait_for_timeout(900)
        page.screenshot(path=os.path.join(OUT, name + "-top.png"))
        if name == "home":
            h = page.evaluate("document.body.scrollHeight")
            print("home page height:", h)
            for ratio, label in [(0.14, "home-mid"), (0.32, "home-low"),
                                 (0.58, "home-cases"), (0.76, "home-cta"),
                                 (0.97, "home-footer")]:
                page.evaluate("window.scrollTo(0, %d)" % int(h * ratio))
                page.wait_for_timeout(700)
                page.screenshot(path=os.path.join(OUT, label + ".png"))
        if name != "home":
            h = page.evaluate("document.body.scrollHeight")
            ratios = [(0.08, "why"), (0.20, "mid"), (0.36, "cards")] if name == "website" else ([(0.10, "plans"), (0.24, "mid")] if name == "pricing" else [(0.24, "mid")])
            for ratio, label in ratios:
                page.evaluate("window.scrollTo(0, %d)" % int(h * ratio))
                page.wait_for_timeout(700)
                page.screenshot(path=os.path.join(OUT, name + "-" + label + ".png"))
        print("OK", name, "links:", page.locator("a").count())
        page.close()
    # 手机端
    page = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    page.goto(url("index.html"), wait_until="load")
    page.wait_for_timeout(900)
    page.screenshot(path=os.path.join(OUT, "mobile-top.png"))
    page.evaluate("window.scrollTo(0, 900)")
    page.wait_for_timeout(700)
    page.screenshot(path=os.path.join(OUT, "mobile-mid.png"))
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(700)
    page.screenshot(path=os.path.join(OUT, "mobile-footer.png"))
    print("OK mobile, horizontal overflow:",
          page.evaluate("document.documentElement.scrollWidth > window.innerWidth"))
    page.close()
    browser.close()
