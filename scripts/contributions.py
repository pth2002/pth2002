"""Draw the profile's contribution card: a year of contributions as a
heatmap, a snake that eats its way through every active day, and the
streaks above it. Writes a dark and a light SVG.

    python scripts/contributions.py --user pth2002 --out dist
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import urllib.request
from pathlib import Path

SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
THEMES = {
    "dark": dict(panel="#121A27", line="#26344A", text="#E6EDF3", muted="#9AA7B8", faint="#5E6B7D",
                 accent="#4F8CFF", glow="#85B0FF",
                 levels=["#1A2333", "#1B3C73", "#2556AB", "#3572E0", "#4F8CFF"]),
    "light": dict(panel="#FFFFFF", line="#D8DEE4", text="#1F2328", muted="#57606A", faint="#8C959F",
                  accent="#2563EB", glow="#6D9CF2",
                  levels=["#EBEEF2", "#D9E6FD", "#A7C5FA", "#5B92F3", "#2563EB"]),
}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

CELL, GAP = 15, 4
STEP = CELL + GAP
GX, GY = 74, 172                      # grid origin
SPEED = 150                           # px per second along the snake's path


def fetch(user: str) -> tuple[list[dict], int]:
    req = urllib.request.Request(f"https://github.com/users/{user}/contributions",
                                 headers={"User-Agent": "profile-contributions"})
    page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    tips = {}
    for target, text in re.findall(r'<tool-tip[^>]*\sfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', page):
        match = re.match(r"\s*(\d+|No) contribution", html.unescape(text))
        tips[target] = 0 if not match or match.group(1) == "No" else int(match.group(1))
    days = []
    for cell in re.findall(r"<td[^>]*data-date=\"[^\"]+\"[^>]*>", page):
        date = re.search(r'data-date="([^"]+)"', cell).group(1)
        level = int(re.search(r'data-level="(\d)"', cell).group(1))
        ident = re.search(r'id="([^"]+)"', cell).group(1)
        days.append({"date": dt.date.fromisoformat(date), "level": level, "count": tips.get(ident, 0)})
    days.sort(key=lambda day: day["date"])
    total = re.search(r'id="js-contribution-activity-description"[^>]*>\s*([\d,]+)', page)
    return days, int(total.group(1).replace(",", "")) if total else sum(d["count"] for d in days)


def highlights(days: list[dict]) -> tuple[int, int, dict | None]:
    """Active days, the busiest week's total, and the busiest day."""
    active = sum(1 for day in days if day["count"] > 0)
    weeks: dict = {}
    for day in days:
        weeks[day["week"]] = weeks.get(day["week"], 0) + day["count"]
    best_week = max(weeks.values()) if weeks else 0
    busiest = max(days, key=lambda d: d["count"]) if days else None
    return active, best_week, busiest


def layout(days: list[dict]) -> list[dict]:
    start = days[0]["date"] - dt.timedelta(days=(days[0]["date"].weekday() + 1) % 7)   # Sunday
    for day in days:
        day["week"] = (day["date"] - start).days // 7
        day["row"] = (day["date"].weekday() + 1) % 7
        day["x"] = GX + day["week"] * STEP
        day["y"] = GY + day["row"] * STEP
    return days


def snake_route(days: list[dict]) -> tuple[str, dict, float]:
    """An orthogonal path through every active day, column by column, going
    down one column and up the next. Returns the path, the time the head
    reaches each day, and the loop length in seconds."""
    active = [d for d in days if d["count"] > 0]
    weeks = sorted({d["week"] for d in active})
    order = []
    for index, week in enumerate(weeks):
        column = sorted((d for d in active if d["week"] == week), key=lambda d: d["row"])
        order.extend(column if index % 2 == 0 else reversed(column))
    half = CELL / 2
    first_y = (order[0]["y"] if order else GY + 3 * STEP) + half
    first_x = (order[0]["x"] if order else GX) + half
    x, y = max(GX - 2 * STEP + half, first_x - 4 * STEP), first_y
    points, length, reach = [(x, y)], 0.0, {}
    for day in order:
        tx, ty = day["x"] + half, day["y"] + half
        for nx, ny in ((tx, y), (tx, ty)):           # across, then down or up
            if (nx, ny) != (x, y):
                length += abs(nx - x) + abs(ny - y)
                x, y = nx, ny
                points.append((x, y))
        reach[day["date"]] = length / SPEED
    end_x = x + 4 * STEP
    length += abs(end_x - x)
    points.append((end_x, y))
    path = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in points)
    loop = length / SPEED + 2.4                      # a beat before the grid refills
    return path, reach, loop


def card(days: list[dict], total: int, theme: dict) -> str:
    t = theme
    active, best_week, busiest = highlights(days)
    path, reach, loop = snake_route(days)
    weeks = max(d["week"] for d in days) + 1
    grid_w = weeks * STEP - GAP
    width = GX + grid_w + 40
    height = 356

    months, last = [], None
    for day in days:
        if day["row"] == 0 and day["date"].month != last:
            last = day["date"].month
            if day["week"] < weeks - 2:
                months.append(f'<text x="{day["x"]}" y="{GY - 12}" fill="{t["faint"]}">{MONTHS[last - 1]}</text>')
    weekdays = "".join(
        f'<text x="{GX - 12}" y="{GY + row * STEP + 12}" text-anchor="end" fill="{t["faint"]}">{name}</text>'
        for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")))

    cells = []
    for day in days:
        color = t["levels"][day["level"]]
        label = f'{day["count"]} contribution{"s" if day["count"] != 1 else ""} on {day["date"]:%b %d, %Y}'
        anim = ""
        if day["date"] in reach:
            te = min(reach[day["date"]] / loop, 0.95)
            anim = (f'<animate attributeName="fill" dur="{loop:.2f}s" repeatCount="indefinite" calcMode="linear" '
                    f'keyTimes="0;{te:.4f};{min(te + 0.004, 0.96):.4f};0.965;1" '
                    f'values="{color};{color};{t["levels"][0]};{t["levels"][0]};{color}"/>')
        cells.append(f'<rect x="{day["x"]}" y="{day["y"]}" width="{CELL}" height="{CELL}" rx="4" fill="{color}">'
                     f'<title>{label}</title>{anim}</rect>')

    segments = 9
    lag = STEP / SPEED * 0.82                       # one cell apart: a body, not a dotted line
    body = []
    for i in range(segments, 0, -1):
        size = CELL - 2 - i * 0.65
        opacity = 1 - i * 0.07
        body.append(f'''<g opacity="0">
      <rect x="{-size / 2:.2f}" y="{-size / 2:.2f}" width="{size:.2f}" height="{size:.2f}" rx="{size / 3:.2f}" fill="{t["accent"]}" fill-opacity="{opacity:.2f}"/>
      <animateMotion dur="{loop:.2f}s" begin="{i * lag:.3f}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;1;1" keyTimes="0;{(loop - 2.4) / loop:.4f};1"><mpath href="#route"/></animateMotion>
      <set attributeName="opacity" to="1" begin="{i * lag:.3f}s"/>
    </g>''')
    head = f'''<g>
      <circle r="13" fill="{t["glow"]}" opacity="0.28" filter="url(#blur)"/>
      <rect x="-8.5" y="-8.5" width="17" height="17" rx="6" fill="{t["accent"]}"/>
      <circle cx="3.6" cy="-3.4" r="1.9" fill="{t["panel"]}"/>
      <circle cx="3.6" cy="3.4" r="1.9" fill="{t["panel"]}"/>
      <animateMotion dur="{loop:.2f}s" repeatCount="indefinite" rotate="auto" calcMode="linear" keyPoints="0;1;1" keyTimes="0;{(loop - 2.4) / loop:.4f};1"><mpath href="#route"/></animateMotion>
    </g>'''

    def stat(x: int, value: str, label: str) -> str:
        return (f'<text x="{x}" y="92" font-family="{SANS}" font-size="26" font-weight="700" fill="{t["text"]}">{value}</text>'
                f'<text x="{x}" y="114" font-family="{MONO}" font-size="12" fill="{t["faint"]}">{label}</text>')
    busy = f'{busiest["count"]} on {busiest["date"]:%b %d}' if busiest and busiest["count"] else "none yet"
    legend_x = width - 40 - 5 * STEP
    legend = "".join(f'<rect x="{legend_x + i * STEP}" y="{GY + 7 * STEP + 12}" width="{CELL}" height="{CELL}" rx="4" fill="{c}"/>'
                     for i, c in enumerate(t["levels"]))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img"
  aria-label="{total} contributions in the last year, across {active} active days.">
  <defs>
    <filter id="blur" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="4"/></filter>
    <clipPath id="grid"><rect x="{GX - 4}" y="{GY - 4}" width="{grid_w + 8}" height="{7 * STEP + 4}"/></clipPath>
    <path id="route" d="{path}"/>
  </defs>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="18" fill="{t["panel"]}" stroke="{t["line"]}"/>
  <text x="32" y="46" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="1.2" fill="{t["faint"]}">CONTRIBUTIONS · LAST 12 MONTHS</text>
  <text x="30" y="104" font-family="{SANS}" font-size="52" font-weight="700" letter-spacing="-1.5" fill="{t["accent"]}">{total:,}</text>
  <text x="{40 + len(f"{total:,}") * 30}" y="102" font-family="{SANS}" font-size="18" fill="{t["muted"]}">contributions, one commit at a time</text>
  {stat(width - 320, f"{best_week}", "in my best week")}
  {stat(width - 170, busy, "busiest day")}
  <g font-family="{MONO}" font-size="12">{"".join(months)}{weekdays}</g>
  <g>{"".join(cells)}</g>
  <g clip-path="url(#grid)">
    {"".join(body)}
    {head}
  </g>
  <g font-family="{MONO}" font-size="12" fill="{t["faint"]}">
    <text x="{legend_x - 10}" y="{GY + 7 * STEP + 24}" text-anchor="end">less</text>
    {legend}
    <text x="{legend_x + 5 * STEP + 6}" y="{GY + 7 * STEP + 24}">more</text>
  </g>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--out", default="dist")
    args = parser.parse_args()
    days, total = fetch(args.user)
    layout(days)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        (out / f"contributions-{name}.svg").write_text(card(days, total, theme), encoding="utf-8")
    print(f"{total} contributions, {len(days)} days -> {out}")


if __name__ == "__main__":
    main()
