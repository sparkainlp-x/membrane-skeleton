# DESIGN.md — membrane-skeleton v0.1.0

## Decisions

- **Hand-defined bone graph, not k-NN.** k-NN (used in the heart
  and brain toys) would connect bones that merely sit near each
  other, e.g. a rib to an arm. Hand edges follow adjacency the
  layout intends: spine chain, rib cage, arms, legs. Every node
  has at least one edge and the graph is connected — both tested.
- **31 nodes, not 206.** A full human skeleton has ~206 bones;
  modelling all of them would be anatomy theatre for a membrane
  demo. 31 named groups (spine in 5, ribs in 6, arms, legs) carry
  the structure the four waves need, and no more is claimed.
- **Wave postures, not joint angles.** Joint angles would imply
  biomechanics this toy does not have. A wave from a seed bone
  (skull, foot, hand, pelvis) is a clean, checkable pattern whose
  recognition and refusal can be measured exactly.
- **Envelope from the start.** membrane-heart's pure-phase failure
  (recognition 0.325) is documented in that package and not
  repeated: amplitude decays with distance, phase advances with
  distance, pattern normalised to unit length.
- **Midpoint tau.** Same improvement as membrane-heart and
  membrane-brain: midpoint of the maximal-J taus, so the frozen
  gate is not sitting on a gap edge.
- **No age in the code.** The image that prompted this package was
  labelled 25 years old. A graph of bone names cannot have an age,
  so the code deliberately drops it rather than pretending to
  model a 25-year-old skeleton.

## Falsified / rejected designs

- **k-NN edges.** Rejected: proximity is not adjacency in a
  skeleton layout; hand edges are checkable by reading the list.
- **Full 206-bone model.** Rejected: more nodes, same four waves,
  no new membrane result — and a false impression of anatomical
  completeness.
- **Muscle / movement simulation.** Rejected: no forces, no
  torques, no gait cycle. Posture names are wave-snapshot labels,
  and the README says so.
- **Clinical output (e.g. a fracture or gait score).**
  Rejected: nothing in this toy is measured on a real body, so
  no output is allowed to look diagnostic.

## Limits, restated

Synthetic only. Flat 2D layout, width 25, period 40, delays in
layout distance units — none of these are biological parameters.
The refusal rate is a property of this toy's random fields, not a
sensitivity or specificity for anything real.
