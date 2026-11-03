# Sound without a track: score from frame numbers

Use only when the person has no track and agrees to a synthesized score. The model can't hear,
so every decision comes from frame numbers and every fix from measuring the decoded audio.

## The score prompt shape

```text
Score this <s> s film (<frames> frames, 60 fps). Synthesize everything in code (numpy or the Web
Audio API), no samples. Each hit lands 1 frame after its visual event.
Bed: <BPM>, bars starting on frames <list>. Kick on <frames>, sub and pad on <chords>.
Events: <event name> at <frame>, … (one per visible action: a card landing, a node lighting,
the bars sorting, the logo meeting).
48 kHz stereo WAV, about -14 LUFS, peak -1 dBTP, no click at the start or end. Mux into the MP4.
```

## Measured follow-ups that came up every time

1. Hits peak late: a waveshaper or a sine starting at phase 0 moves the peak 8-11 ms after the
   frame. Build each tonal hit so its attack ends on a cosine crest at exactly (frame + 1) × 800 samples.
2. Levels uneven over the bed: put every hit 3-6 dB above the bed (K-weighted, first 60 ms).
3. Most energy under 60 Hz plays as nothing on a phone. Move bass up an octave, shorten the kick
   to ~80 ms with a ~190 Hz knock, raise the pad.
4. The limiter squashes a big hit when all its partials crest on one sample: lower what sits under it.
5. AAC adds ~16 ms of padding: for a loop, keep the WAV as master and add a 2 ms raised-cosine
   fade on the first and last 96 samples of the MP4 audio.
6. Remove DC: subtract each channel's mean.
