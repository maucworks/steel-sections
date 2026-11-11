# Conventions (draft, M1)

How dims become identical outlines in every consumer. Normative for
`reference-vectors.json`; parity tests implement exactly this.

## Frame

- Local X = section width axis, local Y = section depth (height) axis.
- Origin placement, rotation sign and anchor semantics are per-consumer
  concerns (ifckit: anchor + rotation params; CreaBIM: profile frame) —
  but the *canonical* section both start from is defined here:
  **origin at bounding-box centre, unrotated**.

## Loops

- Outer loops counter-clockwise, holes clockwise.
- Start vertex: lexicographically smallest corner `(x, then y)`.
- Closed (first corner repeated at the end).
- Sharp corners in v1: fillet radii recorded as data where known, not
  tessellated (open question O1 in the plan).

## Numbers

- Millimetres in the JSON dims; metres-or-as-documented in outlines is
  per consumer — reference vectors are in **millimetres**.
- Reference vectors rounded to 3 decimals (micrometre).
- Parity tolerance: 1e-9 relative per coordinate.

## I-section canonical form (example)

Overall width `w` (X), overall depth `d` (Y), web `tw`, flange `tf`,
centred at origin:

```text
(-w/2, -d/2), (w/2, -d/2), (w/2, -d/2+tf), (tw/2, -d/2+tf),
(tw/2, d/2-tf), (w/2, d/2-tf), (w/2, d/2), (-w/2, d/2),
(-w/2, d/2-tf), (-tw/2, d/2-tf), (-tw/2, -d/2+tf), (-w/2, -d/2+tf),
close → (-w/2, -d/2)
```

L/U/C/T/Z families get the same treatment as their tables land.
