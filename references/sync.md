# The sync system: one cue sheet drives music, SFX, camera and captions

The references feel "totally synced" because one clock drives every layer. These files make
that mechanical. Built and approved on the Whop spec ad ("everything else is just perfect").

```
SPEC.md shot list ──► audio/score.json ──► scripts/score.py ──► assets/audio/score.wav  (music + SFX)
                                                          └──► assets/cues.js        (kick/clap/roll/drops/hits)
voiceover.wav ───────► scripts/word_cues.py ─────────────────► assets/words.js       (word onsets, lines)
assets/cues.js + words.js ──► scripts/camera.js + scene tweens ──► picture rides the same times
```

## 1. Put the cuts on the grid first

Beat = 60 / BPM. Scene starts go on beats; big cuts go on bar lines (4 beats). Inner
moments (a caption, a photo swap) go on 8th notes. At 90 BPM: beat 0.6667 s, bar 2.6667 s, 8th 0.3333 s.
Write starts as exact multiples (5.3333, not 5.33) in `index.html`.
A voice-led film uses the word onsets from `words.js` as its grid instead: a line's picture
changes on its first word, and its accent word lands on that word's `t`.

## 2. score.json (filled example from the Whop film)

```json
{
  "duration": 27, "bpm": 90, "style": "trap", "root": 26,
  "drops": [[5.0, 5.3333], [16.8333, 17.3333]],
  "hits": [5.3333, 17.3333, 23.3333, 24.6667],
  "end": 26.0,
  "sfx_dir": "assets/audio/sfx",
  "sfx": {
    "whoosh": [1.3333, 2.6667, 8.6667, 10.6667, 11.6667, 12.6667, 13.6667, 14.6667, 16.0, 18.3333, 20.6667, 21.6667, 24.0],
    "pop": [0.12, 3.6667, 5.3533, 9.3334, 10.6867, 14.7667, 17.3533, 18.3633],
    "ui": [["ui-receive.mp3", 7.02, 0.4], ["ui-receive.mp3", 7.6867, 0.4], ["ui-press.mp3", 20.0, 0.45], ["ui-purchase.mp3", 20.08, 0.35]]
  },
  "out": "assets/audio/score.wav", "cues": "assets/cues.js"
}
```

- `drops` = the breath before each turn or hero moment (0.33-0.5 s). `hits` = the brand name,
  the hero number, the end card and the logo. These are the moments the viewer remembers.
- `whoosh` = every transition; the sample's loudest point lands on the cut. `pop` = every caption
  appearing (one soft swish each). `ui` = each cursor click, toast, bubble or button press, as a file plus a gain.
- SFX source: `~/sfx-lib/openverse/` (CC0 whooshes and clicks) and uisfx
  (`~/.claude/skills/real-sfx/vendor/node_modules/uisfx/sounds/minimal/*.mp3`: press, receive,
  purchase, success, notification...). Copy the ones you use into `assets/audio/sfx/` and note them in REVIEW.md.
- `style`: `trap` (90-100 BPM, half-time claps, hat rolls, 808 riff) for dark, money or crypto
  pieces. `four` (110-124 BPM, four-on-the-floor) for bright tech pieces. `root` sets the key.
- It's original music written in code, so there's no license question. If the person gives a track, skip
  score.py's music and use `find_drop.py` on the track; still run SFX and the camera off the same cue times.

## 3. Camera: scripts/camera.js

Copy it to `assets/camera.js`, load it after `cues.js`, add the `#dim` and `#flash` overlays
and call `motionCamera(tl, {scenes, cues: window.CUES, shake: [[0, introEnd], [outroStart, 99]]})`
in the root timeline. It punches on kicks, tilts on claps, stutters on hat rolls, whips in at
scene starts, darkens and creeps in during drop-outs, and flashes and punches on hits.

**Shake only in the intro and outro.** The person asked for no shake in the middle after
seeing it everywhere. Flash and dim are not shake; keep them everywhere. Voice-led films use
`strength: 0.5`, or skip kicks and claps and keep only whips, flashes and dims, because the voice is the clock there.

## 4. Captions on the voice: scripts/word_cues.py

`python3 scripts/word_cues.py voiceover.wav --out assets/words.js` gives every word's onset
minus 0.08 s and groups words into lines. In each scene, reveal word `i` at `WORDS[i].t - sceneStart`,
and set the line's accent word in the brand colour. Never time captions by hand when there is a voice.

## 5. Mux, don't trust the render's audio

The renderer brought the mix down about 4 dB. Render the picture, then mux the WAV in with a
true-peak limiter:

```bash
ffmpeg -i renders/film.mp4 -i assets/audio/score.wav -map 0:v -map 1:a -c:v libx264 -crf 20 -preset slow \
  -pix_fmt yuv420p -af "aresample=192000,alimiter=limit=0.7:level=disabled:attack=1:release=30,aresample=48000" \
  -c:a aac -b:a 256k -shortest -movflags +faststart renders/film-social.mp4
```

Check `ebur128=peak=true`: music-only around −9 LUFS with peak ≤ −1 dBFS; with voice
−12 to −14 LUFS.

## 6. Prove the sync on the MP4

`python3 scripts/analyze_reference.py renders/film-social.mp4 --out renders/check` gives
moving/still share, cut-to-grid and the loudness curve. Compare against `playbook.md` §9 and say
it was measured, not heard.
