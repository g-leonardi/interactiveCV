#!/usr/bin/env python3
"""Sprite pixel a CORPO INTERO animato: testa (da sprite2) + corpo + gambe + chitarra.
Frame: idle, blink, walk1..walk4, jump. Uso: python3 fullbody.py"""
import json
from PIL import Image, ImageDraw
from sprite2 import gen as gen_head

CFG = json.load(open('/Volumes/SAMSUNG_SO/Claude/Interactive CV/assets/config.json'))
W, H, CX = 48, 64, 24

def hx(c):
    c=c.lstrip('#'); return (int(c[0:2],16),int(c[2:4],16),int(c[4:6],16),255)

SHIRT=hx('8ba3bb'); SHIRT_SH=hx('6f889f'); COLLAR=hx('5c748c')
TEE=hx('eef2f6'); SKIN=hx('c99f78'); SKIN_SH=hx('b98d66')
DENIM=hx('355074'); DENIM_SH=hx('243a52'); SHOE=hx('14181f')
GTR_BODY=hx('17151c'); GTR_EDGE=hx('c46a1e'); GTR_NECK=hx('6b4a2a'); GTR_HEAD=hx('2a1f16')
STRING=hx('cfd6dc')

# --- teste (normale + blink), ritagliate identiche e scalate ---
HEAD_H = 32
_raw_n = gen_head(dict(CFG)).crop((15, 2, 65, 55))
_bb = _raw_n.getbbox()
def _mk(raw):
    im = raw.crop(_bb)
    hw = round(im.width * HEAD_H / im.height)
    return im.resize((hw, HEAD_H), Image.NEAREST)
_head_n = _mk(_raw_n)
_head_b = _mk(gen_head(dict(CFG, blink=True)).crop((15, 2, 65, 55)))

HEAD_BOTTOM = 27
HIP = 46

def draw_body(frame):
    img = Image.new('RGBA', (W, H), (0,0,0,0))
    d = ImageDraw.Draw(img, 'RGBA')
    head = _head_b if frame == 'blink' else _head_n

    def leg(hipx, footx, foot_y=60):
        d.line([hipx, HIP-1, footx, foot_y], fill=DENIM, width=5)
        d.line([hipx, HIP-1, footx, foot_y], fill=DENIM_SH, width=1)
        d.rectangle([footx-3, foot_y, footx+3, foot_y+3], fill=SHOE)

    # ---- GAMBE per frame ----
    if frame == 'walk1':   leg(20, 15); leg(28, 32)
    elif frame == 'walk2': leg(20, 22); leg(28, 27)
    elif frame == 'walk3': leg(20, 31); leg(28, 24)
    elif frame == 'walk4': leg(20, 22); leg(28, 27)
    elif frame == 'jump':  leg(20, 18, 54); leg(28, 30, 56)   # gambe raccolte
    elif frame == 'fire':  leg(18, 13); leg(30, 35)           # stance largo (power pose)
    else:                  leg(20, 19); leg(28, 29)           # idle/blink

    # ---- BRACCIO POSTERIORE (swing camminata / pugno alzato su 'fire') ----
    bh = {'walk1':(11,45),'walk2':(9,42),'walk3':(8,39),'walk4':(9,42),
          'jump':(8,34),'fire':(10,20)}.get(frame,(9,42))
    d.line([16, HEAD_BOTTOM+3, bh[0], bh[1]], fill=SHIRT_SH, width=5)
    d.ellipse([bh[0]-3, bh[1]-2, bh[0]+3, bh[1]+4], fill=SKIN)

    # ---- BUSTO ----
    d.rounded_rectangle([13, HEAD_BOTTOM, 35, HIP+1], radius=5, fill=SHIRT)
    d.rectangle([13, HEAD_BOTTOM, 17, HIP], fill=SHIRT_SH)
    d.rectangle([31, HEAD_BOTTOM, 35, HIP], fill=SHIRT_SH)
    d.polygon([(CX-6,HEAD_BOTTOM),(CX+6,HEAD_BOTTOM),(CX,HEAD_BOTTOM+9)], fill=TEE)
    d.line([CX-6,HEAD_BOTTOM, CX,HEAD_BOTTOM+9], fill=COLLAR, width=1)
    d.line([CX+6,HEAD_BOTTOM, CX,HEAD_BOTTOM+9], fill=COLLAR, width=1)

    # ---- CHITARRA a tracolla ----
    d.line([16, HEAD_BOTTOM+1, 34, HIP-2], fill=hx('3a2f22'), width=2)
    d.line([33, 43, 15, 30], fill=GTR_NECK, width=3)
    d.rectangle([12, 27, 16, 31], fill=GTR_HEAD)
    d.ellipse([30, 40, 44, 54], fill=GTR_BODY)
    d.ellipse([30, 40, 44, 54], outline=GTR_EDGE, width=1)
    d.ellipse([34, 45, 40, 51], outline=hx('2a2730'), width=1)
    d.line([33, 42, 16, 29], fill=STRING, width=1)

    # ---- BRACCIO ANTERIORE sulla chitarra ----
    hand = (37, 44) if frame != 'jump' else (37, 40)
    d.line([32, HEAD_BOTTOM+3, hand[0], hand[1]], fill=SHIRT, width=5)
    d.ellipse([hand[0]-3, hand[1]-1, hand[0]+3, hand[1]+5], fill=SKIN)

    # ---- TESTA sopra ----
    d.rectangle([CX-3, HEAD_BOTTOM-3, CX+3, HEAD_BOTTOM+1], fill=SKIN_SH)
    img.paste(head, (CX - head.width//2, 0), head)
    return img

if __name__ == '__main__':
    order = ['idle','blink','walk1','walk2','walk3','walk4','jump','fire']
    frames = {fr: draw_body(fr) for fr in order}
    for fr in order:
        frames[fr].resize((W*6, H*6), Image.NEAREST).save(f'fb_{fr}.png')
    sheet = Image.new('RGBA', (W*len(order)+ (len(order)+1)*4, H+8), (18,22,34,255))
    for i,fr in enumerate(order):
        sheet.paste(frames[fr], (4+i*(W+4), 4), frames[fr])
    sheet.resize((sheet.width*4, sheet.height*4), Image.NEAREST).save('fb_sheet.png')
    print('OK frames:', ', '.join(order))
