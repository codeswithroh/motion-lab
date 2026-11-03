# SPEC.md template (filled example: examples/cofoundr/SPEC.md)

```text
GOAL:    what the viewer understands or does at the end, one sentence, with the product's real numbers.
OUTPUT:  HyperFrames, 1080 x 1080, 60 fps (square for the X feed)
TIME:    <s> x 60 = <frames>. Music: <track>, <BPM>, drop at <track s> lands on frame <n>.
LOOK:    ground <hex> (the app shell), ink <hex>, muted <hex>, rule <hex>.
         accent <hex> = <what it means, e.g. "you">; second <hex> = <what it means>, appears only from <shot>.
         display <face> 400, <px> hook / <px> wordmark, tracking -1%.
         body Inter 500/700, 30-40 px, tracking -1%.
         medium: the real product UI. Cards #fff, radius 28, shadow 0 18px 40px rgba(15,23,42,.08).
OBJECTS: <input card>, <stage rail with the real stage names>, <one picture per stage>, <result card>, <logo>.
MOTION:  enter expo.out 0.6 s; carry/camera power3.inOut 0.7 s; exit power3.in 0.3 s.
         words blur 8->0 px in 0.13 s, 0.08 s apart. letters typed 2 frames apart.
         staggers: dots 0.6 s total from centre out, bars 6 ms.
         one spring only, on the payoff: back.out(1.4).
SHOTS:   0-180 f    hook. Line landed on f0, left-aligned. Brand shape beside it. 150-180 f shape carries into the card.
         180-… f    input card, input types, rail appears, node A lights.
         …          one line per stage: frame range, hero move, what's read, node that lights.
         …-end      payoff. Shapes meet as the logo on the drop, wordmark, one line with the numbers. Hold >2 s.
BANNED:  dark navy void, glow, bloom, particles, purple/blue gradients, glass cards, mono caps labels,
         pill chips, everything centred, fade-and-slide-up on everything, drifting titles, logo in a corner,
         three cards in a row, KPI grids, real people's names or faces, + anything the last review found.
QA:      f0 hook readable (thumbnail); one frame per stage showing its picture finished; the hero frame
         and the onset of the drop within 1 frame; last frame still.
```
