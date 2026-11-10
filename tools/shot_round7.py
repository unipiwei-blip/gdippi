# -*- coding: utf-8 -*-
"""第七轮视觉校验：7 个案例的卡片、索引、多端实拍与页脚友情链接"""
import os
from playwright.sync_api import sync_playwright

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
OUT = os.path.join(ROOT, ".tmp", "preview")
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def url(name):
    return "file:///" + os.path.join(ROOT, name).replace("\\", "/")


def ready(pg):
    pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    pg.evaluate("document.querySelectorAll('img').forEach(i=>{i.loading='eager';i.src=i.src})")
    pg.wait_for_timeout(1400)


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EDGE, headless=True,
                          args=["--no-sandbox", "--disable-gpu"])

    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(url("cases.html"), wait_until="load")
    pg.wait_for_timeout(700)
    ready(pg)
    print("案例卡:", pg.locator(".case-card").count(),
          "| 索引链接:", pg.locator(".case-index a").count(),
          "| 多端截图:", pg.locator(".gallery-grid .shot").count())
    pg.locator(".case-index").screenshot(path=os.path.join(OUT, "r7-index.png"))
    pg.locator(".grid.g3").first.screenshot(path=os.path.join(OUT, "r7-cards.png"))
    pg.locator(".gallery-item").first.screenshot(path=os.path.join(OUT, "r7-gallery.png"))
    pg.locator(".footer-links").screenshot(path=os.path.join(OUT, "r7-friends.png"))
    pg.close()

    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(url("index.html"), wait_until="load")
    pg.wait_for_timeout(700)
    ready(pg)
    print("首页案例卡:", pg.locator(".case-card").count())
    pg.locator("section:has(.case-card)").first.screenshot(path=os.path.join(OUT, "r7-home-cases.png"))
    pg.close()

    pg = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    pg.goto(url("cases.html"), wait_until="load")
    pg.wait_for_timeout(700)
    ready(pg)
    pg.locator(".grid.g3").first.screenshot(path=os.path.join(OUT, "r7-cards-mobile.png"))
    print("手机端案例卡:", pg.locator(".case-card").count())
    pg.close()
    b.close()
