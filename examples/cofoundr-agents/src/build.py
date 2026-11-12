"""Inline the apps' official marks into the scene files.

Marks: LobeHub icons (MIT) for Claude, Claude Code, Cursor, OpenAI; VS Code is Microsoft's
icon from code.visualstudio.com/brand (assets/brands/vscode.svg). Run: python3 src/build.py
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
brand_src = pathlib.Path.home() / "Work/cofoundr/src/components/BrandLogo.tsx"
paths = dict(re.findall(r'"(\w+)": (".*?"),\n', brand_src.read_text()))
paths = {k: json.loads(v) for k, v in paths.items()}

TILE_BG = {"claude": "#d97757", "chatgpt": "#0d0d0d", "cursor": "#111111", "claudecode": "#1f1e1d", "vscode": "#1e1e1e"}

def tile(m):
    parts = m.group(1).split(":")
    brand = parts[0]
    style = f"background:{TILE_BG[brand]};"
    if len(parts) > 1 and parts[1] not in ("static",):
        size = parts[1]
        style += f"width:{size}px;height:{size}px;"
    if len(parts) > 2:
        style += f"left:{parts[2]}px;"
    if brand == "vscode":
        inner = '<img src="assets/brands/vscode.svg" alt="" />'
    else:
        inner = f'<svg viewBox="0 0 24 24" fill="#fff" fill-rule="evenodd">{paths[brand]}</svg>'
    return f'<div class="tile" data-app="{brand}" style="{style}">{inner}</div>'

CHECK = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
# full-panel floods use each brand's own colour; VS Code uses Microsoft's white icon on its blue
FLOOD_BG = {"claude": "#d97757", "chatgpt": "#10a37f", "cursor": "#111111", "claudecode": "#2b2a27", "vscode": "#0065a9"}

def flood(m):
    brand, name = m.group(1), m.group(2)
    if brand == "vscode":
        inner = '<img src="assets/brands/vscode-alt.svg" alt="" />'
    else:
        inner = f'<svg viewBox="0 0 24 24" fill="#fff" fill-rule="evenodd">{paths[brand]}</svg>'
    return f'<div class="flood" data-app="{brand}" style="background:{FLOOD_BG[brand]}"><div class="logo">{inner}</div><div class="name">{name}</div></div>'

def mark(m):
    size = m.group(1) or "44"
    return f'<svg viewBox="0 0 64 64" width="{size}" height="{size}"><circle cx="22" cy="32" r="15" fill="#3b5bdb"/><circle cx="42" cy="32" r="15" fill="#818cf8"/></svg>'

MARK = '<svg viewBox="0 0 64 64" width="44" height="44"><circle cx="22" cy="32" r="15" fill="#3b5bdb"/><circle cx="42" cy="32" r="15" fill="#818cf8"/></svg>'

for name in ("agents", "payoff"):
    s = (ROOT / "src" / f"{name}.html").read_text()
    s = re.sub(r"\{\{TILE:([\w:]+)\}\}", tile, s).replace("{{CHECK}}", CHECK)
    s = re.sub(r"\{\{FLOOD:(\w+):([^}]+)\}\}", flood, s)
    s = re.sub(r"\{\{MARK(?::(\d+))?\}\}", mark, s)
    (ROOT / "compositions" / f"{name}.html").write_text(s)
    print("wrote", name)
