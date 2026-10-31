"""membrane-skeleton v0.1.0 — a sparkainlp-x membrane on a skeleton.

Stdlib-only Python, seeded, reproducible, AGPL-3.0-only.

Lineage, reused exactly
-----------------------
1. membrane-capacity: complex oscillators; patterns stored as an
   outer-product holographic memory; recognition is one-shot
   projection — winner = argmax |overlap|, probs = |m|^2 / sum |m|^2.
2. refusing-membrane: REJECT iff max |overlap| < tau, tau calibrated
   once and frozen — with the midpoint-of-max-J improvement from
   membrane-vs-hopfield.
3. membrane-heart + membrane-brain: a pattern is an ENVELOPED phasor
   wave over a graph, not a pure phase wave. Pure phase snapshots
   differ only by a global phase, which |overlap| cannot see
   (membrane-heart first run: recognition 0.325). The envelope —
   amplitude decays with Dijkstra distance from the seed, phase
   advances with distance — is kept here from the start.

The toy skeleton
----------------
31 named bone nodes in a standing figure (skull, jaw, spine chain,
ribs, clavicles, scapulae, arms, pelvis, legs, feet), connected by
hand-defined edges between anatomically adjacent bones. Coordinates
are a flat 2D layout for the graph, not a 3D scan, not a medical
model, and the "25-year-old" label from the earlier holographic
skeleton image is NOT carried into this code: a bone graph has no
age, and nothing here is a measurement of any real person.

Four stored "postures" are wave fields started from four seed bones:
standing (from the skull, top-down), walking (from the left foot),
reaching (from the right hand), crouching (from the pelvis centre).
A probe is projected onto them: the membrane names one, or the
frozen gate refuses it. A random field is refused instead of
mislabelled.

What this is NOT — read before any use
---------------------------------------
Not a human skeleton in any clinical sense. No bone lengths, masses,
joints with degrees of freedom, muscles, or biomechanics. Not a
medical device, not a diagnosis, not a measurement of any real
person. "Holographic" here = outer-product associative memory, the
membrane meaning — not a laser hologram and not a display.
"""

import heapq
import math
import random

__version__ = "0.1.0"


# ---------------------------------------------------------------- helpers
def normalize(v):
    n = math.sqrt(sum(abs(c) ** 2 for c in v))
    if n == 0:
        raise ValueError("cannot normalize a zero vector")
    return [c / n for c in v]


def overlap(field, pattern):
    return sum(p.conjugate() * f for p, f in zip(pattern, field))


def noisy(field, sigma, rng):
    return normalize(
        [c + complex(rng.gauss(0, sigma), rng.gauss(0, sigma))
         for c in field]
    )


def rand_field(n, rng):
    return normalize(
        [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
    )


# ---------------------------------------------------------------- geometry
# (name, x, y) — flat 2D standing layout, y up, feet at y = 2.
NODE_DEFS = [
    ("skull", 0, 88),
    ("jaw", 0, 82),
    ("neck", 0, 78),
    ("spine-upper", 0, 70),
    ("spine-mid", 0, 58),
    ("spine-lower", 0, 46),
    ("pelvis-centre", 0, 38),
    ("pelvis-left", -6, 38),
    ("pelvis-right", 6, 38),
    ("clavicle-left", -8, 72),
    ("clavicle-right", 8, 72),
    ("scapula-left", -11, 66),
    ("scapula-right", 11, 66),
    ("humerus-left", -14, 58),
    ("humerus-right", 14, 58),
    ("forearm-left", -17, 42),
    ("forearm-right", 17, 42),
    ("hand-left", -18, 30),
    ("hand-right", 18, 30),
    ("rib-left-1", -7, 68),
    ("rib-right-1", 7, 68),
    ("rib-left-2", -9, 60),
    ("rib-right-2", 9, 60),
    ("rib-left-3", -8, 52),
    ("rib-right-3", 8, 52),
    ("femur-left", -6, 26),
    ("femur-right", 6, 26),
    ("shin-left", -6, 12),
    ("shin-right", 6, 12),
    ("foot-left", -6, 2),
    ("foot-right", 6, 2),
]

EDGE_DEFS = [
    # Spine chain.
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
    (6, 7), (6, 8),
    # Shoulders and arms.
    (2, 9), (2, 10), (3, 11), (3, 12),
    (9, 13), (10, 14), (11, 13), (12, 14),
    (13, 15), (14, 16), (15, 17), (16, 18),
    # Rib cage.
    (3, 19), (3, 20), (4, 21), (4, 22), (5, 23), (5, 24),
    (19, 21), (20, 22), (21, 23), (22, 24),
    # Legs.
    (7, 25), (8, 26), (25, 27), (26, 28), (27, 29), (28, 30),
]


class Bone:
    def __init__(self, nid, name, x, y):
        self.id = nid
        self.name = name
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"Bone({self.id}, {self.name!r})"


class SkeletonGeometry:
    """Bone graph + Dijkstra delays."""

    def __init__(self):
        self.bones = [
            Bone(i, name, x, y) for i, (name, x, y) in enumerate(NODE_DEFS)
        ]
        self.n = len(self.bones)
        self.edges = sorted(
            (min(a, b), max(a, b)) for a, b in EDGE_DEFS
        )
        self.by_name = {bone.name: bone.id for bone in self.bones}

    def neighbours(self, nid):
        out = []
        for a, b in self.edges:
            if a == nid:
                out.append(b)
            elif b == nid:
                out.append(a)
        return sorted(out)

    def delays_from(self, source):
        """Dijkstra delays from source; inf if unreachable."""
        by_id = {bone.id: bone for bone in self.bones}
        times = {bone.id: math.inf for bone in self.bones}
        times[source] = 0.0
        heap = [(0.0, source)]
        while heap:
            t, nid = heapq.heappop(heap)
            if t > times[nid]:
                continue
            a = by_id[nid]
            for mid in self.neighbours(nid):
                b = by_id[mid]
                w = math.hypot(a.x - b.x, a.y - b.y)
                if t + w < times[mid]:
                    times[mid] = t + w
                    heapq.heappush(heap, (times[mid], mid))
        return [times[bone.id] for bone in self.bones]


# ---------------------------------------------------------------- membrane
class MembraneSkeleton:
    """Skeleton membrane: store, project, refuse."""

    POSTURE_NAMES = ("standing", "walking", "reaching", "crouching")
    SEED_BONES = ("skull", "foot-left", "hand-right", "pelvis-centre")

    def __init__(self, width=25.0, period=40.0):
        if width <= 0 or period <= 0:
            raise ValueError("width and period must be positive")
        self.geometry = SkeletonGeometry()
        self.n = self.geometry.n
        self.width = width
        self.period = period
        self.seed_ids = [
            self.geometry.by_name[name] for name in self.SEED_BONES
        ]
        self.patterns = [self.wave(sid) for sid in self.seed_ids]
        self.tau = None

    def wave(self, source):
        """Enveloped wave field started from bone `source`."""
        delays = self.geometry.delays_from(source)
        out = []
        for d in delays:
            if math.isinf(d):
                out.append(0j)
                continue
            amp = math.exp(-(d * d) / (2.0 * self.width * self.width))
            phase = 2.0 * math.pi * d / self.period
            out.append(amp * complex(math.cos(phase),
                                     math.sin(phase)))
        return normalize(out)

    def overlaps(self, field):
        return [overlap(field, p) for p in self.patterns]

    def project(self, field):
        ms = self.overlaps(field)
        tot = sum(abs(m) ** 2 for m in ms)
        if tot == 0:
            return None, [0.0] * len(ms)
        probs = [abs(m) ** 2 / tot for m in ms]
        return max(range(len(ms)), key=lambda i: abs(ms[i])), probs

    def max_overlap(self, field):
        return max(abs(m) for m in self.overlaps(field))

    def calibrate(self, in_probes, ood_probes, grid=101):
        """Freeze tau: midpoint of the taus maximising Youden's J."""
        in_max = [self.max_overlap(f) for f in in_probes]
        ood_max = [self.max_overlap(f) for f in ood_probes]
        best_j, best_taus = -2.0, []
        for step in range(grid + 1):
            tau = step / grid
            tpr = sum(1 for v in in_max if v >= tau) / len(in_max)
            fpr = sum(1 for v in ood_max if v >= tau) / len(ood_max)
            j = tpr - fpr
            if j > best_j + 1e-12:
                best_j, best_taus = j, [tau]
            elif abs(j - best_j) <= 1e-12:
                best_taus.append(tau)
        self.tau = (best_taus[0] + best_taus[-1]) / 2.0
        return self.tau, best_j

    def decide(self, field):
        """('accept', posture_name, probs) or ('reject', None, probs)."""
        winner, probs = self.project(field)
        if winner is None:
            return "reject", None, probs
        if self.tau is not None and self.max_overlap(field) < self.tau:
            return "reject", None, probs
        return "accept", self.POSTURE_NAMES[winner], probs
