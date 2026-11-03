# motion-lab

An agent skill for making short motion graphics videos (product showcases, pipeline explainers, launch clips) as code with [HyperFrames](https://github.com/heygen-com/hyperframes).

The agent writes a spec where every adjective is a number, builds one worked example that moves through the real mechanism, checks the frames, syncs the music drop to an exact frame by measuring loudness, and renders a square 60 fps MP4.

Example output: [`examples/cofoundr/preview.mp4`](examples/cofoundr/preview.mp4), a 17 s, 1,020-frame film of an AI co-founder search pipeline.

## Use it

**Claude Code**

```bash
git clone https://github.com/codeswithroh/motion-lab ~/.claude/skills/motion-lab
```

Then ask: "make a motion graphics video of how X works".

**Any other agent** (Cursor, Codex, Gemini CLI, ChatGPT…)

Give it this link and say "read this skill and follow it":

```
https://github.com/codeswithroh/motion-lab/blob/main/SKILL.md
```

Or clone the repo into the project and point the agent at `SKILL.md`.

## Requirements

- Node 18+ (`npx hyperframes`, pinned to 0.9.8 in the example)
- ffmpeg
- Python 3 with numpy, for `scripts/find_drop.py`

## What's inside

| Path | What it is |
|---|---|
| `SKILL.md` | The workflow: read the source, spec, story shape, look, build, review loop, music sync, delivery |
| `references/numbers.md` | Eases, durations, hold times, text sizes, and fixes for common check failures |
| `references/spec-template.md` | The SPEC.md the agent fills in before building |
| `references/sound.md` | Synthesizing a score from frame numbers when there's no track |
| `scripts/find_drop.py` | Finds a track's biggest drops and the start offset that lands one on a given frame |
| `examples/cofoundr/` | The full reference build: scenes, spec, review notes |

## Running the example

```bash
cd examples/cofoundr
npx hyperframes preview
```

The original music is licensed and not included. Put any track at `assets/audio/luxe.mp3`, then run `python3 ../../scripts/find_drop.py assets/audio/luxe.mp3 --hero 14.1` and set `data-media-start` in `index.html` to the value it prints.
