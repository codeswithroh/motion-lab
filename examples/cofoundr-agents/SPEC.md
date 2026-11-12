GOAL:    the viewer gets it in one pass: connect cofoundr to Claude, ChatGPT, Cursor, Claude Code or
         VS Code once, ask in chat, and the find_cofounders tool searches 700M profiles, scores 30
         and puts 10 ranked co-founders back in the chat. Sequel to the first cofoundr film.
OUTPUT:  HyperFrames, 1080 x 1080, 60 fps (square for X and LinkedIn)
TIME:    17.5 s x 60 = 1050 frames. Music: Ludlow (Epidemic, user's track), 144.1 BPM, hit at
         64.005 s lands on frame 887 (14.79 s), the frame the two logo circles touch.
LOOK:    v2: ground #f3efe6 (paper), ink #111111, muted #6b6558. Editorial: oversized serif, ink rules,
         a numbered chapter bar, flat brand-colour floods. (v1 used the app shell #f0f2f8.)
         accent #3b5bdb = "you", one focus per frame. tint #818cf8 = "the co-founder", appears only
         from the result rows on. These two are the logo's two circles.
         app tiles use each app's own mark on its tile colour (Claude #d97757, ChatGPT #0d0d0d,
         Cursor #111, Claude Code #1f1e1d, VS Code #1e1e1e); never recoloured.
         display Instrument Serif 400, 120 px hook / 150 px wordmark / 64-150 px numbers, tracking -1%.
         body Inter 500/700, 28-44 px, tracking -1%.
         medium: the real product UI. Cards #fff, radius 28, shadow 0 18px 40px rgba(15,23,42,.08).
OBJECTS: the consent card from /oauth/authorize (you ⇄ app tile, "Connect Claude to cofoundr",
         three permissions search / read / intro, searches-per-day 1 3 5 10 with 3 picked, Allow
         access); a chat card (Claude header, the user's message, the find_cofounders tool call);
         the 700M dot field narrowing to 30 then 10; the chat reply with ranked rows; the logo.
         Rail = the real agent flow: connect, ask, search 700M, 10 in chat.
MOTION:  enter expo.out 0.6 s; carry/camera power3.inOut 0.7 s; exit power3.in 0.3 s.
         words blur 8->0 px in 0.13 s, 0.07 s apart. letters typed 2 frames apart.
         app-slot swap: 0.18 s per app, blur 6 px cross-fade, 5 apps, lands on Claude.
         ticks 0.15 s apart. dot stagger 0.6 s total from centre out. rows 0.12 s apart.
         one spring only, on the payoff: back.out(1.4).
SHOTS:   0-180 f    hook. "now i just ask my agent." left, 120 px, "agent" in accent, landed on f0.
                    Blue circle right. 147-180 f: words blur out, circle carries into the consent
                    card's "you" spot.
         180-360 f  connect. Card lands. The app slot cycles ChatGPT, Cursor, VS Code, Claude Code,
                    lands on Claude; title word swaps with it. Three permissions tick. "3" picked.
                    Allow access presses; node "connect" lights at 348 f.
         360-492 f  ask. Card exits, circle carries to the chat bubble avatar. Message types
                    "find me a technical co-founder". Tool call "find_cofounders" appears. Node
                    "ask" lights.
         492-648 f  search. Circle to centre, 700M field spreads, counter "700M profiles";
                    30 stay lit "30 scored"; 10 of them keep the accent "10 ranked". Node lights.
         648-804 f  10 in chat. Reply card: "10 matches in 12 s", three ranked rows (score 9.9
                    first, real top score from the prod run), "+7 more, intro draft for each".
                    Node "10 in chat" lights.
         804-1020 f payoff. Blue and tint circles meet as the logo on the drop (850 f), "cofoundr"
                    blurs in, "now inside your agent." and the five app tiles. Holds still > 2 s.
BANNED:  dark navy void, glow, bloom, particles, purple/blue gradients, glass cards, mono caps labels,
         pill chips, everything centred, every element fading up, drifting titles, logo in a corner,
         three cards in a row, KPI grids, real people's names or faces (the prod run returned real
         people; the rows use roles only), recoloured app logos.
QA:      f0 hook readable; f300 Claude in the slot + ticks; f350 Allow pressed; f450 message typed +
         tool call; f560 700M field; f620 10 accent dots; f760 three rows readable; f850 circles
         touching = drop onset (±1 f); f1019 logo + wordmark + line + tiles, still.
