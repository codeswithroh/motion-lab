# Review

## v2 (renders/cofoundr-agents-v2.mp4): new look, same cue sheet

- Same music, same cut points, same hit: every scene start and every `at()` cue from v1 is unchanged. Re-measured on the v2 MP4: the circles touch on frame 887 and the hit lands at frame 887.5. Loudness −14.9 LUFS, true peak −4.0 dBTP. 1050 frames, 60 fps, 2.9 MB.
- New visual language, warm paper and ink instead of the app's grey shell:
  - Ground #f3efe6, ink #111, muted #6b6558; oversized Instrument Serif with italic accents.
  - Hook: 156 px type, and a 760 px "you" disc bleeding off the corner.
  - Rail: a numbered chapter bar (01 connect … 04 10 in chat) that fills in ink.
  - Connect: a split screen. "you" sits in an ink-ruled box; the right half floods in each app's brand colour as it swaps (ChatGPT green, Cursor black, VS Code blue with Microsoft's white icon, Claude Code charcoal, Claude orange).
  - Ask: the prompt typed at 112 px serif, and a black `find_cofounders` band sweeping across.
  - Search: a grid of squares instead of round dots; the 10 ranked turn into blue diamonds and fly to where the score bars grow from.
  - Results: full-width score bars whose length is the score.
  - Payoff: a 1.25x logo with a multiply overlap, ink shockwave rings on the hit, a 200 px wordmark, the app tiles and cofoundrs.fun.
- Follow-ups fixed in v2:
  1. Four contrast failures: the muted grey, "Claude" in #d97757 on paper (2.72:1, now #c15f3c), and white on the lavender bars (now #5b63d6).
  2. Labels under 28 px.
  3. "pick your agent." was 0.08 s short.
  4. The tool line was 0.2 s short (shorter text, band 0.13 s earlier).
  5. The closing URL is held 2.05 s.
  6. The shockwave ring showed before the hit (`immediateRender: false`).
  7. The diamonds and the "you" circle crossed the incoming title. The moves are faster and the title waits 0.25 s for the circle to land.
- Weakest beat: 2.5-2.65 s. The right panel is a plain beige square for about 8 frames before the first flood, because ChatGPT arrives at 2.8 s.

## v1 (renders/cofoundr-agents.mp4)

- 17.5 s, 1080x1080, 60 fps, 1050 frames, 2.4 MB. Built from SPEC.md. Sequel to the first cofoundr film: that hook was "i couldn't find a cofounder.", this one is "now i just ask my agent."
- One worked example travels the real agent flow: the OAuth consent card (search / read / intro, 3 searches a day), the message "find me a technical co-founder", the `find_cofounders` tool call, 700M → 30 scored → 10 ranked, and the reply in chat. The blue "you" circle from the hook is the thread: consent avatar, chat avatar, centre of the search field, question avatar, then the logo's left circle.
- Real numbers: 700M profiles, 30 scored, 10 ranked, 1/3/5/10 daily caps, the six scopes and tool names from src/lib/mcpTools.ts, and "12 s" and the 9.9 top score from the production run on 3 Nov 2026. Illustrative: the three role lines and the 9.5 scores on rows 2 and 3 (the prod run returned real people; the film shows roles only).
- App marks are the official ones: LobeHub icons (MIT) for Claude, ChatGPT/OpenAI, Cursor and Claude Code; Microsoft's VS Code icon from its brand kit. Inlined by `src/build.py` from the site's BrandLogo.tsx. Edit scenes in `src/`, then run `python3 src/build.py`.
- Music: Ludlow (Epidemic Sound, from Downloads), 144.1 BPM, from 49.215 s.
  - find_drop's top onset at 63.83 s turned out to be a pickup; the real hit is 0.17 s later.
  - Measured in the delivered MP4: the hit at 14.792 s (frame 887.5), and the logo circles first touching on frame 887 (pixel gap 12 px on 886, 0 on 887). Sound is 0.5 frames after the picture.
  - Loudness −14.9 LUFS, true peak −4.0 dBTP, no clipping (volume 0.6). These are measurements, not listening.
- Follow-ups applied after the first check:
  1. Rows 2-3 were on screen 1.15 s against a 1.27 s floor, and "+7 more…" 0.88 s against 2.17 s. The rows got +0.3 s and the counter +0.5 s via `at()`; the "+7 more" line was cut, since the header already says 10.
  2. The hook was shortened from 3.0 s to 2.5 s; 5 words need 1.5 s, and they get 1.95 s.
  3. Grey rank numbers at 2.56:1 contrast were changed to #64748b.
  4. `data-var-text` on the hook and tagline printed the line twice; removed (the prompt variable stays).
  5. The hero moved from 14.17 s to 14.78 s to hit the real drop; the payoff got 0.2 s more hold.
- Weakest beat: 2.35-2.55 s. Between the hook words leaving and the consent card landing there are about 8 frames with only the blue circle on screen. It reads as the circle travelling, but the card could land 0.1 s earlier.
- Checked: `hyperframes check` (0 errors, 0 warnings), contact sheets at 13 instants, 16 frames pulled from the MP4, ffprobe, audio onset and loudness. Not checked: a phone-width sheet, and listening on speakers.

## Post draft (not posted)

X (long post):

```
now i just ask my agent for a cofounder.

cofoundr is an mcp server now. works in claude, chatgpt, cursor, claude code and vs code.

> connect once. sign in with linkedin, pick what it can do, cap it at 1-10 searches a day
> ask "find me a technical co-founder"
> find_cofounders searches 700M profiles and scores 30
> 10 ranked matches land in the chat, each with an intro draft

my test run took 12 seconds. top match 9.9/10.

it never messages anyone. disconnect and the token dies on the spot.

cofoundrs.fun/#agents
```

X (under 280):

```
now i just ask my agent for a cofounder.

cofoundr works inside claude, chatgpt, cursor and vs code now.

> ask "find me a technical co-founder"
> it searches 700M profiles, scores 30
> 10 ranked matches in chat, intro drafts included

12 seconds on my test run.

cofoundrs.fun/#agents
```
