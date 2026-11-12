# Whop spec ad (brand film, beat montage), code only

27 s, 1920x1080, 90 BPM trap written in code (`audio/beat.py`, the first version of
`scripts/score.py`). The person approved v5 after four rounds:
1. A stock 115 BPM loop: "not good at all".
2. A beat matched to the reference, with cuts moved onto its grid: "much better".
3. The camera driven by `assets/cues.js`, plus SFX on every action: "everything is much better", but "the screen is shaking a lot".
4. Shake toned down.
5. Shake only in the intro and outro, and one soft swish per caption instead of per-letter clicks: "sounds good".

Images, fonts and SFX are not bundled: images and fonts came from `npx hyperframes capture
whop.com`; SFX were CC0 whooshes from `~/sfx-lib/openverse` and uisfx. Read `index.html` for the
camera layer (now `scripts/camera.js`) and `audio/visual_cues.json` for the SFX cue sheet.
Measured on the delivery: −9.2 LUFS, 46% of cuts within 1 frame of an 8th, moving 20% / still 42%
(too still by `references/playbook.md` §9; the next film adds drift and morphs).
