#!/usr/bin/env python3
"""Innesto v4: camminata più lenta, oscillazione (sway) e posa 'spara'."""
import base64, io
from fullbody import draw_body

PRISTINE = '/Users/giuseppeleonardi/.claude/projects/-Users-giuseppeleonardi/927967e7-e41b-4f64-b58e-b14d4228e1ce/tool-results/artifact-c27ccaa5-1783467678-b921.html'
OUT = '/Volumes/SAMSUNG_SO/Claude/Interactive CV/index.html'

def uri(fr):
    im = draw_body(fr); buf = io.BytesIO(); im.save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

U = {fr: uri(fr) for fr in ('idle','blink','walk1','walk2','walk3','walk4','jump','fire')}

h = open(PRISTINE, encoding='utf-8').read()
i = h.find('<title>Giuseppe Leonardi'); assert i > 0
h = h[i:].rstrip()
for t in ('</html>','</body>'):
    if h.endswith(t): h = h[:-len(t)].rstrip()

# 1) variabili sprite
a1 = '  "use strict";'; assert h.count(a1) == 1
decls = '\n'.join('  var PEO_%s="%s";' % (k.upper(), v) for k, v in U.items())
h = h.replace(a1, a1 + '\n' + decls, 1)

# 2) player.innerHTML
old_p = '''  player.innerHTML='<div class="head"></div><div class="torso"></div><div class="gtr"></div><div class="lgL"></div><div class="lgR"></div>';'''
new_p = '''  player.innerHTML='<div class="peo"></div><div class="gtr"></div><div class="lgL"></div><div class="lgR"></div>';'''
assert old_p in h; h = h.replace(old_p, new_p, 1)

# 3) stato "in aria"
old_j = "    player.classList.toggle('walk', moving && !reduce);"
new_j = "    player.classList.toggle('walk', moving && !reduce && onGround);\n    player.classList.toggle('air', !onGround && !reduce);"
assert old_j in h; h = h.replace(old_j, new_j, 1)

# 3b) piedi SOPRA le piattaforme (superficie superiore alla quota d'appoggio)
old_plat = "d.className='platform'; d.style.left=p.x+'px'; d.style.width=p.w+'px'; d.style.bottom=(GB+p.alt)+'px';"
new_plat = "d.className='platform'; d.style.left=p.x+'px'; d.style.width=p.w+'px'; d.style.bottom=(GB+p.alt-14)+'px';"
assert old_plat in h, "platform build non trovato"; h = h.replace(old_plat, new_plat, 1)

# 3c) TEETER ai bordi: ti fermi un istante sul ciglio invece di cadere subito
h = h.replace('  var unlockedCount=0, checkpoint=120, bolts=[];',
              '  var unlockedCount=0, checkpoint=120, bolts=[], teeter=0;', 1)
old_mv = '      var tv=dir*speed; vx+=(tv-vx)*0.2; if(Math.abs(vx)<0.05) vx=0;'
new_mv = '      var wasGround=onGround, edgePx=px;\n' + old_mv
assert old_mv in h; h = h.replace(old_mv, new_mv, 1)
old_cy = '      if(onGround){ coyote=8; } else if(coyote>0){ coyote--; }'
new_cy = ('      if(!onGround && wasGround && vy<=0 && teeter<12){ px=edgePx; py=prevPy; vy=0; onGround=true; teeter++; }\n'
          '      else if(onGround){ teeter=0; }\n' + old_cy)
assert old_cy in h; h = h.replace(old_cy, new_cy, 1)

# 3d) bandierina SYSDIG (con spiegazione via jobForSign->CVJOBS.sysdig)
old_sig = "{x:5150,yr:'',lb:'Personal Projects'} ];"
new_sig = "{x:5150,yr:'',lb:'Personal Projects'}, {x:5830,yr:'2026',lb:'SYSDIG'} ];"
assert old_sig in h, "SIGNS non trovato"; h = h.replace(old_sig, new_sig, 1)

# 4b) download PDF robusto (Blob invece di data-URI gigante)
old_pdf = '''document.getElementById('dlPdf').addEventListener('click', function(){ var a=document.createElement('a'); a.href='data:application/pdf;base64,'+CV_PDF_B64; a.download='Giuseppe-Leonardi-CV.pdf'; document.body.appendChild(a); a.click(); setTimeout(function(){ a.remove(); },100); });'''
new_pdf = '''document.getElementById('dlPdf').addEventListener('click', function(){ try{ var bin=atob(CV_PDF_B64),n=bin.length,arr=new Uint8Array(n); for(var i=0;i<n;i++)arr[i]=bin.charCodeAt(i); var b=new Blob([arr],{type:'application/pdf'}),url=URL.createObjectURL(b); var a=document.createElement('a'); a.href=url; a.download='Giuseppe-Leonardi-CV.pdf'; document.body.appendChild(a); a.click(); setTimeout(function(){ a.remove(); URL.revokeObjectURL(url); },300); }catch(e){ window.open('data:application/pdf;base64,'+CV_PDF_B64,'_blank'); } });'''
assert old_pdf in h, "handler dlPdf non trovato"
h = h.replace(old_pdf, new_pdf, 1)

# 4) CSS
anchor = '  @keyframes stepA{50%{height:9px}} @keyframes stepB{50%{height:9px}}'
assert anchor in h
css = anchor + '''
  /* --- Peo sprite corpo intero animato (v4: sway + camminata lenta + spara) --- */
  #player{width:30px; height:52px;}
  #player .peo{position:absolute; left:-5px; bottom:-1px; width:40px; height:53px;
    image-rendering:pixelated; z-index:2; pointer-events:none; transform-origin:50%% 100%%;
    background-size:100%% 100%%; background-repeat:no-repeat; background-image:url(%(idle)s);
    filter:drop-shadow(0 2px 0 rgba(0,0,0,.45));
    animation:peoidle 4.6s steps(1) infinite, peosway 3.4s ease-in-out infinite;}
  #player .head,#player .torso,#player .lgL,#player .lgR,#player .gtr{display:none}
  @keyframes peoidle{0%%,95%%{background-image:url(%(idle)s)} 96%%,99%%{background-image:url(%(blink)s)} 100%%{background-image:url(%(idle)s)}}
  @keyframes peosway{0%%{transform:translateY(0) rotate(-2.2deg)} 25%%{transform:translateY(-1px) rotate(0deg)} 50%%{transform:translateY(0) rotate(2.2deg)} 75%%{transform:translateY(-1px) rotate(0deg)} 100%%{transform:translateY(0) rotate(-2.2deg)}}
  #player.walk .peo{animation:peowalk .64s steps(1) infinite, peowalkbob .32s ease-in-out infinite;}
  @keyframes peowalk{0%%{background-image:url(%(walk1)s)} 25%%{background-image:url(%(walk2)s)} 50%%{background-image:url(%(walk3)s)} 75%%{background-image:url(%(walk4)s)}}
  @keyframes peowalkbob{0%%,100%%{transform:translateY(0) rotate(-1.2deg)} 50%%{transform:translateY(-1.5px) rotate(1.2deg)}}
  #player.air .peo{animation:none; background-image:url(%(jump)s); transform:translateY(-1px) rotate(0deg);}
  #player.fire .peo{animation:none; background-image:url(%(fire)s); transform:rotate(-9deg) translateY(-1px);
    filter:brightness(1.4) drop-shadow(0 0 7px var(--cyan));}''' % U
h = h.replace(anchor, css, 1)

open(OUT, 'w', encoding='utf-8').write(h)
print('PATCH v4 OK · bytes', len(h))
