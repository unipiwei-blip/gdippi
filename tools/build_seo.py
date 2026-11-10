# -*- coding: utf-8 -*-
"""生成 SEO 与 GitHub Pages 发布文件：分享图 / sitemap.xml / robots.txt / CNAME / .nojekyll"""
import os
import datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
SITE = "https://gd.ippi.com.cn/"
TODAY = datetime.date.today().isoformat()

PAGES = [
    ("", "1.0", "daily"),
    ("website.html", "0.9", "weekly"),
    ("miniprogram.html", "0.9", "weekly"),
    ("cases.html", "0.8", "weekly"),
    ("service.html", "0.8", "weekly"),
    ("pricing.html", "0.9", "weekly"),
    ("contact.html", "0.7", "monthly"),
    ("sitemap.html", "0.5", "monthly"),
]
PAGES += [("case-shanghui.html", "0.7", "monthly"), ("case-cailie.html", "0.7", "monthly"), ("case-baydea.html", "0.7", "monthly"), ("case-jianzhuo.html", "0.7", "monthly"), ("case-guanxiang.html", "0.7", "monthly"), ("case-niling.html", "0.7", "monthly"), ("case-leiyiming.html", "0.7", "monthly")]

FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_REG = "C:/Windows/Fonts/msyh.ttc"


def make_og_image():
    W, H = 1200, 630
    xx = np.linspace(0, 1, W)[None, :, None]
    yy = np.linspace(0, 1, H)[:, None, None]
    t = np.clip(0.72 * xx + 0.28 * yy, 0, 1)
    c1 = np.array([10, 55, 180], dtype=float)
    c2 = np.array([105, 70, 235], dtype=float)
    c3 = np.array([214, 30, 125], dtype=float)
    a = c1 + (c2 - c1) * np.clip(t / 0.55, 0, 1)
    b = c2 + (c3 - c2) * np.clip((t - 0.55) / 0.45, 0, 1)
    arr = np.where(t < 0.55, a, b).clip(0, 255).astype("uint8")
    img = Image.fromarray(arr, "RGB").convert("RGBA")

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((740, -200, 1340, 400), fill=(255, 255, 255, 52))
    gd.ellipse((-180, 340, 420, 900), fill=(80, 200, 255, 46))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(90)))

    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((70, 64, 1130, 566), radius=34, fill=(255, 255, 255, 240))
    img = Image.alpha_composite(img, card)

    d = ImageDraw.Draw(img)
    for r in (168, 124, 82):
        d.ellipse((962 - r, 300 - r, 962 + r, 300 + r), outline=(26, 107, 255, 34), width=3)

    logo = Image.open(os.path.join(ROOT, "assets", "img", "logo.png")).convert("RGBA")
    logo.thumbnail((96, 96), Image.LANCZOS)
    img.alpha_composite(logo, (112, 108))

    f1 = ImageFont.truetype(FONT_BOLD, 64)
    f2 = ImageFont.truetype(FONT_REG, 30)
    f3 = ImageFont.truetype(FONT_BOLD, 25)
    f4 = ImageFont.truetype(FONT_REG, 21)
    d.text((112, 232), "极站 GOSITE", font=f1, fill=(10, 30, 60, 255))
    d.text((112, 322), "纯静态官网 · 最快当天上线 · 全年代运营", font=f2, fill=(70, 95, 130, 255))
    d.line((112, 382, 1088, 382), fill=(220, 232, 250, 255), width=2)
    d.text((112, 408), "399 元/年 官网包年  ｜  设计满意再付款", font=f3, fill=(26, 107, 255, 255))
    d.text((112, 492), "gd.ippi.com.cn", font=f4, fill=(120, 140, 170, 255))

    out = os.path.join(ROOT, "assets", "img", "og-image.png")
    img.convert("RGB").save(out, "PNG", optimize=True)
    print("og-image.png", img.size)


def write_text(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("written", name)


def main():
    make_og_image()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority, freq in PAGES:
        lines.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod>"
                     "<changefreq>%s</changefreq><priority>%s</priority></url>"
                     % (SITE, path, TODAY, freq, priority))
    lines.append("</urlset>")
    write_text("sitemap.xml", "\n".join(lines) + "\n")
    write_text("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % SITE)
    write_text("CNAME", "gd.ippi.com.cn\n")
    write_text(".nojekyll", "")


if __name__ == "__main__":
    main()
