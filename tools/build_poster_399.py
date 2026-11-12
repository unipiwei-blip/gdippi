# -*- coding: utf-8 -*-
"""399 建站手机海报（1080×1920）。

依据 gd.ippi.com.cn 站点当前口径：399 元/年、标准价 998 元/年、
每月前 10 名顾客且资料齐全、最快当天上线、全年代运营维护更新。

三个底部变体：
  qr    —— 带官网网址二维码（扫码直达 https://gd.ippi.com.cn/）
  clean —— 无二维码、无网址、无联系方式
  url   —— 无二维码、保留官网网址（备选）
每版同时输出 PNG 与便于微信分享的 JPG。
"""
import math
import os

import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
OUT = os.path.join(ROOT, "assets", "poster")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1920
FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"
SITE = "https://gd.ippi.com.cn/"
DOMAIN = "gd.ippi.com.cn"

WHITE = (255, 255, 255)
PALE = (198, 220, 255)
GOLD = (255, 214, 102)
BLUE = (22, 104, 255)
INK = (12, 32, 72)


def f(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)


def center(d, y, text, fnt, fill):
    d.text(((W - d.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


def hexline(d, cx, cy, r, color, width=2):
    pts = [(cx + r * math.cos(math.radians(60 * k - 30)),
            cy + r * math.sin(math.radians(60 * k - 30))) for k in range(6)]
    d.line(pts + [pts[0]], fill=color, width=width, joint="curve")


def background():
    yy = np.linspace(0, 1, H)[:, None, None]
    xx = np.linspace(0, 1, W)[None, :, None]
    t = np.clip(0.55 * xx + 0.45 * yy, 0, 1)
    c1 = np.array([5, 18, 66], dtype=float)
    c2 = np.array([26, 74, 192], dtype=float)
    c3 = np.array([122, 44, 196], dtype=float)
    a = c1 + (c2 - c1) * np.clip(t / 0.5, 0, 1)
    b = c2 + (c3 - c2) * np.clip((t - 0.5) / 0.5, 0, 1)
    img = Image.fromarray(np.where(t < 0.5, a, b).astype("uint8"), "RGB").convert("RGBA")

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((540, -300, 1360, 520), fill=(70, 190, 255, 78))
    g.ellipse((-320, 860, 520, 1700), fill=(226, 21, 127, 58))
    g.ellipse((260, 260, 940, 940), fill=(130, 100, 255, 44))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(120)))

    # 半透明元素必须画在独立图层再合成，否则转成 RGB 时 alpha 被丢弃、半透明白变纯白
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for x in range(0, W, 72):
        d.line((x, 0, x, H), fill=(255, 255, 255, 9), width=1)
    for y in range(0, H, 72):
        d.line((0, y, W, y), fill=(255, 255, 255, 9), width=1)
    for r, a in ((210, 46), (150, 60), (92, 80)):
        hexline(d, 860, 300, r, (140, 210, 255, a), 3)
    d.ellipse((806, 246, 914, 354), fill=(120, 210, 255, 46))
    bars = [(0, 1740, 96, 180), (104, 1780, 62, 140), (174, 1700, 88, 220),
            (270, 1760, 70, 160), (348, 1668, 104, 252), (460, 1750, 66, 170),
            (534, 1710, 92, 210), (634, 1782, 58, 138), (700, 1690, 96, 230),
            (804, 1752, 74, 168), (886, 1720, 90, 200), (984, 1770, 96, 150)]
    for x, y, w, _h in bars:
        d.rectangle((x, y, x + w, H), fill=(4, 14, 48, 92))
    return Image.alpha_composite(img, ov)


def icon(d, kind, cx, cy):
    """卡片顶部简约线性图标。"""
    c = (140, 214, 255, 255)
    if kind == "bolt":
        d.polygon([(cx + 4, cy - 20), (cx - 12, cy + 3), (cx - 1, cy + 3),
                   (cx - 5, cy + 21), (cx + 13, cy - 4), (cx + 1, cy - 4)], fill=c)
    elif kind == "refresh":
        d.arc((cx - 18, cy - 18, cx + 18, cy + 18), 40, 320, fill=c, width=4)
        d.polygon([(cx + 12, cy - 20), (cx + 23, cy - 12), (cx + 11, cy - 5)], fill=c)
    elif kind == "shield":
        pts = [(cx, cy - 21), (cx + 18, cy - 13), (cx + 16, cy + 8),
               (cx, cy + 21), (cx - 16, cy + 8), (cx - 18, cy - 13)]
        d.line(pts + [pts[0]], fill=c, width=3, joint="curve")
        d.line((cx - 8, cy, cx - 1, cy + 7, cx + 10, cy - 7), fill=c, width=3, joint="curve")
    elif kind == "phone":
        d.rounded_rectangle((cx - 13, cy - 21, cx + 13, cy + 21), radius=5, outline=c, width=3)
        d.line((cx - 5, cy + 14, cx + 5, cy + 14), fill=c, width=3)
    elif kind == "pen":
        d.line((cx - 17, cy + 15, cx + 12, cy - 14), fill=c, width=4)
        d.polygon([(cx + 8, cy - 19), (cx + 18, cy - 9), (cx + 12, cy - 5)], fill=c)
        d.arc((cx - 20, cy - 2, cx + 4, cy + 22), 20, 160, fill=c, width=3)
    elif kind == "search":
        d.ellipse((cx - 17, cy - 19, cx + 7, cy + 5), outline=c, width=3)
        d.line((cx + 5, cy + 3, cx + 19, cy + 18), fill=c, width=4)


POINTS = [
    ("bolt", "最快当天上线", "资料齐备即可发布"),
    ("refresh", "改稿当天发布", "全年更新代运营"),
    ("shield", "纯静态更安全", "无后台数据库暴露面"),
    ("phone", "手机微信都好看", "多端自适应呈现"),
    ("pen", "设计满意再付款", "先看稿再定稿"),
    ("search", "搜索与 AI 可读", "标题描述地图配齐"),
]


def gradient_number(img, y, text, fnt):
    """用文字掩码把金→浅金渐变贴到主图上。"""
    w = int(fnt.getlength(text)) + 30
    h = 320
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((15, 0), text, font=fnt, fill=255)
    patch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(patch)
    for j in range(h):
        k = j / (h - 1)
        pd.line((0, j, w, j), fill=(255, int(232 - 42 * k), int(132 - 34 * k), 255))
    img.paste(patch, ((W - w) // 2, y), mask)


def common(img):
    logo = Image.open(os.path.join(ROOT, "assets", "img", "logo.png")).convert("RGBA")
    logo.thumbnail((100, 100), Image.LANCZOS)
    img.alpha_composite(logo, ((W - 100) // 2, 72))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    center(d, 180, "极站 GOSITE", f(46, True), WHITE)
    center(d, 238, "GDiis · 官网快上线 · 全年有人管", f(25), PALE)

    eyebrow = "企业官网包年 · 限时福利"
    ew = d.textlength(eyebrow, font=f(26, True)) + 76
    d.rounded_rectangle(((W - ew) / 2, 294, (W + ew) / 2, 354), radius=30,
                        fill=(255, 255, 255, 34), outline=(255, 255, 255, 80), width=2)
    center(d, 308, eyebrow, f(26, True), WHITE)

    gradient_number(ov, 366, "399", f(250, True))
    center(d, 670, "元 / 年   ·   企业官网包年", f(46, True), WHITE)
    center(d, 730, "纯静态官网整站 + 全年代运营维护更新", f(28), PALE)

    std = "标准价 998 元 / 年"
    sw = d.textlength(std, font=f(26))
    d.text(((W - sw) / 2, 782), std, font=f(26), fill=(214, 226, 248, 220))
    d.line(((W - sw) / 2, 798, (W + sw) / 2, 798), fill=(214, 226, 248, 200), width=2)
    badge = "每月前 10 名顾客 · 资料齐全"
    bw = d.textlength(badge, font=f(29, True)) + 80
    d.rounded_rectangle(((W - bw) / 2, 818, (W + bw) / 2, 878), radius=30, fill=(226, 21, 127, 238))
    center(d, 832, badge, f(29, True), WHITE)

    x0, y0, cw, ch, gap = 60, 900, 460, 180, 16
    for i, (kind, title, sub) in enumerate(POINTS):
        col, row = i % 2, i // 2
        x = x0 + col * (cw + gap)
        y = y0 + row * (ch + gap)
        d.rounded_rectangle((x, y, x + cw, y + ch), radius=26,
                            fill=(255, 255, 255, 30), outline=(255, 255, 255, 62), width=2)
        icon(d, kind, x + cw / 2, y + 42)
        d.text((x + (cw - d.textlength(title, font=f(30, True))) / 2, y + 78),
               title, font=f(30, True), fill=WHITE)
        d.text((x + (cw - d.textlength(sub, font=f(22))) / 2, y + 126),
               sub, font=f(22), fill=PALE)

    d.line((130, 1490, 950, 1490), fill=(255, 255, 255, 55), width=2)
    center(d, 1512, "纯静态官网 · 最快当天上线 · 全年有人管", f(28, True), WHITE)
    return Image.alpha_composite(img, ov)


def make_qr():
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H,
                       box_size=12, border=2)
    qr.add_data(SITE)
    qr.make(fit=True)
    im = qr.make_image(fill_color=(12, 32, 72), back_color="white").convert("RGB")
    return im.resize((196, 196), Image.NEAREST)


def footer(img, variant):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    x0, x1, y0, y1 = 60, 1020, 1564, 1900
    if variant == "qr":
        d.rounded_rectangle((x0, y0, x1, y1), radius=32, fill=(255, 255, 255, 246))
        ov.paste(make_qr().convert("RGBA"), ((W - 196) // 2, y0 + 14))
        center(d, y0 + 220, "扫码访问官网", f(25), (70, 95, 130, 255))
        center(d, y0 + 254, DOMAIN, f(34, True), (22, 104, 255, 255))
        center(d, y0 + 294, "399 元/年 · 每月前 10 名顾客且资料齐全", f(20), (110, 132, 165, 255))
    elif variant == "url":
        d.rounded_rectangle((x0, y0, x1, y1), radius=32,
                            fill=(8, 26, 78, 228), outline=(255, 255, 255, 70), width=2)
        center(d, y0 + 34, "官网了解详情", f(26), PALE)
        center(d, y0 + 82, DOMAIN, f(56, True), WHITE)
        center(d, y0 + 180, "399 元 / 年 · 企业官网包年", f(30, True), GOLD)
        center(d, y0 + 246, "纯静态官网 · 最快当天上线", f(24), PALE)
    else:
        d.rounded_rectangle((x0, y0, x1, y1), radius=32,
                            fill=(8, 26, 78, 228), outline=(255, 255, 255, 70), width=2)
        center(d, y0 + 34, "极站 GOSITE", f(50, True), WHITE)
        center(d, y0 + 116, "399 元 / 年", f(60, True), GOLD)
        center(d, y0 + 212, "企业官网包年 · 全年代运营维护更新", f(28), WHITE)
        center(d, y0 + 270, "官网快上线 · 全年有人管", f(24), PALE)
    return Image.alpha_composite(img, ov)


def main():
    names = {"qr": "poster-399-qr", "clean": "poster-399-clean", "url": "poster-399-url"}
    for variant, stem in names.items():
        img = background()
        img = common(img)
        img = footer(img, variant)
        rgb = img.convert("RGB")
        p_png = os.path.join(OUT, stem + ".png")
        p_jpg = os.path.join(OUT, stem + ".jpg")
        rgb.save(p_png, "PNG", optimize=True)
        rgb.save(p_jpg, "JPEG", quality=90, optimize=True, subsampling=0)
        print(stem, "|", rgb.size,
              "| PNG %.0fKB" % (os.path.getsize(p_png) / 1024),
              "| JPG %.0fKB" % (os.path.getsize(p_jpg) / 1024))


if __name__ == "__main__":
    main()
