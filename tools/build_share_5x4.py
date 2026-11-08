# -*- coding: utf-8 -*-
"""小程序分享图 5:4（1000×800）
沿用 v3 风格：极速建站、无 LOGO 图形 / 无 GOSITE / 无网址 / 无联系方式，
只呈现 399 元官网包年这一项服务。
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_shop_v3 as B  # noqa: E402  (复用配色、字体、渐变工具)

W, H = 1000, 800
img = B.gradient(W, H)

glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
g = ImageDraw.Draw(glow)
g.ellipse((700, -220, 1240, 320), fill=(255, 255, 255, 50))
g.ellipse((-220, 540, 320, 1040), fill=(80, 200, 255, 42))
img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(90)))

d = ImageDraw.Draw(img)
B.rounded(d, (36, 36, 964, 764), 36, (255, 255, 255, 246))

d.text((80, 78), "极速建站", font=B.font(36, True), fill=B.INK)
d.text((80, 126), "企业官网快上线服务", font=B.font(20), fill=B.MUTED)

d.text((80, 186), "企业官网包年", font=B.font(66, True), fill=B.INK)
d.text((80, 288), "¥", font=B.font(48, True), fill=B.BLUE)
d.text((132, 266), "399", font=B.font(120, True), fill=B.BLUE)
d.text((432, 340), "/ 年", font=B.font(32, True), fill=B.MUTED)

B.rounded(d, (80, 424, 920, 428), 2, (232, 240, 255))
d.text((80, 452), "纯静态官网 · 最快当天上线 · 全年代运营维护更新",
       font=B.font(27), fill=B.INK)

x = 80
for t in ["最快当天上线", "改稿当天发布", "设计满意再付款"]:
    w = d.textlength(t, font=B.font(24, True)) + 40
    B.rounded(d, (x, 520, x + w, 576), 28, (235, 244, 255))
    d.text((x + 20, 532), t, font=B.font(24, True), fill=B.BLUE)
    x += w + 16

d.text((80, 646), "399 元/年 · 仅限前 10 名且资料齐全",
       font=B.font(26, True), fill=B.PINK)
d.text((80, 706), "极速建站 · 企业官网包年", font=B.font(20), fill=B.MUTED)

out_png = os.path.join(B.OUT, "share-5x4.png")
out_jpg = os.path.join(B.OUT, "share-5x4.jpg")
img.convert("RGB").save(out_png, "PNG", optimize=True)
img.convert("RGB").save(out_jpg, "JPEG", quality=88, optimize=True)
print("share-5x4.png", os.path.getsize(out_png) // 1024, "KB")
print("share-5x4.jpg", os.path.getsize(out_jpg) // 1024, "KB")
