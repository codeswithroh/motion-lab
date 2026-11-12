# The playbook: what the five reference films do

Distilled from five brand films the person called "the best work done": Slash "Global" (27 s),
Elysium (47 s), Gamdom (31.5 s), TxFlow (32 s), GoDark (30 s). Every number below was measured
with `scripts/analyze_reference.py` or read frame by frame; the beat sheets are in
`reference-films.md`. Use this file as the rules for any ad, promo, spec ad or launch film.

## 1. The arc: five acts, always in this order

| Act | Share of runtime | What happens | Seen in |
|---|---|---|---|
| 1. Tension | first 15-30% | The viewer's pain, said plainly, usually with a number. The picture is dark, compressed or broken. | "Every day, $8 billion in crypto gets front-run." / "This is one trade. Well... it's three apps." / "Every chain wants your liquidity. It takes it, and it keeps it." |
| 2. Breath + turn | lands at 15-33% | 0.15-0.4 s of near-silence, then the brand name on the loudest hit in the film. The world flips: dark to bright, chaos to order, many to one. | "...until now." then GoDark (loudest point, −4.4 dB) / "So TxFlow built one chain for all of it." / white flash, then turquoise "Elysium works the other way" (peak −6.4 dB) / dip to −22 dB, then "This is Gamdom" |
| 3. Proof in threes | middle 40% | Three (or four numbered) parallel beats with the same layout and new content each time. The real product acts: a cursor clicks, a slider moves, a toast confirms. Lines often come in action/benefit pairs. | "Bet. Spin. Win." / "Place your order. No one sees it. Get matched. No one knows. Settle onchain." / Spot, Perps, Prediction / 01/04 to 04/04 |
| 4. One hero number | about 75% | One stat, huge numeral with a small unit, counting or snapping in. | "59 new perps in the last month" (counts 73 to 59) / "100 ms blocks" / "8,200+ games" |
| 5. Resolve | last 3-4.5 s | The film's motif collapses into the logo, then wordmark, tagline and URL. Calm or inverted ground, dead-still hold, music tail. | TxFlow line → one square → logo / Elysium rings → logo on white / Gamdom coin → logo + URL |

The tension is never skipped: a film that opens on the product has nothing to resolve. Write
act 1 in the customer's words, not the company's.

## 2. One motif carries the whole film

Each film picks one shape from the logo and makes it the atom of every picture, so the logo at
the end feels inevitable rather than stamped on.

- TxFlow: the logo's pixel square → a progress line → bridge loader → shattering pixels →
  terrain → status cards on one line → one square → logo.
- Gamdom: the logo mark → a glowing orb → coins → a burst of logo coins → the mark spinning into the lockup.
- Elysium: concentric rings → the hero island growing a new ring per step → globe → round logo.
- GoDark: a single bright cube (your order) moving through darkness → the "G" radar → logo.
- Slash: the white caption pill and dashed grid lines on every shot → end card.

Rule: write the motif in SPEC.md before any shot. Every shot must contain it or be made of it.

## 3. Camera and cuts: two modes

| | Voice-led film (Gamdom, TxFlow, GoDark, Elysium) | Beat montage (Slash) |
|---|---|---|
| Hard cuts | 3-6 in 30-47 s; median shot 3-6 s | 52 in 27 s; median shot 0.33 s |
| Transition | morph the motif, zoom-through, match on shape, whip with motion blur, 1-3 frame white flash at the turn and before the logo | hard cuts, 0-2 frames early on the beat |
| What sets the clock | the voice: a new line every 2-3 s, a word on screen as it's spoken | the beat: 44% of cuts within 1 frame of an 8th note; 47% of motion peaks on the 8th grid |
| Motion on beat grid | 20-33% (chance level, so the beat is not the clock) | 47% |
| Moving frames | 33-54% | 65% |
| Still frames | 8-37% | 21% |

**Where the motion comes from:** continuous movement, not shake. The hero object orbits, grows
or morphs. The camera drifts and pushes the whole time (Elysium never stops; TxFlow's terrain
rolls). Parallax layers and fog move at different speeds, and counters tick. Shake is seasoning
for the intro and outro only. The Whop spec ad (approved, with shake in the intro and outro only)
measured 20% moving and 42% still. That is the gap the next film closes with drift and morphs, not punches.

Pick the mode from the request: a voiceover or script means voice-led. Music only with many
shots or photos means beat montage. Never let the picture sit still for over 2 s before the final hold;
the Whop v2 cut had 50% still frames and the person said picture and music felt like "two
things going in a separate way".

## 4. Type

- One sans family. A serif italic is allowed for one accent word (GoDark "order").
- Lines are 2-6 words. Each word appears as it's spoken, landing 0-4 frames before the voice.
  It enters with blur 8 → 0 px, a scramble/decode (TxFlow, Elysium) or a caret typing in a field (Gamdom, GoDark).
- **One accent-coloured word per line**: the meaning word ("one *trade*", "live *markets*",
  "your *kingdom*", "*dark pool*").
- Scale contrast: the hero word or numeral is 3-5× the body size. A small label sits above a big
  word ("Built on / **Hyperliquid.**", "Settled on / **HyperEVM.**"). For a number, the numeral is
  huge and the unit is small and raised ("**100** ms blocks", "**8** Billion Dollars").
- Text sits in the negative space beside the hero object, never on top of busy detail.
- Numbered steps leave a running checklist: done steps stack above, small and faded (Elysium 01/04 to 04/04).
- UI words get UI treatment: a selection box with handles, an input field pill, or a button that gets clicked.

## 5. Colour and light

- One hue family plus black or white. Measured palettes: Elysium is all teal (#3dc4c0, #489a94,
  #276b7d), TxFlow is black plus one green, GoDark is black plus purple and green, Gamdom is greens on black.
- Light is the brand hue: soft gradient blooms, fog and depth of field in the brand colour.
  Generic neon glow that isn't the brand hue is still banned.
- The turn changes the light. Dark to bright (Elysium mean luma jumps at 7 s, Gamdom goes black to
  mint at 3.2 s), or a 1-3 frame white flash (Elysium 40.8 s, GoDark 26.5 s).

## 6. Product on screen

Show the real UI floating on a tilted card with a soft shadow and the brand glow. It always
acts: a cursor moves and clicks, a slider drags to 50x, a tab switches, a toast confirms ("Market
order submitted"), a counter ticks (+1,368 points). Static screenshots never appear. One widget
stays put while its content changes per proof beat (TxFlow's one trade ticket goes Spot → Perps → Prediction).

## 7. Sound

- **Voice:** 1.6-2.1 words/s, with a new line every 2-3 s. It sits on top. The music runs underneath
  at an integrated −12 to −14.3 LUFS for the whole mix.
- **Music-only films** are mastered loud and flat: Slash −8.1 LUFS with LRA 1.3; Elysium −11.5.
- **Build into the turn.** Elysium rises from −33 dB to −6 dB over the first 7 s, so the reveal is the loudest
  point. Other films dip 9-18 dB for 0.15-0.4 s just before the name.
- **The loudest moment of the film is the brand reveal.** The second hit is the hero number or the logo.
- Tempo: 90-117 BPM across all five. Dark/finance pieces sit at 90-100 BPM on trap or half-time drums.
  Brighter tech pieces sit at 110-120 BPM.
- SFX on visible actions: a whoosh peaking on each transition, a click on each cursor press, a
  soft swish when a caption pops, an impact on hits. **Never one click per typed letter**; the
  person called that "odd".

## 8. Holds and pacing

- Something new every 1-2 s in acts 1-4. Each line holds 0.5 s plus 0.3 s per word, then gets replaced.
- Final lockup holds 3-4.5 s, dead still, with the music tail ringing out.
- Runtime 27-32 s for a social ad, up to 47 s for a launch film.

## 9. Measured targets for your own render

Run `analyze_reference.py` on your render and compare:

| Metric | Voice-led target | Beat-montage target |
|---|---|---|
| moving frames | 33-55% | 55-70% |
| still frames | ≤ 35% | ≤ 25% |
| cuts within 1 frame of an 8th | n/a | ≥ 40% |
| integrated loudness | −12 to −14.5 LUFS | −8 to −11.5 LUFS |
| loudest 0.5 s window | at the brand reveal | at the brand reveal or the first drop hit |
| final hold | 3-4.5 s | 3-4 s |
| Whop v5 (for scale) | n/a | moving 20%, still 42%, cuts on 8th 46%, −9.2 LUFS: on-beat, but too still |
