# -*- coding: utf-8 -*-
"""从案例详情页已有封面中心裁切出 400×400 微信分享方图。

只做裁切与缩放，不生成新画面；原封面保持不变；输出 JPEG 无 EXIF、单张 ≤100KB。
"""
import glob
import os

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES_DIR = os.path.join(ROOT, "assets", "cases")


def main():
    srcs = sorted(glob.glob(os.path.join(CASES_DIR, "case-*.png")))
    print("封面数:", len(srcs))
    for src in srcs:
        stem = os.path.splitext(os.path.basename(src))[0]
        short = stem[len("case-"):]
        out = os.path.join(CASES_DIR, "share-%s.jpg" % short)
        im = Image.open(src).convert("RGB")
        square = ImageOps.fit(im, (400, 400), Image.LANCZOS, centering=(0.5, 0.5))
        q = 85
        while True:
            # 不传 exif 参数，新建图像自然不带 EXIF
            square.save(out, "JPEG", quality=q, optimize=True, subsampling=0)
            if os.path.getsize(out) <= 100 * 1024 or q <= 70:
                break
            q -= 5
        check = Image.open(out)
        print("%-26s -> %-24s %s %s %dKB q=%d EXIF=%s" % (
            os.path.basename(src), os.path.basename(out), check.size,
            check.format, os.path.getsize(out) // 1024, q, bool(check.getexif())))


if __name__ == "__main__":
    main()
