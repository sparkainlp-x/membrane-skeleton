"""Demo for membrane-skeleton v0.1.0. Run: python demo.py"""

import random

from skeleton import MembraneSkeleton, noisy, rand_field


def main():
    skel = MembraneSkeleton()
    geo = skel.geometry
    print(f"membrane-skeleton v0.1.0 — {geo.n} bones, "
          f"{len(geo.edges)} edges")
    delays = geo.delays_from(geo.by_name["skull"])
    print(f"skull to left foot: "
          f"{delays[geo.by_name['foot-left']]:.2f} distance units")

    rng = random.Random(11)
    in_probes = [noisy(skel.patterns[k % 4], 0.15, rng)
                 for k in range(100)]
    ood_probes = [rand_field(31, rng) for _ in range(100)]
    tau, j = skel.calibrate(in_probes, ood_probes)
    print(f"gate calibrated: tau = {tau:.3f}, Youden J = {j:.3f} (frozen)")

    rng2 = random.Random(99)
    ok = sum(
        1 for k in range(40)
        if skel.decide(noisy(skel.patterns[k % 4], 0.15,
                             rng2))[1] == skel.POSTURE_NAMES[k % 4])
    print(f"fresh noisy recognition (sigma=0.15): {ok}/40")
    rej = sum(
        1 for _ in range(50)
        if skel.decide(rand_field(31, rng2))[0] == "reject")
    print(f"fresh random fields refused: {rej}/50")
    clean = skel.decide(skel.patterns[1])
    print(f"clean walking probe -> {clean[0]}: {clean[1]}")


if __name__ == "__main__":
    main()
