"""Exact 617x383 source art window + sticker on a gray 736x1024 canvas."""
import numpy as np
from PIL import Image
from scipy import ndimage
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
src=Image.open(ROOT/'assets/source-card.png').convert('RGB')
W,H=736,1024; content=(66,101,683,484)
mask=np.array(Image.open(ROOT/'work/sticker_mask_1.png').convert('L'))>127
mask=ndimage.binary_fill_holes(ndimage.binary_dilation(mask,iterations=3))
Image.fromarray((mask*255).astype(np.uint8)).save(ROOT/'work/sticker_mask_final.png')
canvas=Image.new('RGB',(W,H),(128,128,128)); canvas.paste(src.crop(content),(content[0],content[1]))
m=np.zeros((H,W),bool); m[:mask.shape[0],:mask.shape[1]]=mask
s=np.zeros((H,W,3),np.uint8); s[:src.height,:src.width]=np.array(src)
a=np.array(canvas); a[m]=s[m]; canvas=Image.fromarray(a)
canvas.save(ROOT/'work/content_canvas_gray.png')
km=Image.new('L',(W,H),0); km.paste(Image.new('L',(content[2]-content[0],content[3]-content[1]),255),(content[0],content[1]))
km=Image.fromarray(np.maximum(np.array(km),np.array(Image.fromarray((m*255).astype(np.uint8)))))
km.save(ROOT/'work/content_known_mask.png')
print('content',content,'size',content[2]-content[0],content[3]-content[1])
