#!/usr/bin/env python3
"""Render a printable Cradio layout reference from config/cradio.keymap."""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KEYMAP = ROOT / "config" / "cradio.keymap"
DEFAULT_MARKDOWN = ROOT / "docs" / "layouts" / "current-layout.md"
DEFAULT_SVG = ROOT / "docs" / "layouts" / "current-layout.svg"
DEFAULT_HTML = ROOT / "docs" / "layouts" / "current-layout.html"

LAYER_BLOCKS = {
    "default_layer": "DEFAULT",
    "left_layer": "LFT",
    "right_layer": "RGT",
    "tri_layer": "TRI",
}

KEY_LABELS = {
    "SEMI": ";",
    "COLON": ":",
    "COMMA": ",",
    "DOT": ".",
    "FSLH": "/",
    "BSLH": "\\",
    "PIPE": "|",
    "TILDE": "~",
    "LBRC": "{",
    "RBRC": "}",
    "LBKT": "[",
    "RBKT": "]",
    "LPAR": "(",
    "RPAR": ")",
    "CARET": "^",
    "ASTRK": "*",
    "PRCNT": "%",
    "DLLR": "$",
    "EXCL": "!",
    "HASH": "#",
    "AT": "@",
    "AMPS": "&",
    "MINUS": "-",
    "EQUAL": "=",
    "PLUS": "+",
    "UNDER": "_",
    "GRAVE": "`",
    "BSPC": "BSP",
    "SPACE": "Space",
    "ENTER": "Enter",
    "TAB": "Tab",
    "ESC": "Esc",
    "DEL": "Del",
    "INS": "Ins",
    "HOME": "Home",
    "END": "End",
    "PG_DN": "PgDn",
    "PG_UP": "PgUp",
    "LARW": "Left",
    "DARW": "Down",
    "UARW": "Up",
    "RARW": "Right",
    "N0": "0",
    "N1": "1",
    "N2": "2",
    "N3": "3",
    "N4": "4",
    "N5": "5",
    "N6": "6",
    "N7": "7",
    "N8": "8",
    "N9": "9",
    "C_VOICE_COMMAND": "Voice",
}

BEHAVIOR_LABELS = {
    "trans": "",
    "none": "",
    "studio_unlock": "Studio",
    "caps_word": "Caps",
    "sys_reset": "Reset",
    "bootloader": "Boot",
    "da_ae": "AE",
    "da_oe": "OE",
    "sv_ao": "AA",
    "sv_ae": "A-um",
    "sv_oe": "O-um",
}

MOD_LABELS = {
    "LSHFT": "Shift",
    "RSHFT": "Shift",
    "LALT": "Alt",
    "RALT": "Alt",
    "LCTRL": "Ctrl",
    "RCTRL": "Ctrl",
    "LGUI": "Gui",
    "RGUI": "Gui",
}

CATEGORY_COLORS = {
    "base": "#111827",
    "mod": "#b45309",
    "lft": "#1d4ed8",
    "rgt": "#047857",
    "tri": "#be123c",
    "muted": "#9ca3af",
}

MARKDOWN_LABELS = {
    "Tab": "TAB",
    "Enter": "ENTER",
    "Space": "SPACE",
    "Esc": "ESC",
    "Ins": "INS",
    "Del": "DEL",
    "Caps": "CAPS",
    "Home": "HOME",
    "PgDn": "PGDN",
    "PgUp": "PGUP",
    "End": "END",
    "Left": "LEFT",
    "Down": "DOWN",
    "Up": "UP",
    "Right": "RIGHT",
}

MARKDOWN_MODS = {
    "Shift": "SFT",
    "Ctrl": "CTL",
}

KEY_POSITION_INDEXES = {
    "LT4": 0,
    "LT3": 1,
    "LT2": 2,
    "LT1": 3,
    "LT0": 4,
    "RT0": 5,
    "RT1": 6,
    "RT2": 7,
    "RT3": 8,
    "RT4": 9,
    "LM4": 10,
    "LM3": 11,
    "LM2": 12,
    "LM1": 13,
    "LM0": 14,
    "RM0": 15,
    "RM1": 16,
    "RM2": 17,
    "RM3": 18,
    "RM4": 19,
    "LB4": 20,
    "LB3": 21,
    "LB2": 22,
    "LB1": 23,
    "LB0": 24,
    "RB0": 25,
    "RB1": 26,
    "RB2": 27,
    "RB3": 28,
    "RB4": 29,
    "LH1": 30,
    "LH0": 31,
    "RH0": 32,
    "RH1": 33,
}

KEY_POSITION_LABELS = {
    "LH1": "left outer thumb",
    "LH0": "left inner thumb",
    "RH0": "right inner thumb",
    "RH1": "right outer thumb",
}


@dataclass(frozen=True)
class Combo:
    name: str
    binding: str
    key_positions: list[str]
    layers: list[str]
    timeout_ms: str


def strip_comments(text: str) -> str:
    return re.sub(r"//.*", "", text)


def find_block(text: str, name: str, start: int = 0) -> str:
    name_match = re.search(rf"\b{re.escape(name)}\b\s*\{{", text[start:])
    if not name_match:
        raise ValueError(f"Could not find block: {name}")

    open_brace = start + name_match.end() - 1
    depth = 0
    for i in range(open_brace, len(text)):
        char = text[i]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[open_brace + 1 : i]

    raise ValueError(f"Unterminated block: {name}")


def extract_binding_blocks(text: str) -> dict[str, str]:
    keymap = find_block(text, "keymap")
    blocks: dict[str, str] = {}
    for block_name, layer_name in LAYER_BLOCKS.items():
        layer_block = find_block(keymap, block_name)
        match = re.search(r"bindings\s*=\s*<(?P<body>.*?)>;", layer_block, flags=re.S)
        if not match:
            raise ValueError(f"Could not find bindings for {block_name}")
        blocks[layer_name] = match.group("body")
    return blocks


def clean_key_label(token: str) -> str:
    return KEY_LABELS.get(token, token)


def parse_macro_args(tokens: list[str], start: int) -> tuple[str, list[str], int]:
    parts = [tokens[start]]
    i = start
    while ")" not in parts[-1]:
        i += 1
        if i >= len(tokens):
            raise ValueError(f"Unterminated macro starting at {tokens[start]}")
        parts.append(tokens[i])
    macro = " ".join(parts)
    name, arg_text = macro.split("(", 1)
    args = [arg.strip() for arg in arg_text.rstrip(")").split(",")]
    return name, args, i + 1


def label_for_binding(behavior: str, args: list[str]) -> str:
    if behavior == "kp":
        return clean_key_label(args[0])
    if behavior == "lt":
        layer, tap = args
        return f"{clean_key_label(tap)}/{layer}"
    if behavior == "ht":
        mod, tap = args
        return f"{clean_key_label(tap)}/{MOD_LABELS.get(mod, mod)}"
    if behavior == "bt":
        action = args[0]
        if action == "BT_CLR":
            return "BTClr"
        if action == "BT_SEL" and len(args) > 1:
            return f"BT{args[1]}"
        return action.removeprefix("BT_")
    return BEHAVIOR_LABELS.get(behavior, behavior)


def parse_single_binding(binding: str) -> str:
    tokens = binding.split()
    if not tokens or not tokens[0].startswith("&"):
        return binding

    behavior = tokens[0][1:]
    args = tokens[1:]
    return label_for_binding(behavior, args)


def split_macro_args(arg_text: str) -> list[str]:
    args: list[str] = []
    current = []
    depth = 0
    for char in arg_text:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    if current:
        args.append("".join(current).strip())
    return args


def parse_combos(text: str) -> list[Combo]:
    combos: list[Combo] = []
    for match in re.finditer(r"ZMK_COMBO\((?P<args>.*?)\)", strip_comments(text), flags=re.S):
        args = split_macro_args(match.group("args"))
        if len(args) < 3:
            continue
        combos.append(
            Combo(
                name=args[0],
                binding=parse_single_binding(args[1]),
                key_positions=args[2].split(),
                layers=args[3].split() if len(args) >= 4 else [],
                timeout_ms=args[4] if len(args) >= 5 else "30",
            )
        )
    return combos


def parse_bindings(body: str) -> list[str]:
    body = strip_comments(body)
    tokens = body.split()
    bindings: list[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.startswith("HRML(") or token.startswith("HRMR("):
            macro, args, i = parse_macro_args(tokens, i)
            if len(args) != 4:
                raise ValueError(f"{macro} expected 4 args, got {args}")
            mods = ["Shift", "Alt", "Ctrl", "Gui"] if macro == "HRML" else ["Gui", "Ctrl", "Alt", "Shift"]
            bindings.extend(f"{clean_key_label(key)}/{mod}" for key, mod in zip(args, mods))
            continue
        if token.startswith("&"):
            behavior = token[1:]
            if behavior in {"trans", "none", "studio_unlock", "caps_word", "sys_reset", "bootloader"}:
                bindings.append(label_for_binding(behavior, []))
                i += 1
            elif behavior in {"da_ae", "da_oe", "sv_ao", "sv_ae", "sv_oe"}:
                bindings.append(label_for_binding(behavior, []))
                i += 1
            elif behavior == "kp":
                bindings.append(label_for_binding(behavior, [tokens[i + 1]]))
                i += 2
            elif behavior == "lt":
                bindings.append(label_for_binding(behavior, [tokens[i + 1], tokens[i + 2]]))
                i += 3
            elif behavior == "bt":
                if tokens[i + 1] == "BT_SEL":
                    bindings.append(label_for_binding(behavior, [tokens[i + 1], tokens[i + 2]]))
                    i += 3
                else:
                    bindings.append(label_for_binding(behavior, [tokens[i + 1]]))
                    i += 2
            else:
                raise ValueError(f"Unsupported binding behavior: {behavior}")
        else:
            raise ValueError(f"Unexpected token: {token}")
    if len(bindings) != 34:
        raise ValueError(f"Expected 34 bindings, got {len(bindings)}: {bindings}")
    return bindings


def parse_keymap(path: Path) -> dict[str, list[str]]:
    text = path.read_text()
    return {layer: parse_bindings(body) for layer, body in extract_binding_blocks(text).items()}


def parse_layout(path: Path) -> tuple[dict[str, list[str]], list[Combo]]:
    text = path.read_text()
    labels = {layer: parse_bindings(body) for layer, body in extract_binding_blocks(text).items()}
    return labels, parse_combos(text)


def key_positions() -> list[tuple[float, float]]:
    positions: list[tuple[float, float]] = []
    key_w = 72
    key_h = 62
    gap = 10
    half_gap = 52
    x0 = 36
    y0 = 96
    right_x0 = x0 + 5 * (key_w + gap) + half_gap

    for row in range(3):
        y = y0 + row * (key_h + gap)
        for col in range(5):
            positions.append((x0 + col * (key_w + gap), y))
        for col in range(5):
            positions.append((right_x0 + col * (key_w + gap), y))

    thumb_y = y0 + 3 * (key_h + gap) + 14
    positions.extend(
        [
            (x0 + 3 * (key_w + gap), thumb_y),
            (x0 + 4 * (key_w + gap), thumb_y),
            (right_x0, thumb_y),
            (right_x0 + (key_w + gap), thumb_y),
        ]
    )
    return positions


def split_base_label(label: str) -> tuple[str, str]:
    if "/" not in label or label == "/":
        return label, ""
    base, mod = label.split("/", 1)
    return base, mod


def hold_color(hold_label: str) -> str:
    if hold_label == "LFT":
        return CATEGORY_COLORS["lft"]
    if hold_label == "RGT":
        return CATEGORY_COLORS["rgt"]
    if hold_label == "TRI":
        return CATEGORY_COLORS["tri"]
    return CATEGORY_COLORS["mod"]


def svg_text(x: float, y: float, text: str, size: int, color: str, anchor: str = "middle", weight: str = "500") -> str:
    if not text:
        return ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(text)}</text>'
    )


def render_key(index: int, x: float, y: float, labels: dict[str, list[str]]) -> str:
    key_w = 72
    key_h = 62
    base, mod = split_base_label(labels["DEFAULT"][index])
    lft = labels["LFT"][index]
    rgt = labels["RGT"][index]
    tri = labels["TRI"][index]
    parts = [
        f'<g class="key" data-index="{index}">',
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{key_w}" height="{key_h}" rx="8" ry="8" />',
        svg_text(x + key_w / 2, y + 39, base, 18, CATEGORY_COLORS["base"], weight="700"),
        svg_text(x + 8, y + 13, lft, 9, CATEGORY_COLORS["lft"], anchor="start", weight="600"),
        svg_text(x + key_w - 8, y + 13, rgt, 9, CATEGORY_COLORS["rgt"], anchor="end", weight="600"),
        svg_text(x + key_w / 2, y + 25, tri, 8, CATEGORY_COLORS["tri"], anchor="middle", weight="700"),
        svg_text(x + key_w / 2, y + key_h - 8, mod, 9, hold_color(mod), anchor="middle", weight="700"),
        "</g>",
    ]
    return "\n".join(part for part in parts if part)


def render_combo_annotations(combos: list[Combo], positions: list[tuple[float, float]]) -> str:
    key_w = 72
    key_h = 62
    parts: list[str] = []
    for combo in combos:
        indexes = [KEY_POSITION_INDEXES[position] for position in combo.key_positions if position in KEY_POSITION_INDEXES]
        if len(indexes) < 2:
            continue
        centers = [(positions[index][0] + key_w / 2, positions[index][1] + key_h / 2) for index in indexes]
        x1, y1 = centers[0]
        x2, y2 = centers[-1]
        label_x = (x1 + x2) / 2
        label_y = max(y1, y2) + 52
        parts.extend(
            [
                f'<line x1="{x1:.1f}" y1="{y1 + 28:.1f}" x2="{x2:.1f}" y2="{y2 + 28:.1f}" stroke="#7c3aed" stroke-width="2.5" stroke-linecap="round" />',
                f'<circle cx="{x1:.1f}" cy="{y1 + 28:.1f}" r="4" fill="#7c3aed" />',
                f'<circle cx="{x2:.1f}" cy="{y2 + 28:.1f}" r="4" fill="#7c3aed" />',
                svg_text(label_x, label_y, f"combo: {combo.binding}", 10, "#6d28d9", weight="700"),
            ]
        )
    return "\n".join(parts)


def render_svg(labels: dict[str, list[str]], combos: list[Combo]) -> str:
    positions = key_positions()
    width = 916
    height = 430
    keys = "\n".join(render_key(i, x, y, labels) for i, (x, y) in enumerate(positions))
    combo_annotations = render_combo_annotations(combos, positions)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Current Cradio Layout</title>
  <desc id="desc">Printable generated reference for the active Cradio keymap.</desc>
  <style>
    svg {{ background: #ffffff; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .key rect {{ fill: #f9fafb; stroke: #d1d5db; stroke-width: 1.25; }}
    .legend text {{ font-size: 12px; }}
    .title {{ font-size: 24px; font-weight: 750; fill: #111827; }}
    .subtitle {{ font-size: 13px; fill: #4b5563; }}
  </style>
  <text x="36" y="38" class="title">Current Cradio Layout</text>
  <text x="36" y="62" class="subtitle">Center: DEFAULT. Top left: LFT. Top right: RGT. Top center: TRI utilities. Bottom center: held modifier/layer.</text>
  <g class="legend" transform="translate(590 28)">
    <text x="0" y="0" fill="{CATEGORY_COLORS['base']}">DEFAULT</text>
    <text x="92" y="0" fill="{CATEGORY_COLORS['lft']}">LFT</text>
    <text x="138" y="0" fill="{CATEGORY_COLORS['rgt']}">RGT</text>
    <text x="184" y="0" fill="{CATEGORY_COLORS['tri']}">TRI</text>
    <text x="230" y="0" fill="{CATEGORY_COLORS['mod']}">hold</text>
    <text x="282" y="0" fill="#6d28d9">combo</text>
  </g>
  <line x1="458" y1="88" x2="458" y2="386" stroke="#e5e7eb" stroke-width="2" stroke-dasharray="6 6" />
  {keys}
  {combo_annotations}
</svg>
"""


def render_html(svg: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Current Cradio Layout</title>
  <style>
    :root {{ color-scheme: light; }}
    body {{
      margin: 0;
      padding: 24px;
      background: #eef2f7;
      color: #111827;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{
      max-width: 1100px;
      margin: 0 auto;
      background: white;
      border: 1px solid #d1d5db;
      border-radius: 12px;
      padding: 18px;
      box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
    }}
    svg {{ width: 100%; height: auto; display: block; }}
    @media print {{
      @page {{ size: A4 landscape; margin: 8mm; }}
      body {{ padding: 0; background: white; }}
      main {{ border: 0; box-shadow: none; padding: 0; max-width: none; }}
    }}
  </style>
</head>
<body>
  <main>
{svg}
  </main>
</body>
</html>
"""


def markdown_label(label: str) -> str:
    if not label:
        return "."
    if "/" in label:
        tap, hold = label.split("/", 1)
        return f"{MARKDOWN_LABELS.get(tap, tap)}/{MARKDOWN_MODS.get(hold, hold).upper()}"
    return MARKDOWN_LABELS.get(label, label)


def format_markdown_row(layer: list[str], start: int) -> str:
    cell_width = 7
    left = [markdown_label(label).ljust(cell_width) for label in layer[start : start + 5]]
    right = [markdown_label(label).ljust(cell_width) for label in layer[start + 5 : start + 10]]
    return f"  {' '.join(left)} | {' '.join(right)}".rstrip()


def format_markdown_thumbs(layer: list[str]) -> str:
    cell_width = 7
    left = [markdown_label(label).ljust(cell_width) for label in layer[30:32]]
    right = [markdown_label(label).ljust(cell_width) for label in layer[32:34]]
    return f"  {' ' * ((cell_width + 1) * 3)}{' '.join(left)} | {' '.join(right)}".rstrip()


def format_markdown_layer(labels: dict[str, list[str]], layer_name: str, title: str) -> str:
    layer = labels[layer_name]
    rows = [format_markdown_row(layer, 0), format_markdown_row(layer, 10), format_markdown_row(layer, 20)]
    rows.append(format_markdown_thumbs(layer))
    return f"{title}\n" + "\n".join(rows)


def describe_combo_position(position: str) -> str:
    return KEY_POSITION_LABELS.get(position, position)


def render_markdown_combos(combos: list[Combo]) -> str:
    if not combos:
        return "No combos are currently defined."

    lines = []
    for combo in combos:
        positions = " + ".join(combo.key_positions)
        descriptions = " + ".join(describe_combo_position(position) for position in combo.key_positions)
        layer_text = ", ".join(combo.layers) if combo.layers else "all layers"
        lines.append(
            f"- `{positions}` ({descriptions}) -> `{combo.binding}` on `{layer_text}`; timeout `{combo.timeout_ms} ms`."
        )
    return "\n".join(lines)


def render_markdown(labels: dict[str, list[str]], combos: list[Combo]) -> str:
    compact_layers = [
        format_markdown_layer(labels, "DEFAULT", "DEFAULT"),
        format_markdown_layer(labels, "LFT", "LFT symbols"),
        format_markdown_layer(labels, "RGT", "RGT numbers/nav"),
        format_markdown_layer(labels, "TRI", "TRI system"),
    ]
    compact_sections = "\n\n".join(compact_layers)
    detail_layers = [
        format_markdown_layer(labels, "DEFAULT", "## DEFAULT"),
        format_markdown_layer(labels, "RGT", "## RGT"),
        format_markdown_layer(labels, "LFT", "## LFT"),
        format_markdown_layer(labels, "TRI", "## TRI"),
    ]
    detail_blocks = []
    for section in detail_layers:
        heading, *rows = section.splitlines()
        detail_blocks.append(f"{heading}\n\n```text\n{chr(10).join(rows)}\n```")
    detail_sections = "\n\n".join(detail_blocks)

    return f"""# Current Cradio Layout

Source: `../../config/cradio.keymap`

This is the generated human-readable reference for the currently active keymap. Regenerate it after keymap edits, especially after edits made through ZMK Studio.

Generated printable reference:

- `current-layout.html`
- `current-layout.svg`

Open `current-layout.html` in a browser for the printable view. Use browser print / save as PDF for a one-page PDF copy.

Regenerate all layout references with:

```bash
just layout-ref
```

## Compact Reference

```text
Access
  hold left thumb TAB  -> LFT symbols
  hold right thumb BSP -> RGT numbers/nav
  hold both LFT + RGT  -> TRI system

{compact_sections}
```

Dots represent transparent keys.

## Layer Summary

- `DEFAULT`: typing, Colemak-style base, home-row mods.
- `RGT`: numbers, navigation, Scandinavian characters.
- `LFT`: symbols and ZMK Studio unlock.
- `TRI`: system, bootloader/reset, Bluetooth profile selection.
- `extra1`: reserved.
- `extra2`: reserved.

## Access

- Hold left thumb `TAB` for `LFT`.
- Hold right thumb `BSPC` for `RGT`.
- Hold both `LFT` and `RGT` for `TRI`.
- `extra1` and `extra2` are not reachable yet.

## Combos

{render_markdown_combos(combos)}

{detail_sections}

Dots represent transparent keys.

## Notes

- Center labels come from `DEFAULT`.
- Top-left labels in the SVG are `LFT`.
- Top-right labels in the SVG are `RGT`.
- Top-center red labels in the SVG are `TRI`.
- Bottom-center labels in the SVG are held modifiers or held layers from `DEFAULT`.
- Purple markings in the SVG are combos.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keymap", type=Path, default=DEFAULT_KEYMAP)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--svg", type=Path, default=DEFAULT_SVG)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    args = parser.parse_args()

    labels, combos = parse_layout(args.keymap)
    svg = render_svg(labels, combos)
    args.markdown.write_text(render_markdown(labels, combos))
    args.svg.write_text(svg)
    args.html.write_text(render_html(svg))
    print(f"Wrote {args.markdown}")
    print(f"Wrote {args.svg}")
    print(f"Wrote {args.html}")


if __name__ == "__main__":
    main()
