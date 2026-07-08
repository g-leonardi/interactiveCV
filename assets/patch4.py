#!/usr/bin/env python3
"""Innesto v4+v5: sprite corpo intero + audio arcade, schermata vittoria, sfondo deep-space."""
import base64, io
from fullbody import draw_body

PRISTINE = '/Users/giuseppeleonardi/.claude/projects/-Users-giuseppeleonardi/927967e7-e41b-4f64-b58e-b14d4228e1ce/tool-results/artifact-c27ccaa5-1783467678-b921.html'
OUT = '/Volumes/SAMSUNG_SO/Claude/Interactive CV/public/index.html'

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

# 3e) SISTEMA 3 CUORI (anni '90): bug/burrone = -1 cuore, invuln 0.5s flicker, no cura
h = h.replace('      <div class="mem" id="bugCount" style="color:var(--magenta)">\U0001f41b BUGS 0</div>',
              '      <div class="mem" id="bugCount" style="color:var(--magenta)">\U0001f41b BUGS 0</div>\n      <div class="mem" id="lives" style="letter-spacing:3px;font-size:16px;margin-top:2px"></div>', 1)
h = h.replace('  var bugs=[], bugKills=0, invuln=0;',
              '  var bugs=[], bugKills=0, invuln=0, hearts=3;', 1)
old_dr = ('  var overEl=document.getElementById(\'over\');\n'
          '  function die(){ if(dead) return; dead=true; keysDown.left=keysDown.right=0; setDir(); overEl.classList.remove(\'hide\'); }\n'
          '  function respawn(){ dead=false; overEl.classList.add(\'hide\'); px=checkpoint; py=170; vy=0; vx=0; }')
new_dr = ('  var overEl=document.getElementById(\'over\');\n'
          '  function renderHearts(){ var el=document.getElementById(\'lives\'); if(!el) return; var s=\'\'; for(var i=0;i<3;i++){ s+=\'<span style="color:\'+(i<hearts?\'#ff5c8a\':\'#3a2f52\')+\';text-shadow:\'+(i<hearts?\'0 0 8px #ff5c8a\':\'none\')+\'">\\u2665</span>\'; } el.innerHTML=s; }\n'
          '  function flick(ms){ player.classList.add(\'hurt\'); setTimeout(function(){ player.classList.remove(\'hurt\'); }, ms||500); }\n'
          '  function loseHeart(){ if(hearts>0) hearts--; renderHearts(); }\n'
          '  function die(){ if(dead) return; dead=true; keysDown.left=keysDown.right=0; setDir(); overEl.classList.remove(\'hide\'); }\n'
          '  function respawn(){ dead=false; overEl.classList.add(\'hide\'); hearts=3; renderHearts(); px=checkpoint; py=170; vy=0; vx=0; invuln=40; flick(500); }\n'
          '  renderHearts();')
assert old_dr in h, "blocco die/respawn non trovato"; h = h.replace(old_dr, new_dr, 1)
# pit fall -> perdi un cuore + checkpoint (game over solo a 0)
h = h.replace('      if(py<DEATH){ die(); }',
              '      if(py<DEATH){ if(invuln<=0){ loseHeart(); if(hearts<=0){ die(); } else { px=checkpoint; py=180; vy=0; vx=0; invuln=45; flick(600); toast(\'\U0001f573️ CADUTO\',\'-1 \\u2665 \\u00b7 dal checkpoint\'); } } else if(hearts<=0){ die(); } }', 1)
# bug collision -> perdi un cuore
old_bug = "      if(invuln<=0 && onGround && py<30 && Math.abs(px-b.x)<22){ var kn=(px<b.x?-1:1); px+=kn*24; vx=kn*3.5; invuln=48; player.classList.add('hurt'); setTimeout(function(){ player.classList.remove('hurt'); },520); }"
new_bug = "      if(invuln<=0 && onGround && py<30 && Math.abs(px-b.x)<22){ var kn=(px<b.x?-1:1); px+=kn*24; vx=kn*3.5; invuln=36; flick(500); loseHeart(); toast('\U0001f41b AHIA!','-1 \\u2665'); if(hearts<=0) die(); }"
assert old_bug in h, "collisione bug non trovata"; h = h.replace(old_bug, new_bug, 1)

# 3f) testi tutorial aggiornati (niente piu 'fall = full CV instant')
h = h.replace('grab a \U0001f511 then press ↑ at its cabinet · fall = full CV',
              'grab a \U0001f511 then press ↑ at its cabinet · ♥♥♥ bugs & pits cost a heart', 1)
h = h.replace('Fall in a pit? You get the <b>full CV</b> instantly — no skill required.',
              'You start with <b>3 ♥</b> — bugs and pits each cost one (pits drop you at the last checkpoint). Out of hearts? You still get the <b>full CV</b> — button top-right, anytime.', 1)

# 4a) download MD robusto (fallback a nuova scheda se il download è bloccato)
old_dlt = '''  function dlText(name,text,type){ var b=new Blob([text],{type:type}); var a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=name; document.body.appendChild(a); a.click(); setTimeout(function(){ a.remove(); URL.revokeObjectURL(a.href); },100); }'''
new_dlt = '''  function dlText(name,text,type){ try{ var b=new Blob([text],{type:type}),url=URL.createObjectURL(b); var a=document.createElement('a'); a.href=url; a.download=name; a.rel='noopener'; document.body.appendChild(a); a.click(); setTimeout(function(){ a.remove(); URL.revokeObjectURL(url); },400); }catch(e){ window.open('data:'+type+';charset=utf-8,'+encodeURIComponent(text),'_blank'); } }'''
assert old_dlt in h, "dlText non trovato"; h = h.replace(old_dlt, new_dlt, 1)

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

# ============================================================
#  v5 — AUDIO ARCADE + SCHERMATA VITTORIA + SFONDO DEEP-SPACE
# ============================================================

# 5a) modulo audio WebAudio (nessun file esterno → CSP-safe), dopo la var reduce
a_red = "  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;"
assert a_red in h, "ancora 'reduce' non trovata"
audio_js = a_red + '''
  // ---- audio (WebAudio synth · niente file esterni · CSP-safe) ----
  var AUDIO={ctx:null,muted:false,master:null};
  function audioInit(){ if(AUDIO.ctx) return; try{ var C=window.AudioContext||window.webkitAudioContext; if(!C) return; AUDIO.ctx=new C(); AUDIO.master=AUDIO.ctx.createGain(); AUDIO.master.gain.value=0.22; AUDIO.master.connect(AUDIO.ctx.destination); }catch(e){} }
  function beep(freq,dur,type,vol,slideTo){ if(AUDIO.muted||!AUDIO.ctx) return; var c=AUDIO.ctx,t=c.currentTime; var o=c.createOscillator(),g=c.createGain(); o.type=type||'square'; o.frequency.setValueAtTime(freq,t); if(slideTo) o.frequency.exponentialRampToValueAtTime(slideTo,t+dur*0.9); g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(vol||0.3,t+0.008); g.gain.exponentialRampToValueAtTime(0.0001,t+dur); o.connect(g); g.connect(AUDIO.master); o.start(t); o.stop(t+dur+0.03); }
  function sfx(name){ if(AUDIO.muted||!AUDIO.ctx) return;
    if(name==='jump'){ beep(340,0.16,'square',0.26,720); }
    else if(name==='fire'){ beep(900,0.12,'sawtooth',0.20,170); }
    else if(name==='key'){ beep(660,0.08,'square',0.28); setTimeout(function(){beep(990,0.13,'square',0.28);},80); }
    else if(name==='bug'){ beep(220,0.18,'square',0.28,55); }
    else if(name==='hurt'){ beep(180,0.26,'sawtooth',0.30,48); }
    else if(name==='open'){ beep(520,0.07,'triangle',0.24); setTimeout(function(){beep(784,0.14,'triangle',0.24);},75); } }
  function fanfare(){ if(AUDIO.muted||!AUDIO.ctx) return; var ns=[523,659,784,1047,880,1319]; for(var i=0;i<ns.length;i++){ (function(f,j){ setTimeout(function(){ beep(f,0.24,'square',0.26); beep(f/2,0.24,'triangle',0.10); }, j*150); })(ns[i],i); } }'''
h = h.replace(a_red, audio_js, 1)

# 5b) pulsante mute nell'HUD (prima di FULL CV)
old_cv = '      <button class="cvbtn" id="cvBtn">☰ FULL CV</button>'
new_cv = '      <button class="cvbtn" id="muteBtn" title="Sound on/off" aria-label="Toggle sound">\U0001f50a</button>\n' + old_cv
assert old_cv in h, "bottone cvBtn non trovato"; h = h.replace(old_cv, new_cv, 1)

# 5c) begin(): sblocca l'audio al primo gesto + handler del mute
old_begin = ("  document.getElementById('startBtn').addEventListener('click', begin);\n"
             "  function begin(){ if(started) return; started=true; document.getElementById('start').classList.add('hide'); }")
new_begin = ("  document.getElementById('startBtn').addEventListener('click', begin);\n"
             "  function begin(){ if(started) return; started=true; document.getElementById('start').classList.add('hide'); audioInit(); if(AUDIO.ctx && AUDIO.ctx.state==='suspended') AUDIO.ctx.resume(); }\n"
             "  (function(){ var mb=document.getElementById('muteBtn'); if(!mb) return; mb.addEventListener('click', function(){ audioInit(); AUDIO.muted=!AUDIO.muted; if(!AUDIO.muted && AUDIO.ctx && AUDIO.ctx.state==='suspended') AUDIO.ctx.resume(); mb.textContent=AUDIO.muted?'\U0001f507':'\U0001f50a'; mb.style.opacity=AUDIO.muted?'0.5':'1'; if(!AUDIO.muted) sfx('key'); }); })();")
assert old_begin in h, "begin() non trovato"; h = h.replace(old_begin, new_begin, 1)

# 5d) hook SFX su salto / fuoco / chiave / bug / apertura cabinato / danno
hooks = [
  ("      if(jbuf>0 && coyote>0){ vy=JUMP; onGround=false; coyote=0; jbuf=0; } else if(jbuf>0){ jbuf--; }",
   "      if(jbuf>0 && coyote>0){ vy=JUMP; onGround=false; coyote=0; jbuf=0; sfx('jump'); } else if(jbuf>0){ jbuf--; }"),
  ("  function fire(){ if(!started||paused()||!hasGuitar||fireCD>0) return; fireCD=15;",
   "  function fire(){ if(!started||paused()||!hasGuitar||fireCD>0) return; fireCD=15; sfx('fire');"),
  ("  function collectKey(k){ k.got=true;",
   "  function collectKey(k){ k.got=true; sfx('key');"),
  ("  function killBug(b){ if(b.dead) return; b.dead=true;",
   "  function killBug(b){ if(b.dead) return; b.dead=true; sfx('bug');"),
  ("    if(!s._done){ s._done=true; stationEls[s.id].classList.add('done');",
   "    if(!s._done){ s._done=true; sfx('open'); stationEls[s.id].classList.add('done');"),
  ("  function loseHeart(){ if(hearts>0) hearts--; renderHearts(); }",
   "  function loseHeart(){ if(hearts>0) hearts--; renderHearts(); sfx('hurt'); }"),
]
for o, n in hooks:
    assert o in h, "hook SFX non trovato: " + o[:48]
    h = h.replace(o, n, 1)

# 5e) SCHERMATA VITTORIA: gameClear diventa un overlay vero (+ fanfara)
old_gc = "  function gameClear(){ toast('◆ GAME CLEARED ◆','all 9 keys collected — thanks for playing'); }"
new_gc = '''  function gameClear(){ if(window.__cleared) return; window.__cleared=true; fanfare();
    var o=document.createElement('div'); o.className='overlay'; o.id='winScreen'; o.style.zIndex='90';
    o.innerHTML='<h1 class="title" style="color:var(--cyan);text-shadow:0 0 22px rgba(69,214,232,.6),4px 4px 0 rgba(255,92,138,.3)">✦ GAME CLEARED ✦</h1>'
      +'<div style="font-family:var(--mono);font-size:22px;letter-spacing:6px;margin:14px 0 6px">\U0001f511\U0001f511\U0001f511\U0001f511\U0001f511\U0001f511\U0001f511\U0001f511\U0001f511</div>'
      +'<p class="lede" style="max-width:46ch;color:var(--muted)">All <b>9 keys</b> collected — you walked my whole career, 2011 to today. Thanks for playing. Now the real thing:</p>'
      +'<button class="contBtn" id="winCv">☰ READ THE FULL CV</button>'
      +'<button class="ghostBtn" id="winAgain">▶ PLAY AGAIN</button>';
    (overEl.parentNode||document.body).appendChild(o);
    document.getElementById('winCv').addEventListener('click', function(){ openCv(); });
    document.getElementById('winAgain').addEventListener('click', function(){ location.reload(); }); }'''
assert old_gc in h, "gameClear non trovato"; h = h.replace(old_gc, new_gc, 1)

# 5f) SFONDO DEEP-SPACE: nuovo campo stellare a parallasse + pianeta ad anelli + nebulosa
old_stars = "    stars=[]; for(var i=0;i<70;i++) stars.push({x:Math.random()*W,y:Math.random()*H*0.5,r:Math.random()*1.4+0.3,a:Math.random()*0.6+0.2}); }"
new_stars = "    stars=[]; for(var i=0;i<170;i++){ var lyr=i<95?0:(i<145?1:2); stars.push({x:Math.random()*W,y:Math.random()*H,r:(lyr===2?Math.random()*1.8+1.1:Math.random()*1.1+0.3),a:Math.random()*0.55+0.28,l:lyr,tw:Math.random()*6.28}); } }"
assert old_stars in h, "init stelle non trovato"; h = h.replace(old_stars, new_stars, 1)

new_drawbg = '''  function drawBG(t){
    ctx.clearRect(0,0,W,H);
    var bg=ctx.createLinearGradient(0,0,0,H); bg.addColorStop(0,'#0a0620'); bg.addColorStop(0.55,'#0d0826'); bg.addColorStop(1,'#050310'); ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);
    var neb=[[W*0.24,H*0.30,'rgba(120,60,200,0.16)'],[W*0.74,H*0.52,'rgba(60,120,220,0.13)'],[W*0.50,H*0.80,'rgba(200,60,140,0.10)']];
    for(var q=0;q<neb.length;q++){ var nn=neb[q]; var rg=ctx.createRadialGradient(nn[0],nn[1],0,nn[0],nn[1],Math.max(W,H)*0.42); rg.addColorStop(0,nn[2]); rg.addColorStop(1,'rgba(0,0,0,0)'); ctx.fillStyle=rg; ctx.fillRect(0,0,W,H); }
    var tw=reduce?0:t*0.002, pf=[0.05,0.10,0.17];
    for(var i=0;i<stars.length;i++){ var s=stars[i]; var sx=((s.x - px*pf[s.l])%W+W)%W; var a=s.a*(0.55+0.45*Math.sin(tw+s.tw)); ctx.fillStyle='rgba('+(s.l===2?'185,222,255':'212,202,255')+','+a.toFixed(3)+')'; ctx.fillRect(sx,s.y,s.r,s.r); if(s.l===2 && s.r>2.2){ ctx.fillStyle='rgba(140,200,255,'+(a*0.4).toFixed(3)+')'; ctx.fillRect(sx-1,s.y,s.r+2,s.r); ctx.fillRect(sx,s.y-1,s.r,s.r+2); } }
    var pxp=W*0.80 - px*0.03, pyp=H*0.24, pr=Math.min(W,H)*0.11;
    ctx.save();
    var pg=ctx.createLinearGradient(pxp-pr,pyp-pr,pxp+pr,pyp+pr); pg.addColorStop(0,'#ff9a6e'); pg.addColorStop(0.5,'#e0556b'); pg.addColorStop(1,'#6a2a6e');
    ctx.fillStyle=pg; ctx.beginPath(); ctx.arc(pxp,pyp,pr,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='rgba(6,4,20,0.42)'; ctx.beginPath(); ctx.arc(pxp+pr*0.3,pyp,pr,0,Math.PI*2); ctx.fill();
    ctx.strokeStyle='rgba(120,200,255,0.55)'; ctx.lineWidth=Math.max(2,pr*0.05); ctx.save(); ctx.translate(pxp,pyp); ctx.scale(1,0.30); ctx.beginPath(); ctx.arc(0,0,pr*1.7,0,Math.PI*2); ctx.stroke(); ctx.restore();
    ctx.restore();
    var horizon=H*0.72, off=reduce?0:((t*0.0004)%1);
    ctx.save(); ctx.strokeStyle='rgba(69,214,232,0.20)'; ctx.lineWidth=1;
    for(var r=0;r<14;r++){ var f=(r+off)/14; var yy=horizon+(H-horizon)*(f*f); ctx.globalAlpha=0.10+f*0.35; ctx.beginPath(); ctx.moveTo(0,yy); ctx.lineTo(W,yy); ctx.stroke(); }
    ctx.globalAlpha=1; var vpx=W*0.5; ctx.strokeStyle='rgba(120,90,200,0.28)';
    for(var vx2=-8;vx2<=8;vx2++){ var fx=vpx+vx2*(W*0.16); ctx.beginPath(); ctx.moveTo(vpx,horizon); ctx.lineTo(fx,H); ctx.stroke(); }
    ctx.globalAlpha=1; ctx.strokeStyle='rgba(69,214,232,0.5)'; ctx.lineWidth=2; ctx.shadowBlur=14; ctx.shadowColor='#45d6e8'; ctx.beginPath(); ctx.moveTo(0,horizon); ctx.lineTo(W,horizon); ctx.stroke();
    ctx.restore();
  }'''
i1 = h.find('  function drawBG(t){')
i2 = h.find('  requestAnimationFrame(loop);', i1)
assert i1 > 0 and i2 > i1, "blocco drawBG non individuato"
h = h[:i1] + new_drawbg + '\n' + h[i2:]

open(OUT, 'w', encoding='utf-8').write(h)
print('PATCH v4+v5 OK · bytes', len(h))
