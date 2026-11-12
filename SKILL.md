---
name: motion-lab
description: >
  Default for any "make a motion graphics video" request: brand film, ad, spec ad, promo,
  product showcase, architecture or pipeline explainer, launch clip, hackathon win, feature reveal,
  for X or LinkedIn. Use it for any motion graphic, animated explainer of how something works,
  "a video like the cofoundr one", "an ad like these references", or when the person hands over
  reference videos to learn from. Breaks references down by measurement (shots, motion, music,
  drops, voice), writes a directed spec full of numbers on the five-act arc the reference films
  share, builds in HyperFrames, drives music, SFX, camera and captions from one cue sheet, checks
  frames and sync by measurement, renders the MP4 and drafts the post.
---

# Motion Lab

A directed motion piece: every adjective becomes a number, every follow-up is a measured note,
and the film shows the real thing working. Reference builds in this skill, each with SPEC.md,
compositions/, REVIEW.md and preview.mp4:
- `examples/cofoundr/`: the first film, in the app-shell look.
- `examples/cofoundr-agents/`: the sequel the person called perfect. Ludlow scored to a measured
  hit, and the paper-and-ink look; see §4 and §7.
- `examples/whop-spec/`: the brand-film mode, a beat montage where music, SFX and camera run off one
  cue sheet (code only; see its README for the five rounds of notes that shaped the rules in §7).

Read both before your first build in a session.

The rules for brand films and ads come from five reference films the person called the best work
done (Slash, Elysium, Gamdom, TxFlow, GoDark): read `references/playbook.md` (the principles,
with numbers) and `references/reference-films.md` (their beat sheets) before any ad, promo or
launch film. `references/sync.md` is how every layer gets locked to one clock.

## 0. Pick the mode, study the references

| Mode | When | Shape |
|---|---|---|
| **Brand film** (default for ad, promo, spec ad, launch film, "like these references") | the subject is a company or product to sell | 16:9 1920x1080 30 fps, 27-32 s (up to 47 s), five-act arc (`playbook.md` §1), voice-led or beat montage |
| **Explainer** | the subject is a mechanism (a pipeline, an agent, a repo) | 1080x1080 60 fps for the X feed, 15-17 s, the cofoundr shape (§3 below) |

If the person gives reference videos, measure each one before writing anything:

```bash
python3 scripts/analyze_reference.py <video> --out <dir>   # report.md, shots.jpg, timeline.jpg
```

Read `report.md` with `timeline.jpg` (one tile per second) and write a beat sheet in the
shape of `reference-films.md`: time, words, picture, turn, hero number, resolve. Name the
reference's clock (voice or beat), its motif, its palette, its loudest moment. Your film copies
the structure, rhythm and sync. It never copies their footage, music or words.

Dependencies: ffmpeg, numpy, scipy, librosa (`python3 -m venv .venv && .venv/bin/pip install librosa scipy`),
whisper-cli with a ggml model for voice.

Load `hyperframes` for the render contract, then follow these steps. `hyperframes` rules win on
format; this skill wins on story, look and process.

## 1. Read the source

Before writing anything, read the subject itself: repo, README, the main route or pipeline file,
pricing, the live site. Pull out:

- the **mechanism**: the real steps in order (function names, API calls, stages).
- the **real numbers**: dataset sizes, counts, weights, timings, limits. Never invent one. A value
  the source doesn't give is either cut or marked illustrative in REVIEW.md.
- the **brand**: accent hex, second colour, logo SVG, fonts, any style lock file.
- one **surprising detail** a developer would quote (a clamp, a fallback chain, a bug that shipped).

If the person names a technology the source doesn't use (a sponsor, a tool from a tweet), don't
draw it. Say so and ask what it does.

## 2. Write SPEC.md (the directed prompt)

The vague prompt ("cool, premium, modern") gets dark navy, glow rings, particles and a made-up
tagline. The directed prompt gets the film. Write `SPEC.md` at the project root from
`references/spec-template.md`. Each line is a number:

- GOAL, OUTPUT (1080x1080, 60 fps default for X), TIME (seconds x 60 = frames).
- LOOK: ground, ink, muted ink, rule colour, accent and what it means, display and body faces
  with px sizes and tracking, card radius and shadow.
- OBJECTS: every thing the viewer must recognise, drawn from the product's real UI.
- MOTION: eases by role, durations and staggers in frames (`references/numbers.md`).
- SHOTS: frame ranges, one hero move each, what the viewer reads, the hand-off to the next shot.
- BANNED and QA (the frames to check and what each must show).

## 3. Story shape

**Brand film:** the five acts in `playbook.md` §1. Tension in the customer's words (15-30%).
Then a breath and the turn, with the brand name on the loudest hit (15-33%). Then proof in threes
with the real UI acting, one hero number, and the motif collapsing into the logo with a 3-4.5 s
hold. Write the motif (one shape from the logo that every shot contains) and the clock
(voice or beat) into SPEC.md before the shots.

**Explainer** (what made the cofoundr film work):

1. **Hook on frame 0.** The first frame is the thumbnail. The hook line is already landed on it,
   in the display serif, left-aligned, one word in the accent. A big brand shape sits beside it.
   Example: "i couldn't find a cofounder." with the blue circle.
2. **One worked example travels the whole mechanism.** A real input (the user's LinkedIn URL, a real
   query) enters a product card and moves through every stage. The shape from the hook carries
   into the card (it becomes the avatar), so the viewer never loses the thread.
3. **A stage rail** across the top names the real stages ("enrich you, search 700M, score 30,
   write intros") and lights each node as the picture reaches it. This is the architecture
   diagram, built into the film.
4. **Each stage gets its own picture shape**: a typed field, a field of dots narrowing from
   700M to 30, bars sorting by score with the top 10 kept in the accent, a result card typing
   its output. Similar lines never get the same picture.
5. **Payoff = the logo meaning something.** The two shapes (you and the match) slide together
   into the logo, the wordmark blurs in, one line with the key numbers. Hold 2 s+, dead still.

Length 15-17 s. Under 15 s if the person wants a loop.

## 4. Look

Brand films follow `playbook.md` §4-6. Use one hue family plus black or white, with light in the
brand hue. Use one sans, with one accent-coloured word per line and a hero word or numeral at 3-5× body
size. The real UI floats on a tilted card and acts. Those rules override the bans below where they
conflict: a dark ground lit by the brand's own hue and soft brand-colour bloom are what the
references do. Generic neon and a glow that isn't the brand hue stay banned.

Explainers:

Default to the product's own light app shell, not a dark void: ground like `#f0f2f8`, white
cards radius 28 with `0 18px 40px rgba(15,23,42,.08)`, ink `#0f172a`, muted `#64748b`.
Display: the brand's serif (download it into `assets/fonts/`, `@font-face` in every scene that
uses it). Body: Inter 500/700. Text read at 28 px minimum. The accent marks one focus per frame.

Banned: dark navy void, glow, bloom, neon, particles, purple/blue gradients, glass cards,
monospace caps labels, pill chips, everything centred, every element fading up, titles that drift
after landing, the logo docked in a corner, three cards in a row, KPI grids, real people's faces
or names as fake candidates.

**Every film gets a look of its own.** Before building, look at the person's previous films
(`~/Work/*-video/renders/`, this skill's `examples/`) and pick a visual language none of them used.
Keep the story shape (§3) and the brand's colours and logo; change the medium. The cofoundr agents
film's first cut reused the app-shell look and the person said it felt like the earlier films; v2 changed
only the look on the same cue sheet and they called it perfect. That v2 language, for reference:
paper `#f3efe6` + ink `#111` + oversized serif with italic accents, a numbered chapter bar that
fills in ink, split-screen flat colour floods in each app's real brand colour, a full-width black
tool band, a grid of squares whose winners turn into diamonds, score bars whose length is the
score, ink shockwave rings on the hit. Other languages to reach for next time: Swiss grid with
one huge numeral, blueprint/ruled diagram, newspaper columns, stamp/riso print. Never two films
in a row in the same one.

## 5. Build

- Brand film: one scene per act beat (tension, turn, each proof, number, resolve) in `compositions/`.
  The root holds the scene hosts, `#dim` and `#flash` overlays, the audio, and loads `assets/cues.js`,
  `assets/camera.js` (and `assets/words.js` with a voice). Scene starts sit on the grid (`sync.md` §1).

- `npx hyperframes init <dir>` in `<slug>-video/`. Root `index.html` mounts 3 scenes:
  `hook`, the mechanism scene (one continuous framing while the UI acts), `payoff`.
- Seed every random (mulberry32). Generated dots and bars are children of a timed scene.
- `fromTo` for every tween; `immediateRender: false` on repeated fromTo of the same target
  after the first.
- Keep a time-shift helper (`const at = (t) => t + …`) in the mechanism scene, so a retime is
  one line, not twenty.
- Copy that may change (the URL, the headline) goes in composition variables.

## 6. The lab loop (follow-ups with receipts)

Never trust the first build. After each pass:

1. `npx hyperframes check --json`; fix every error. `line_unread` means hold the line longer
   (0.5 s + 0.3 s a word) or cut words; never shrink type.
2. `npx hyperframes snapshot --at <every shot's mid and end>` and read the contact sheet.
3. Brand films: `analyze_reference.py` on the render. Moving frames, still frames and the loudest
   window must hit `playbook.md` §9; a miss is a follow-up.
4. Write each problem as a numbered follow-up with numbers, the way the reference prints them:
   "the need tag is on screen 0.56 s, floor 1.27 s: land it at 0.9 s and shift everything after
   1.6 s by +0.6 s". Log them in REVIEW.md.
5. After rendering, pull seam frames from the MP4 itself
   (`ffmpeg -vf "select='eq(n\,F1)+eq(n\,F2)',scale=360:-1,tile=Nx1"`) and look at them.

## 7. Sound and sync

Brand films: follow `references/sync.md`. One cue sheet (`audio/score.json`) feeds three things:
- `scripts/score.py` writes an original bed and the SFX, with the breath before each turn and an impact on each hit.
- `assets/cues.js` drives `scripts/camera.js`.
- With a voiceover, `scripts/word_cues.py` gives each caption its spoken time.

The person's verdict on the Whop film went from "it's not good at all" (a stock loop laid under
the cut) to "much better" (beat matched to the reference) to "everything is much better" (camera
and SFX driven by the beat's own event times). The difference was one clock for every layer.

Rules the person set on that film:
- Shake (punches, tilts, whips) only in the intro and outro. The middle stays steady; flash and dim are fine.
- Captions get one soft swish as they appear. Never one click per letter ("sounds odd").
- Get motion from continuous drift, orbit and morph in every shot (2-6% scale or 20-60 px of travel
  per second on the hero layer, background parallax at half that), not from shake.
- Picture must move with the music: below 33% moving frames it reads as "two things going
  in a separate way". Measure it with `analyze_reference.py` on the render.

### Using a given track (explainers, or when the person supplies music)

The music is what the person remembers. The process below produced a film they called perfect
("love your sound selection and matching it to the video"); follow it every time.

**Picking the track.** Use the track the user gives (copy into `assets/audio/`). If they give none,
look for their own licensed tracks before asking: `ls ~/Downloads/ES_*.mp3` (Epidemic Sound) and
the `assets/audio/` of their earlier `~/Work/*-video/` projects. Run `find_drop.py` on every
candidate and pick the one with a strong drop that sits after a quieter bar or two, at a tempo
whose beat (60 / BPM s) gives cuts room: 120-150 BPM suits a 15-18 s film. Prefer a track the
previous film didn't use, so the two don't sound alike. Say which you picked and why. Only if
nothing is on disk, ask, or offer a synthesized score (`references/sound.md`).

1. `python3 scripts/find_drop.py <track>` prints the loudness map and the biggest drops with
   their onset; `npx hyperframes beats <track> --json` gives the beat times and BPM.
2. **The listed onset can be a pickup, not the hit.** In Ludlow, find_drop's onset was 63.83 s,
   but the loud hit (−30 → −6 dB in 10 ms) came 0.17 s later. Read the loudness map around the
   onset, and always confirm on the render (step 6).
3. Pick the film's hero moment (the logo shapes touching, the result landing). Compute the frame
   it actually happens on (for `back.out(1.4)` the shapes touch ~23% into the tween, at 73% of the
   travel); keep that ratio if you rescale the shapes.
4. `data-media-start` = a beat near (hit − hero time), so the film starts on a beat. Then move
   the **picture** (the hero tween's start), never the audio, until the hero frame sits 0-1 frame
   **before** the sound. Write the arithmetic in an HTML comment next to the `<audio>` tag.
5. `<audio id="music" class="clip" data-start="0" data-duration="<film>" data-media-start="…"
   data-volume="…" data-fade-in="0.05" data-fade-out="1.2">`. Start at volume 0.6 for a mastered
   pop/electronic track; adjust after measuring.
6. Render, then measure on the MP4 itself:
   `python3 scripts/sync_check.py <mp4> <hit_s> <hero_frame> <row_y>` prints the audio hit's
   exact time and frame and the pixel gap between the two shapes frame by frame. Pass when the
   gap reaches 0 at most 1 frame before the hit. `npx hyperframes audio <mp4> --json`: loudness
   −16 to −14 LUFS, true peak ≤ −1 dBTP; change `data-volume` and re-render until it fits.
   Say it was measured, not heard.
7. When the person asks for changes to the look, keep the cue sheet (scene starts, `at()` cues,
   hero tween start) exactly as it is, so the sync they liked survives. Re-measure anyway.

## 8. Deliver

- Brand films: render the picture, mux the score WAV with a true-peak limiter (`sync.md` §5),
  then run `analyze_reference.py` on the delivery file and compare with `playbook.md` §9. Put the
  numbers in REVIEW.md next to the reference's.

- `npx hyperframes render -f 60 -q delivery -o renders/<slug>.mp4`, then `ffprobe` for size,
  fps and frame count.
- Send the MP4 to the user.
- REVIEW.md: creative calls, what was measured, the weakest beat, warnings kept on purpose.
- Draft the post in the user's voice (default: lowercase, hook first, short lines, the
  mechanism as `>` steps, one real detail from the code, no hype words). Never post it.
