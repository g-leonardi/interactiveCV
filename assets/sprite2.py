#!/usr/bin/env python3
"""Generatore che rispecchia AL PIXEL il motore JS del Sprite Lab.
Uso: python3 sprite2.py '<json params>' out.png [scale]"""
import sys, json
from PIL import Image

W=H=80; CX=40

def hx(c):
    c=c.lstrip('#'); return (int(c[0:2],16),int(c[2:4],16),int(c[4:6],16),255)

SKINS=[['#d8b088','#c69a74','#e2bd95'],['#c99f78','#b98d66','#d6ad84'],['#b3855f','#9c704c','#c1966f']]
SHIRTS=[['#8ba3bb','#6f889f','#5c748c'],['#2c2f38','#1c1f26','#3a3f4a'],['#3f5a78','#2c4258','#213a52']]
HAIR_D=hx('4c443c'); HAIR_M=hx('8b8178'); HAIR_L=hx('c8ccd2')
BEARD_D=hx('332821'); BEARD_M=hx('6a5f55'); BEARD_L=hx('9a8f83')
TEE=hx('eef2f6'); TEE_SH=hx('d3dae1')

def ell(x,y,cx,cy,rx,ry):
    a=(x-cx)/rx; b=(y-cy)/ry; return a*a+b*b<=1.0

def gen(P):
    _s=[P['seed'] & 0xFFFFFFFF]
    def rnd():
        _s[0]=(_s[0]*1664525+1013904223)&0xFFFFFFFF; return _s[0]/4294967296.0

    sweepX=33+P['sweep']*0.9; topY=9-P['quiff']
    top_edge=lambda x: topY+0.058*(x-sweepX)*(x-sweepX)
    hairline=lambda x: P['hairline']+max(0.0,(abs(x-CX)-10))*0.4
    bRy=12.5+P['beard']*0.7; bCy=41.5+P['beard']*0.45
    face=lambda x,y: ell(x,y,CX,34,16,19)
    def hair(x,y):
        if 23<=x<=56 and top_edge(x)<=y<hairline(x): return True
        if ell(x,y,CX,31,19.5,20):
            if y<hairline(x): return True
            if (x<28 or x>52) and y<43: return True
        return False
    sideburn=lambda x,y: ((23<=x<=28) or (52<=x<=57)) and 27<=y<=45
    beard=lambda x,y: ((ell(x,y,CX,bCy,16.5,bRy) and y>=38) or sideburn(x,y)
                       or (38<=y<=43 and 30<=x<=50)) and 21<=x<=59
    neck=lambda x,y: 34<=x<=46 and 52<=y<=61
    shirt=lambda x,y: ell(x,y,CX,82,31,24) and y>=57
    tee=lambda x,y: 58<=y<=76 and abs(x-CX)<(y-56)*0.45

    sk=[hx(c) for c in SKINS[P['skin']]]; sh=[hx(c) for c in SHIRTS[P['shirt']]]
    SKIN,SKIN_SH,SKIN_HI=sk; SHIRT,SHIRT_SH,COLLAR=sh
    silverK=P['silver']/100.0; bsilverK=P['bsilver']/100.0

    img=Image.new('RGBA',(W,H),(0,0,0,0)); px=img.load()
    for y in range(H):
        for x in range(W):
            c=None
            if beard(x,y):
                r=rnd(); pM=0.10+0.30*bsilverK; pL=0.02+0.14*bsilverK
                c = BEARD_L if r<pL else (BEARD_M if r<pL+pM else BEARD_D)
            elif hair(x,y):
                hl=hairline(x); te=top_edge(x)
                top=max(0.0,min(1.0,(hl-y)/max(1.0,hl-te)))
                strand=int(x*1.15+y*0.35)%5; r=rnd()
                pL=(0.05+0.34*top*top)*(0.4+1.5*silverK); pM=0.20+0.10*top
                if strand==0: pL+=0.22
                if strand==2: pM+=0.15
                c = HAIR_L if r<pL else (HAIR_M if r<pL+pM else HAIR_D)
            elif face(x,y):
                c=SKIN
                if ell(x,y,29,38,5,6) or ell(x,y,51,38,5,6): c=SKIN_SH
                if ell(x,y,CX,40,2.4,4): c=SKIN_SH
            elif neck(x,y):
                c=SKIN_SH if y>58 else SKIN
            elif tee(x,y):
                c=TEE_SH if (x<CX-3 or x>CX+3) else TEE
            elif shirt(x,y):
                c=SHIRT_SH if (x<CX-8 or x>CX+8) else SHIRT
                if rnd()<0.10: c=SHIRT_SH
                if y<62 and abs(abs(x-CX)-9)<1.4: c=COLLAR
            if c: px[x,y]=c

    # --- overlays su griglia (eyebrows, eyes, glasses, smile) ---
    from PIL import ImageDraw
    dr=ImageDraw.Draw(img,'RGBA')
    def rect(x,y,w,h,col): dr.rectangle([x,y,x+w-1,y+h-1],fill=col)
    BROW=hx('3a2c22'); EYE=hx('2a2018'); METAL=(130,141,151,255)
    for x in range(25,38):
        yy=27-round((x-31)*(x-31)/40); rect(x,yy,1,2,BROW)
    for x in range(43,56):
        yy=27-round((x-49)*(x-49)/40); rect(x,yy,1,2,BROW)
    if P.get('blink'):
        for ex in (31,49):
            for x in range(ex-2,ex+3): px[x,35]=EYE   # palpebra chiusa
    else:
        for ex in (31,49):
            for y in range(32,37):
                for x in range(ex-2,ex+3):
                    if ell(x,y,ex,34,1.7,1.9): px[x,y]=EYE
            px[ex,33]=hx('eef3ff')
    gr=P['glass']; grY=gr*0.9
    for cx in (31.5,48.5):
        dr.ellipse([cx-gr,34-grY,cx+gr,34+grY],fill=(150,205,230,36),outline=METAL,width=1)
    dr.line([38.6,30.4,41.4,30.4],fill=METAL,width=1)
    dr.line([38.4,33.2,41.6,33.2],fill=METAL,width=1)
    dr.line([25,29.6,38.6,29.4],fill=METAL,width=1); dr.line([41.4,29.4,55,29.6],fill=METAL,width=1)
    dr.line([24,33,18,31],fill=METAL,width=1); dr.line([56,33,62,31],fill=METAL,width=1)
    dr.line([35,47,40,49,45,47],fill=hx('5a3d34'),width=1)
    return img

if __name__=='__main__':
    P=json.loads(sys.argv[1]); out=sys.argv[2]; scale=int(sys.argv[3]) if len(sys.argv)>3 else 8
    img=gen(P); img.resize((W*scale,H*scale),Image.NEAREST).save(out)
    print('saved',out)
