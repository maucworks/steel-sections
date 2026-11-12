"""Derive reference outlines from section dims (M2: IPE only).

Coarse: sharp 12-gon, centred, CCW from the lexicographic minimum.
Fine: the same loop with the four root fillets as exact tangent arcs.
Writes reference-vectors.json; --check fails when the committed file
is stale (CI freshness gate, no silent drift).
"""

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def coarse_i(dims):
    """Sharp I-section ring, centred, CCW, closed, minimum corner first."""
    w, d, tw, tf = (dims[k] for k in ("b", "h", "tw", "tf"))
    hw, hh, htw, fy = w / 2, d / 2, tw / 2, d / 2 - tf
    pts = [
        (-hw, -hh), (hw, -hh), (hw, -fy), (htw, -fy), (htw, fy), (hw, fy),
        (hw, hh), (-hw, hh), (-hw, fy), (-htw, fy), (-htw, -fy), (-hw, -fy),
    ]
    pts.append(pts[0])
    first = min(range(len(pts) - 1), key=lambda i: pts[i])
    return pts[first:-1] + pts[:first] + [pts[first]]


def fine_i(dims):
    """Coarse loop with root fillets as exact tangent arcs (segments).

    Walked CCW from the minimum corner; each fillet replaces a sharp
    inner corner by its tangent arc (clockwise, through the void).
    """
    w, d, tw, tf, r = (dims[k] for k in ("b", "h", "tw", "tf", "r"))
    hw, hh, htw, fy = w / 2, d / 2, tw / 2, d / 2 - tf
    segs = []

    def line(a, b):
        segs.append({"line": [[round(a[0], 3), round(a[1], 3)],
                              [round(b[0], 3), round(b[1], 3)]]})

    def arc(c, a1, a2):
        segs.append({"arc": {"c": [round(c[0], 3), round(c[1], 3)],
                             "r": round(r, 3), "a1": a1, "a2": a2,
                             "ccw": False}})

    line((-hw, -hh), (hw, -hh))
    line((hw, -hh), (hw, -fy))
    line((hw, -fy), (htw + r, -fy))
    arc((htw + r, -fy + r), 180.0, 90.0)
    line((htw, -fy + r), (htw, fy - r))
    arc((htw + r, fy - r), 90.0, 0.0)
    line((htw + r, fy), (hw, fy))
    line((hw, fy), (hw, hh))
    line((hw, hh), (-hw, hh))
    line((-hw, hh), (-hw, fy))
    line((-hw, fy), (-htw - r, fy))
    arc((-htw - r, fy - r), 0.0, 270.0)
    line((-htw, fy - r), (-htw, -fy + r))
    arc((-htw - r, -fy + r), 270.0, 180.0)
    line((-htw - r, -fy), (-hw, -fy))
    line((-hw, -fy), (-hw, -hh))
    return segs


def _shoelace(pts):
    n = len(pts) - 1
    return abs(sum(pts[i][0] * pts[i + 1][1] - pts[i + 1][0] * pts[i][1]
                   for i in range(n))) / 2


def build():
    out = {"conventions": "conventions.md",
           "unit": "mm",
           "sections": {}}
    for path in sorted((ROOT / "sections" / "v1").glob("*.json")):
        data = json.loads(path.read_text())
        shape = data.get("shape", "I")
        if shape != "I":
            raise SystemExit(f"{path.name}: shape {shape!r} not supported yet")
        for s in data["sections"]:
            dims, r = s["dims"], s["dims"].get("r", 0.0)
            coarse = [[round(x, 3), round(y, 3)] for x, y in coarse_i(dims)]
            coarse_area = _shoelace(coarse)
            fillet = 4 * r * r * (1 - math.pi / 4)
            entry = {"coarse": coarse,
                     "coarse_area_mm2": round(coarse_area, 3),
                     "fillet_area_mm2": round(fillet, 3),
                     "fine_area_mm2": round(coarse_area + fillet, 3)}
            if r > 0:
                entry["fine"] = fine_i(dims)
            out["sections"][s["designation"]] = entry
    return out


def main() -> int:
    check = "--check" in sys.argv
    text = json.dumps(build(), indent=1) + "\n"
    path = ROOT / "reference-vectors.json"
    if check:
        if not path.exists() or path.read_text() != text:
            print("reference-vectors.json is stale: run tools/derive.py")
            return 1
        print("reference-vectors.json is fresh")
        return 0
    path.write_text(text)
    print(f"wrote {path} ({len(json.loads(text)['sections'])} sections)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
