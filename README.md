# Interactive CV — progetto (backup persistente)

**Artifact live (gioco):** https://claude.ai/code/artifact/c27ccaa5-f81a-4026-b461-ab7e88beb451

## File
- `interactive-cv.html` — **sorgente canonico** del gioco (pulito, dal `<title>`). È QUESTO che si ripubblica.
- `interactive-cv.raw-with-wrapper.html` — copia grezza scaricata dall'artifact (con wrapper host). Solo archivio.
- `select-your-engineer.html` — schermata arcade "Select Your Engineer".
- `sprite-lab.html` — tuner interattivo dello sprite (slider + export PNG).
- `assets/` — sprite pixel (avatar_80/160/320, tondo, idle), `sprite2.py` (generatore), `config.json` (parametri), `patch_game.py` (innesto sprite nel gioco).

## Sprite nel gioco
`#player` usa `<img class="peo">` (avatar_160 ritagliato) al posto dei riquadri CSS head/torso/gambe.
Flip (`scaleX`), camera, `.walk` e la chitarra `.gtr` restano invariati. Rigenerare l'innesto: `python3 assets/patch_game.py`.

## Ripubblicare dopo modifiche
Tool Artifact con `url=<artifact live>` e `file_path=interactive-cv.html`.
IMPORTANTE: pubblicare la versione SENZA wrapper (dal `<title>`), altrimenti il frame-runtime dell'host si duplica.
