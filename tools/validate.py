"""Validate every sections/v1/*.json against schema.json (stdlib + jsonschema)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    import jsonschema

    schema = json.loads((ROOT / "schema.json").read_text())
    files = sorted((ROOT / "sections" / "v1").glob("*.json"))
    if not files:
        print("no section files yet (M1 scaffold) — schema itself parses, ok")
        jsonschema.Draft7Validator.check_schema(schema)
        return 0
    ok = True
    for path in files:
        try:
            data = json.loads(path.read_text())
            jsonschema.validate(data, schema)
            print(f"ok: {path.name}")
        except Exception as exc:  # noqa: BLE001 — report and keep going
            ok = False
            print(f"FAIL: {path.name}: {exc}")
    # M2 adds: re-derive outlines from dims, diff reference-vectors.json.
    return 0 if ok else 1


if __name__ == "__main__":
    main()
