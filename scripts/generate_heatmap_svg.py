from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

PALETTE = ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"]
W, H = 1200, 270
LEFT, TOP = 52, 62
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
<text x="1145" y="30" text-anchor="end" font-family="monospace" font-size="11" fill="#777">[ {stats.get('total', 0):,} contributions ]</text>
<line x1="20" y1="45" x2="1180" y2="45" stroke="#ddd"/>
<text x="18" y="79" font-family="monospace" font-size="10" fill="#777">Sun</text>
<text x="18" y="111" font-family="monospace" font-size="10" fill="#777">Tue</text>
<text x="18" y="143" font-family="monospace" font-size="10" fill="#777">Thu</text>
<text x="18" y="175" font-family="monospace" font-size="10" fill="#777">Sat</text>
''']
    for x, y, key, count, level in cells:
        svg.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{PALETTE[level]}" data-date="{key}" data-count="{count}"/>')
    legend_y = 205
    svg.append(f'''<text x="52" y="{legend_y+18}" font-family="monospace" font-size="11" fill="#555">Less</text>''')
    for i, c in enumerate(PALETTE):
        svg.append(f'<rect x="88" y="{legend_y+7}" width="13" height="13" rx="2" fill="{c}"/>')
    svg.append(f'''<text x="170" y="{legend_y+18}" font-family="monospace" font-size="11" fill="#555">More</text>
<text x="420" y="{legend_y+18}" font-family="monospace" font-size="11" fill="#111">streak: {stats.get('current_streak',0)} days</text>
<text x="650" y="{legend_y+18}" font-family="monospace" font-size="11" fill="#111">best: {stats.get('best_day',{}).get('count',0)} on {stats.get('best_day',{}).get('date','—')}</text>
<style>@media (prefers-reduced-motion:no-preference) {{ rect[data-date] {{ opacity:0; animation: pop .18s ease-out forwards; }} @keyframes pop {{ to {{ opacity:1; }} }} }}</style>
</svg>''')
    OUT.write_text("\n".join(svg), encoding="utf-8")

if __name__ == "__main__": main()
