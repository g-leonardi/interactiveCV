# Interactive CV — Giuseppe Leonardi

CV giocabile (platformer synthwave): cammini la timeline di carriera, sblocchi i
progetti dai cabinati, raccogli le chiavi. Personaggio = sprite pixel di Giuseppe.

**Deploy entrypoint:** `public/index.html` (Cloudflare Pages output dir = `public/`) (self-contained, nessuna dipendenza esterna).
**Live artifact:** https://claude.ai/code/artifact/c27ccaa5-f81a-4026-b461-ab7e88beb451

## File
- `public/index.html` — il gioco (unica cosa servita online) (con CV PDF + deep-dive MD incorporati e scaricabili).
- `select-your-engineer.html` — schermata arcade "Select Your Engineer".
- `sprite-lab.html` — tuner interattivo dello sprite.
- `interactive-cv.original-backup.html` — sorgente originale intatto (base per le patch).
- `assets/` — toolchain sprite:
  - `sprite2.py` — genera la testa pixel dalla foto/config.
  - `config.json` — parametri sprite scelti (silver fox, ciuffo swept…).
  - `fullbody.py` — genera i **8 frame** a corpo intero (idle/blink/walk1-4/jump/fire).
  - `patch4.py` — innesta lo sprite animato nel gioco (riparte SEMPRE dal backup originale).
  - `fullbody_*.png` — i frame renderizzati.

## Rigenerare lo sprite nel gioco
```
python3 assets/fullbody.py     # rigenera i frame
python3 assets/patch4.py       # riscrive public/index.html col nuovo sprite
```

## Deploy (statico)
Qualsiasi host statico serve `index.html` alla radice. Es. Cloudflare Pages:
```
wrangler pages deploy public --project-name giuseppe-leonardi
```
