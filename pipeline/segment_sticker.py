import numpy as np
from PIL import Image
from segment_anything import sam_model_registry, SamPredictor
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
src=Image.open(ROOT/'projects/vulpix-30th/source/card.png').convert('RGB')
sam=sam_model_registry['vit_b'](checkpoint=str(ROOT/'work/sam_vit_b.pth')).to('cpu')
p=SamPredictor(sam); p.set_image(np.array(src))
# sticker around x575..710, y385..505; point on the face, box around the decal
masks,scores,_=p.predict(point_coords=np.array([[640,435]]),point_labels=np.array([1]),
                         box=np.array([550,360,730,520]),multimask_output=True)
for i,(m,s) in enumerate(zip(masks,scores)):
    print(i, 'area',int(m.sum()),'score',float(s))
    out=src.copy(); ov=Image.new('RGB',src.size,(0,255,0))
    out=Image.composite(ov,out,Image.fromarray((m*120).astype(np.uint8)))
    out.save(ROOT/f'work/sticker_overlay_{i}.png')
    Image.fromarray((m*255).astype(np.uint8)).save(ROOT/f'work/sticker_mask_{i}.png')
