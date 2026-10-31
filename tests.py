"""Tests for membrane-skeleton v0.1.0. Run: python tests.py"""

import math
import random
import unittest

from skeleton import (
    MembraneSkeleton,
    SkeletonGeometry,
    noisy,
    rand_field,
)


class TestMembraneSkeleton(unittest.TestCase):
    def test_geometry_connected_no_isolated(self):
        geo = SkeletonGeometry()
        self.assertEqual(geo.n, 31)
        for bone in geo.bones:
            self.assertGreaterEqual(len(geo.neighbours(bone.id)), 1)
        delays = geo.delays_from(geo.by_name["skull"])
        self.assertTrue(all(math.isfinite(d) for d in delays))
        self.assertGreater(max(delays), 0.0)

    def test_patterns_unit_and_distinct(self):
        skel = MembraneSkeleton()
        self.assertEqual(len(skel.patterns), 4)
        for p in skel.patterns:
            self.assertAlmostEqual(
                math.sqrt(sum(abs(c) ** 2 for c in p)), 1.0, places=9)
        for i in range(4):
            for j in range(i + 1, 4):
                ov = abs(sum(a.conjugate() * b for a, b
                             in zip(skel.patterns[i],
                                    skel.patterns[j])))
                self.assertLess(ov, 0.95)

    def test_clean_posture_recognition(self):
        skel = MembraneSkeleton()
        skel.tau = None
        for i, p in enumerate(skel.patterns):
            verdict, name, _ = skel.decide(p)
            self.assertEqual(verdict, "accept")
            self.assertEqual(name, skel.POSTURE_NAMES[i])

    def test_noisy_recognition(self):
        skel = MembraneSkeleton()
        skel.tau = None
        rng = random.Random(7)
        ok, trials = 0, 40
        for k in range(trials):
            probe = noisy(skel.patterns[k % 4], 0.15, rng)
            _, name, _ = skel.decide(probe)
            ok += name == skel.POSTURE_NAMES[k % 4]
        self.assertGreaterEqual(ok / trials, 0.90)

    def test_gate_refuses_random(self):
        skel = MembraneSkeleton()
        rng = random.Random(11)
        in_probes = [noisy(skel.patterns[k % 4], 0.15, rng)
                     for k in range(100)]
        ood_probes = [rand_field(31, rng) for _ in range(100)]
        tau, j = skel.calibrate(in_probes, ood_probes)
        self.assertGreater(j, 0.90)
        self.assertGreater(tau, 0.2)
        self.assertLess(tau, 0.95)
        rng2 = random.Random(99)
        accepted = sum(
            1 for k in range(50)
            if skel.decide(noisy(skel.patterns[k % 4], 0.15,
                                 rng2))[0] == "accept")
        rejected = sum(
            1 for _ in range(50)
            if skel.decide(rand_field(31, rng2))[0] == "reject")
        self.assertGreaterEqual(accepted / 50, 0.90)
        self.assertGreaterEqual(rejected / 50, 0.90)

    def test_skull_to_foot_spread(self):
        geo = SkeletonGeometry()
        delays = geo.delays_from(geo.by_name["skull"])
        foot = delays[geo.by_name["foot-left"]]
        self.assertTrue(math.isfinite(foot))
        self.assertGreater(foot, 50.0)

    def test_determinism(self):
        a = MembraneSkeleton()
        b = MembraneSkeleton()
        self.assertEqual(a.patterns, b.patterns)
        self.assertEqual(a.geometry.edges, b.geometry.edges)


if __name__ == "__main__":
    unittest.main(verbosity=2)
