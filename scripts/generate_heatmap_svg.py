from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

PALETTE = ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"]
W, H = 880, 190
LEFT, TOP = 22, 62
CELL, GAP = 13, 3


def main():
    data = json.loads(DATA.read_text())
    days = {d["date"]: d["count"] for d in data.get("days", [])}
    stats = data.get("stats", {})

    if days:
        end = date.fromisoformat(max(days))
    else:
        end = date.today()
    start = end - timedelta(days=363)
    while start.weekday() != 6:
        start -= timedelta(days=1)

    cells = []
    months_seen = set()
    cur = start
    week = 0
    while cur <= end:
        dow = (cur.weekday() + 1) % 7
        x = LEFT + week * (CELL + GAP)
        y = TOP + dow * (CELL + GAP)
        key = cur.isoformat()
        count = days.get(key, 0)
        if count == 0: level = 0
        elif count <= 5: level = 1
        elif count <= 15: level = 2
        elif count <= 30: level = 3
        else: level = 4
        cells.append((x, y, key, count, level))
        if dow == 6:
            week += 1
        cur += timedelta(days=1)

    max_week = week + 1
    svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" rx="18" fill="#fff"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="none" stroke="#171717"/>
<circle cx="25" cy="25" r="5" fill="#111"/><circle cx="43" cy="25" r="5" fill="#777"/><circle cx="61" cy="25" r="5" fill="#bbb"/>
<text x="82" y="30" font-family="monospace" font-size="13" fill="#111">afzal@github:~$ ./contributions.sh</text>
<text x="{W-25}" y="30" text-anchor="end" font-family="monospace" font-size="11" fill="#777">[ {stats.get('total', 0):,} contributions ]</text>
<line x1="20" y1="45" x2="{W-20}" y2="45" stroke="#ddd"/>
''']
    for x, y, key, count, level in cells:
        svg.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{PALETTE[level]}" data-date="{key}" data-count="{count}"/>')
    svg.append(f'''<style>@media (prefers-reduced-motion:no-preference) {{ rect[data-date] {{ opacity:0; animation: pop .18s ease-out forwards; }} @keyframes pop {{ to {{ opacity:1; }} }} }}</style>
</svg>''')
    OUT.write_text("\n".join(svg), encoding="utf-8")

if __name__ == "__main__": main()
