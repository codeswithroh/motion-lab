# The numbers

| What | Value |
|---|---|
| Arrival | `expo.out` or `power4.out`, 0.5-0.6 s |
| Camera move, carry across, colour flood | `power2.inOut` / `power3.inOut`, 0.6-0.7 s |
| Exit | `power3.in`, 40-50% shorter than the entrance (0.2-0.3 s) |
| Word reveal | blur 8 → 0 px + opacity, 0.13 s each, 60-120 ms apart, no translate |
| Typing | one letter every 2 frames at 60 fps |
| List or grid stagger | 40-80 ms per item; a field of dots 0.6 s total, ordered by distance from the source |
| Overlap | the next element starts when the previous is 30-50% done |
| Springs | damping 0.7-0.85 premium, 0.4-0.6 playful; position and scale only, never opacity or colour |
| `back.out(1.4)` | overshoot ~10%; reaches 73% of its travel at 23% of the duration |
| Hold to read | 0.5 s + 0.3 s a word; the last line ≥ 2 s |
| Something new | every 2-4 s |
| Beat grid | frames per beat = fps × 60 / BPM; compute each beat from its index, never add a rounded beat |
| Sound vs picture | sound peaks 0-1 frame after the picture event |
| Loudness (explainer) | −16 to −14 LUFS integrated, true peak ≤ −1 dBTP, measured on the delivered MP4 |
| Text size | ≥ 28 px at 1080; hook 104-120 px; wordmark 130-150 px |
| Brand film arc | tension 15-30%, turn at 15-33%, proof x3 in the middle 40%, hero number ~75%, logo hold 3-4.5 s |
| Voice | 1.6-2.1 words/s; a new line every 2-3 s; each word lands 0-4 frames before it is spoken |
| Breath before a hit | 0.15-0.5 s, 9-18 dB down; then the loudest moment of the film on the brand name |
| Motion budget | moving frames 33-55% (voice-led) / 55-70% (montage); still ≤ 35%; nothing static > 2 s before the end |
| Camera (approved) | kick 2.2% push, clap 0.3° + 4 px, cut whip 70 px, hit 10% + white flash 0.32 s; intro/outro only |
| Cuts on beat (montage) | ≥ 40% within 1 frame of an 8th, 0-2 frames early |
| Mix loudness | music-only about −9 LUFS (refs −8.1 to −11.5); with voice −12 to −14.5 LUFS |
| Safe area | content inside the central 90%; text inside 80% |

## Fixes for failures you'll hit

| Symptom | Fix |
|---|---|
| Frame 0 empty (`first_frame_empty`) | land the hook line on f0 with `tl.set(words, {opacity:1}, 0)`; animate the shape, not the words |
| `line_unread` | hold the line longer or cut words; shift everything after with the `at()` helper |
| Repeated fromTo snaps to the wrong state when scrubbing | `immediateRender: false` on every fromTo after the first on that target |
| `overlapping_gsap_tweens` on x | end the entrance before the move starts |
| Elements show through a card while it fades in | fade the elements out before the card passes 50% opacity, or shrink them into the card's avatar |
| Music drop lands a few frames off | compute when the hero event actually happens on its ease, not when its tween starts; move the tween start, not the audio |
| A font silently falls back | `@font-face` inside every scene `<template>` that uses it, with a file in `assets/fonts/` |
