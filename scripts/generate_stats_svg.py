from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/contributions.json').read_text())
s = data

monthly_list = s.get('monthly', [])
months = [(m['month'], m['total']) for m in monthly_list[-12:]]

W, H = 900, 940
items = [
    ('CURRENT STREAK', f"{s.get('current_streak', {}).get('length', 0)} days"),
    ('LONGEST STREAK', f"{s.get('longest_streak', {}).get('length', 0)} days"),
    ('CONTRIBUTIONS', f"{s.get('total_contributions', 0):,}"),
    ('ACTIVE DAYS', f"{s.get('active_days', 0)}"),
    ('BEST DAY', f"{s.get('best_day', {}).get('count', 0)}"),
    ('AVG / ACTIVE DAY', f"{s.get('avg_per_active_day', 0)}")
]

svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" rx="18" fill="#fff"/><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="none" stroke="#171717"/>
<circle cx="25" cy="25" r="5" fill="#111"/><circle cx="43" cy="25" r="5" fill="#777"/><circle cx="61" cy="25" r="5" fill="#bbb"/>
<text x="82" y="30" font-family="monospace" font-size="13" fill="#111">afzal@github:~$ ./stats.sh</text>
<line x1="20" y1="45" x2="{W-20}" y2="45" stroke="#ddd"/>''']

for i, (label, val) in enumerate(items):
    col = i % 2
    row = i // 2
    x = 35 + col * 420
    y = 100 + row * 120
    svg.append(f'<rect x="{x}" y="{y}" width="410" height="90" rx="8" fill="#fafafa" stroke="#e4e4e4"/>')
    svg.append(f'<text x="{x+25}" y="{y+35}" font-family="monospace" font-size="12" fill="#777">{label}</text>')
    svg.append(f'<text x="{x+25}" y="{y+75}" font-family="monospace" font-size="30" font-weight="700" fill="#111">{val}</text>')

svg.append('<text x="35" y="520" font-family="monospace" font-size="13" fill="#555">MONTHLY CONTRIBUTIONS</text>')

maxv = max([v for _, v in months], default=1)
base = 830

for i, (m, v) in enumerate(months):
    x = 42 + i * 70
    bh = 260 * v / maxv if maxv else 0
    y = base - bh
    svg.append(f'<rect x="{x}" y="{y:.1f}" width="45" height="{bh:.1f}" rx="4" fill="#111"><title>{m}: {v}</title></rect>')
    svg.append(f'<text x="{x+22}" y="855" text-anchor="middle" font-family="monospace" font-size="11" fill="#666">{m[5:]}</text>')

svg.append(f'<text x="35" y="905" font-family="monospace" font-size="12" fill="#777">afzal@github:~$ <tspan fill="#111">echo "keep building"</tspan></text></svg>')

(ROOT / 'stats.svg').write_text('\n'.join(svg), encoding='utf-8')
