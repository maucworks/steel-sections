# steel-sections

Open structural steel section data for IFC tooling and beyond: dimensions,
orientation conventions, and machine-checkable reference outlines.

- **Data, no code.** Dims tables any library can read; loaders live in each
  consumer (ifckit, CreaBIM, …).
- **CC0** — use it anywhere, including commercial tools and generated files,
  no attribution required.
- **Versioned** — SemVer tags; consumers pin a release and verify by hash.

Status: scaffold (M1). Section tables land in M2.

## Layout

```text
sections/v1/*.json   dims per designation + source + standard (M2)
conventions.md       orientation/anchor/rotation/winding/corner decisions
reference-vectors.json  canonical corner coords per section: the contract (M2)
schema.json          JSON schema for the section files
```

## Consuming

Vendor a pinned copy, then add one parity test in your library: load the
catalogue, build outlines per `conventions.md`, compare
`reference-vectors.json`. Same input, same output, no shared code.

## Contributing sections

PRs welcome: one family per file, open source recorded per entry, CI
re-derives every outline from dims and diffs the reference vectors.
See `CHANGELOG.md` for versioning (dims fixes = patch, new families =
minor, format/convention changes = major).
