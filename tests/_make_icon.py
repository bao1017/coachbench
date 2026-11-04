# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os
outdir = r"C:\Users\陈硕腾\Desktop\app"
for size in (192, 512):
    img = Image.new("RGBA", (size,size), (7,11,26,255))
    d = ImageDraw.Draw(img)
    # 红底圆角方块
    pad = size//10
    d.rounded_rectangle([pad,pad,size-pad,size-pad], radius=size//6, fill=(181,58,46,255))
    # "台" 字
    try:
        font = ImageFont.truetype("msyhbd.ttc", int(size*0.5))
    except:
        font = ImageFont.load_default()
    bbox = d.textbbox((0,0), "台", font=font)
    w = bbox[2]-bbox[0]; h = bbox[3]-bbox[1]
    d.text(((size-w)/2 - bbox[0], (size-h)/2 - bbox[1]), "台", font=font, fill=(251,249,243,255))
    img.save(os.path.join(outdir, f"icon-{size}.png"))
print("ok")
