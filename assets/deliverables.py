#!/usr/bin/env python3
"""Sforna i deliverable dallo sprite finale: avatar puliti + tondo + idle animata."""
import json, sys
from PIL import Image, ImageDraw
from sprite2 import gen, W, H

P = json.loads(sys.argv[1])

# --- avatar trasparenti (nearest upscale) ---
base = gen(dict(P))
for s in (1,2,4):
    base.resize((W*s,H*s),Image.NEAREST).save(f'avatar_{W*s}.png')
print('avatar 80/160/320 ok')

# --- badge tondo 320 (disco scuro + sprite mascherato + anello cyan) ---
S=320
sprite=base.resize((W*4,H*4),Image.NEAREST)           # 320x320
mask=Image.new('L',(S,S),0); ImageDraw.Draw(mask).ellipse([8,8,S-8,S-8],fill=255)
badge=Image.new('RGBA',(S,S),(0,0,0,0))
ImageDraw.Draw(badge).ellipse([6,6,S-6,S-6],fill=(12,20,36,255))   # disco
clipped=Image.new('RGBA',(S,S),(0,0,0,0))
clipped.paste(sprite,(0,0),sprite)                    # sprite su trasparente
clipped.putalpha(Image.composite(clipped.split()[3],Image.new('L',(S,S),0),mask))
badge=Image.alpha_composite(badge,clipped)
ImageDraw.Draw(badge).ellipse([5,5,S-5,S-5],outline=(57,226,255,255),width=6)
badge.save('avatar_round_320.png')
print('badge tondo ok')

# --- idle animata (APNG trasparente): respiro + blink ---
def frame(dy=0, blink=False):
    pp=dict(P); pp['blink']=blink
    f=gen(pp)
    canv=Image.new('RGBA',(W,H),(0,0,0,0))
    canv.paste(f,(0,dy),f)
    return canv.resize((W*4,H*4),Image.NEAREST)

frames=[frame(0), frame(1), frame(0), frame(0,blink=True)]
durations=[900,700,260,140]     # ms: fermo, respiro giù, su, blink
frames[0].save('idle.png', save_all=True, append_images=frames[1:],
               duration=durations, loop=0, disposal=2, format='PNG')
# GIF fallback su fondo arcade (per compatibilità larga)
gframes=[]
bg=(12,18,32,255)
for fr in frames:
    b=Image.new('RGBA',fr.size,bg); b=Image.alpha_composite(b,fr)
    gframes.append(b.convert('P',palette=Image.ADAPTIVE))
gframes[0].save('idle.gif', save_all=True, append_images=gframes[1:],
                duration=durations, loop=0)
print('idle.png (APNG) + idle.gif ok')
