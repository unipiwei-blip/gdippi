# -*- coding: utf-8 -*-
"""生成全站统一的微信分享固定图（400×400 JPG）。

源图为用户提供的商标图样，整张等比缩放到正方形画布内，不裁切内容、不生成新画面。
输出 JPEG 无 EXIF、单张 ≤100KB；源图保持不变。
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r"D:\项目管理\logo设计\logos\export-20260930\trademark\商标图样-图形-G标识.jpg"
OUT = os.path.join(ROOT, "assets", "img", "share-site.jpg")
SIZE = 400


def main():
    if not os.path.exists(SRC):
        raise SystemExit("找不到商标源图: " + SRC)
    src = Image.open(SRC).convert("RGB")
    canvas = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    fitted = src.copy()
    fitted.thumbnail((SIZE, SIZE), Image.LANCZOS)
    canvas.paste(fitted, ((SIZE - fitted.width) // 2, (SIZE - fitted.height) // 2))

    q = 85
    while True:
        canvas.save(OUT, "JPEG", quality=q, optimize=True, subsampling=0)
        if os.path.getsize(OUT) <= 100 * 1024 or q <= 70:
            break
        q -= 5
    check = Image.open(OUT)
    print("源图 %s %s -> %s" % (os.path.basename(SRC), src.size, OUT))
    print("输出 %s %s %dKB q=%d EXIF=%s" % (
        check.size, check.format, os.path.getsize(OUT) // 1024, q, bool(check.getexif())))


if __name__ == "__main__":
    main()
