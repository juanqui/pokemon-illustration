"""Tighten the SAM fox mask: remove green/blue background, fill interior holes."""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
plate=np.asarray(Image.open(ROOT/'work/plate.png').convert('RGB')).astype(int)
m=np.array(Image.open(ROOT/'work/fox_mask_0.png').convert('L'))>127
lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1)); m=lab==(np.argmax(sizes)+1)
R,G,B=plate[...,0],plate[...,1],plate[...,2]
# fox is orange/brown/cream/dark; reject green and blue background
notgreen=(G<=R+4); notblue=(B<=R+10)
keep=notgreen & notblue
m=m & keep
m=ndimage.binary_closing(m,iterations=2)
m=ndimage.binary_fill_holes(m)
lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1)); m=lab==(np.argmax(sizes)+1)
m=ndimage.binary_fill_holes(m)
m=ndimage.binary_dilation(m,iterations=1)
# do not touch the sticker corner
m[572:,1116:]=False
ys,xs=np.where(m); print('tight mask bbox',xs.min(),xs.max(),ys.min(),ys.max(),'area',m.sum())
Image.fromarray((m*255).astype(np.uint8)).save(ROOT/'work/fox_mask_final.png')
Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)).save(ROOT/'work/fox_mask_soft.png')
# visualization
vis=(plate*0.45).astype(np.uint8); green=np.zeros_like(vis); green[...,1]=255
vis[m]=(0.35*vis[m]+0.65*green[m]).astype(np.uint8)
Image.fromarray(vis).resize((1080,667),Image.LANCZOS).save(ROOT/'work/mask_vis.jpg',quality=93)
