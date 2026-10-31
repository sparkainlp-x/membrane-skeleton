# membrane-skeleton v0.1.0

**A sparkainlp-x membrane on a skeleton — a toy graph, not a body.**

Stdlib-only Python, seeded, reproducible, AGPL-3.0-only.

## Lineage reused

- **membrane-capacity**: complex oscillators, outer-product
  holographic memory, one-shot projection (argmax |overlap|).
- **refusing-membrane**: REJECT iff max |overlap| < tau, tau
  calibrated once via Youden's J and frozen, with the
  midpoint-of-best-taus improvement from membrane-vs-hopfield.
- **membrane-heart / membrane-brain**: patterns as ENVELOPED
  phasor waves over a graph (amplitude decays with Dijkstra
  distance from the seed, phase advances with distance). Pure
  phase waves were falsified in membrane-heart and are not
  repeated here.

## Run

```bash
python demo.py    # numbers + gate + recognition
python tests.py   # 7 tests
```

## The toy, in one paragraph

31 named bone nodes in a standing 2D layout, connected by
hand-defined edges between adjacent bones. Four stored "postures"
are wave fields started from four seed bones: standing (skull),
walking (left foot), reaching (right hand), crouching (pelvis
centre). A probe is projected onto them: the membrane names one,
or the frozen gate refuses it. A random field is refused instead
of mislabelled.

## Measured (demo)

- 31 bones, 36 edges; skull to left foot: 92.00 distance units
- Gate calibrated: tau = 0.455, Youden J = 1.000 (frozen)
- Fresh noisy recognition (sigma = 0.15): 39/40
- Fresh random fields refused: 50/50
- Clean walking probe: accept, walking

## Honest limits — read before any use

- **Not a human skeleton in any clinical sense.** No bone lengths,
  masses, joints with degrees of freedom, muscles, or biomechanics.
- **No age.** The earlier holographic skeleton image was labelled
  25 years old; this bone graph has no age, and nothing here is a
  measurement of any real person.
- **Not a medical device, not a diagnosis.** Posture names are
  labels for wave snapshots, not observed movements.
- "Holographic" here = outer-product associative memory, the
  membrane meaning — not a laser hologram and not a display.
- Coordinates are a flat 2D layout, not a 3D scan. Delays are in
  layout distance units, not milliseconds or centimetres.

## Files

- `skeleton.py` — bone graph, wave, membrane, gate
- `demo.py` — measured demo
- `tests.py` — 7 tests
- `DESIGN.md` — decisions, falsified designs, limits
- `LICENSE` — AGPL-3.0-only

## Credits

Authors: Jean-François Brisson and Mun Seok Lee.
Lee, author of the Digital to Wave paradigm (Zenodo 21947036,
21947108), is the inspiration friend behind this wave and
membrane work. This package's code was built by Brisson with
AI assistance, except where a file already credits Lee as
author; the joint credit here is for the shared programme,
not a claim that Lee wrote every line of this package.
