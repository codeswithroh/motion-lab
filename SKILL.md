---
name: motion-lab
description: >
  Default for any "make a motion graphics video" request (product showcase, architecture
  or pipeline explainer, launch clip, hackathon win, feature reveal) for X or LinkedIn. Use it
  for any motion graphic, animated explainer of how something works, or "a video like the
  cofoundr one". Writes a directed spec
  full of numbers, builds one worked example travelling through the real mechanism in HyperFrames,
  checks frames by measurement, syncs to the music track's drop, renders a square 60 fps MP4 and
  drafts the post.
---

# Motion Lab

A directed motion piece: every adjective becomes a number, every follow-up is a measured note,
and the film shows the real thing working. Reference build: `examples/cofoundr/` in this skill
(SPEC.md, compositions/, REVIEW.md, preview.mp4). Read it before your first build in a session.

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

## 3. Story shape (what made the cofoundr film work)

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

Default to the product's own light app shell, not a dark void: ground like `#f0f2f8`, white
cards radius 28 with `0 18px 40px rgba(15,23,42,.08)`, ink `#0f172a`, muted `#64748b`.
Display: the brand's serif (download it into `assets/fonts/`, `@font-face` in every scene that
uses it). Body: Inter 500/700. Text read at 28 px minimum. The accent marks one focus per frame.

Banned: dark navy void, glow, bloom, neon, particles, purple/blue gradients, glass cards,
monospace caps labels, pill chips, everything centred, every element fading up, titles that drift
after landing, the logo docked in a corner, three cards in a row, KPI grids, real people's faces
or names as fake candidates.

## 5. Build

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
3. Write each problem as a numbered follow-up with numbers, the way the reference prints them:
   "the need tag is on screen 0.56 s, floor 1.27 s: land it at 0.9 s and shift everything after
   1.6 s by +0.6 s". Log them in REVIEW.md.
4. After rendering, pull seam frames from the MP4 itself
   (`ffmpeg -vf "select='eq(n\,F1)+eq(n\,F2)',scale=360:-1,tile=Nx1"`) and look at them.

## 7. Music

Use the track the user gives (copy into `assets/audio/`). Without one, ask for one, or offer a score
synthesized in code from frame numbers (`references/sound.md`).

1. `python3 scripts/find_drop.py <track>` prints the loudness map and the biggest drops with
   their exact onset and the beats around them.
2. Pick the film's hero moment (the logo shapes touching, the result landing). Compute the frame
   it actually happens on (for `back.out(1.4)` the shapes touch at ~23% of the tween).
3. `data-media-start` = drop onset − hero time, snapped to the nearest beat so the film starts on
   one. Sound lands 0-1 frame **after** the picture, never before.
4. `<audio id="music" class="clip" data-start="0" data-duration="<film>" data-media-start="…"
   data-volume="1" data-fade-in="0.05" data-fade-out="1.2">`.
5. Render, then measure: `npx hyperframes audio <mp4> --json` must show an onset within one frame
   of the hero frame; loudness −16 to −14 LUFS, true peak ≤ −1 dBTP. Say it was measured, not heard.

## 8. Deliver

- `npx hyperframes render -f 60 -q delivery -o renders/<slug>.mp4`, then `ffprobe` for size,
  fps and frame count.
- Send the MP4 to the user.
- REVIEW.md: creative calls, what was measured, the weakest beat, warnings kept on purpose.
- Draft the post in the user's voice (default: lowercase, hook first, short lines, the
  mechanism as `>` steps, one real detail from the code, no hype words). Never post it.
