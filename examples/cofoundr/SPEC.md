GOAL:    the viewer understands what cofoundr does in one pass: paste your LinkedIn, an agent
         searches 700M profiles, scores 30, and hands back 10 ranked co-founders with intro drafts.
OUTPUT:  HyperFrames, 1080 x 1080, 60 fps (square for the X feed)
TIME:    15.0 s x 60 = 900 frames. Silent by design (X autoplays muted); type and pictures carry it.
LOOK:    ground #f0f2f8 (the app shell), ink #0f172a, muted ink #64748b, rule #d8dceb.
         accent #3b5bdb = "you", one focus per frame. tint #818cf8 = "the co-founder", appears only
         from the match card on. These two are the logo's two circles.
         display Instrument Serif 400, 104 px hook / 132 px wordmark, tracking -1%.
         body Inter 500/700, 30-40 px, tracking -1%.
         medium: the real product UI. White cards #fff, radius 28, shadow 0 18px 40px rgba(15,23,42,.08).
OBJECTS: input card (avatar circle, LinkedIn URL field, "need: technical" tag), the real 4-stage
         pipeline rail from /api/match (A enrich, B search, C score, D intros), a profile field
         (dots), a score bar chart (30 bars), a match card (avatar, title, score, intro draft),
         the logo (two circles r15, centres 20 apart, scaled).
MOTION:  enter expo.out 0.6 s; carry/camera power3.inOut 0.7 s; exit power3.in 0.3 s.
         words blur 8->0 px in 0.13 s, 0.08 s apart. letters typed 2 frames apart.
         dot stagger 0.6 s total from centre out. bar sort 0.8 s power3.inOut, 6 ms stagger.
         one spring only: the logo circles meeting, back.out(1.4).
SHOTS:   0-180 f    hook. Big blue circle right, alone. "i couldn't find a cofounder." left-aligned,
                    per-word blur-in from 15 f. Holds. 150-180 f circle shrinks into card avatar spot.
         180-276 f  input card lands, URL types, tag lands. Rail appears, node A lights at 234 f.
         276-408 f  card carries up-left; 700M field of dots spreads out; counter "700M profiles".
                    Node B lights at 288 f. At 360 f all but 30 dots dim; counter becomes "30 candidates".
         408-552 f  the 30 lit dots become 30 bars, sorted by score. Top 10 stay blue, rest grey.
                    Weights line "availability 40 · skill 35 · culture 25". Node C lights at 414 f.
         552-684 f  bars fold into one match card: tint avatar, "Founding Engineer, Bengaluru",
                    score 9.1, intro draft types. Node D lights at 558 f.
         684-900 f  payoff. Blue and tint circles slide together into the logo, "cofoundr" blurs in,
                    "10 ranked co-founders. about 60 seconds." per word. Holds to the end (>2 s).
BANNED:  dark navy void, glow, bloom, particles, purple/blue gradients, glass cards, mono caps labels,
         pill chips, everything centred, every element fading and sliding up, titles drifting after
         landing, logo in a corner, three cards in a row, KPI grids, real people's names or faces.
QA:      f0 not empty; f120 hook readable; f250 URL fully typed; f380 30 lit dots; f520 sorted bars;
         f660 intro draft readable; f899 logo + wordmark + line, all still.
