from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/contributions.json').read_text())
s=data.get('stats',{})
monthly=s.get('monthly',{})
W,H=900,470
items=[
('CURRENT STREAK',f"{s.get('current_streak',0)} days"),
('LONGEST STREAK',f"{s.get('longest_streak',0)} days"),
('CONTRIBUTIONS',f"{s.get('total',0):,}"),
('ACTIVE DAYS',f"{s.get('active_days',0)}"),
('BEST DAY',f"{s.get('best_day',{}).get('count',0)}"),
('AVG / ACTIVE DAY',f"{s.get('average_active_day',0)}"),]
svg=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" rx="18" fill="#fff"/><rect x="1" y="1" width="898" height="468" rx="18" fill="none" stroke="#171717"/>
<circle cx="25" cy="25" r="5" fill="#111"/><circle cx="43" cy="25" r="5" fill="#777"/><circle cx="61" cy="25" r="5" fill="#bbb"/>
<text x="82" y="30" font-family="monospace" font-size="13" fill="#111">afzal@github:~$ ./stats.sh</text>
<line x1="20" y1="45" x2="880" y2="45" stroke="#ddd"/>''']
for i,(label,val) in enumerate(items):
    col=i%2; row=i//2; x=28+col*425; y=72+row*72
    svg.append(f'<rect x="{x}" y="{y}" width="400" height="58" rx="8" fill="#fafafa" stroke="#e4e4e4"/>')
    svg.append(f'<text x="{x+18}" y="{y+20}" font-family="monospace" font-size="9" fill="#777">{label}</text>')
    svg.append(f'<text x="{x+18}" y="{y+44}" font-family="monospace" font-size="18" font-weight="700" fill="#111">{val}</text>')
svg.append('<text x="28" y="305" font-family="monospace" font-size="11" fill="#555">MONTHLY CONTRIBUTIONS</text>')
months=list(monthly.items())[-12:]
maxv=max([v for _,v in months],default=1)
base=425
for i,(m,v) in enumerate(months):
    x=35+i*70; bh=100*v/maxv if maxv else 0; y=base-bh
    svg.append(f'<rect x="{x}" y="{y:.1f}" width="42" height="{bh:.1f}" rx="4" fill="#111"><title>{m}: {v}</title></rect>')
    svg.append(f'<text x="{x+21}" y="444" text-anchor="middle" font-family="monospace" font-size="9" fill="#666">{m[5:]}</text>')
svg.append('<text x="28" y="458" font-family="monospace" font-size="10" fill="#777">afzal@github:~$ <tspan fill="#111">echo "keep building"</tspan></text></svg>')
(ROOT/'stats.svg').write_text('\n'.join(svg),encoding='utf-8')
