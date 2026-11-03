# Review

- 17 s, 1080x1080, 60 fps, 1020 frames. Built from SPEC.md; one worked example (codeswithroh's LinkedIn) travels the real /api/match pipeline: enrich, search 700M, score 30, intros for the top 10.
- Numbers come from the repo: 700M profiles, 30 candidates, weights 40/35/25, top 10, ~60 s. The match card (Founding Engineer, Bengaluru, 9.1) and the bar heights are illustrative.
- Retimed after the first check: the need tag got +0.6 s, the intro draft +1.4 s, the "top 10" label was cut, and the hook line now sits on frame 0 for the thumbnail.
- Kept on purpose: `film_silent`. X autoplays muted; type and pictures carry it. No sound was made.
- Weakest beat: 10.0-10.4 s, the top-10 bars show through the match card while it fades in. Reads as the bars folding into the card, but a cleaner version would shrink the bars into the card's avatar.
- Checked: `hyperframes check` (0 errors), contact sheets at 17 instants, seam frames from the rendered MP4. Not checked: phone-width sheet.
