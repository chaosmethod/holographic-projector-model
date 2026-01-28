
# Holographic Projector Framework (HPF) – Lu Calibration (2026)

## Executive Summary

Recent experiments by **Chao-Yang Lu et al. (USTC, 2026)** revealed an intermediate quantum regime in which wave–particle duality manifests as a **finite “blur”**, rather than a sharp dichotomy. This establishes an empirical resolution limit in phase space and identifies a transition between localized and delocalized behavior.

The **Holographic Projector Framework (HPF)** does **not** derive or predict the Lu experiment. Instead, HPF **uses the Lu equilibrium as an empirical calibration point** to construct a **resolution-limited stability function** that reproduces the observed transition across scales. HPF provides a **mechanistic interpretation**: finite information capacity naturally produces intermediate stability regimes.

---

## Core Axiom (HPF)

> **Stability ((\zeta)) decreases as Information Satiation ((S_f)) approaches the resolution limit of the projection grid.**

This axiom formalizes the concept that **localization is conditional**, not absolute, when information density approaches system capacity.

---

## The Unified Stability Equation

[
\zeta(S_f) = \frac{1}{1 + e^{k(S_f - \lambda)}}
]

Where:

* **(S_f)** (*Flux Satiation*): Dimensionless measure of information pressure ((\Delta p \cdot \Delta x)) normalized by the finite resolution scale.

* **(\zeta)** (*Zeta Stability*): Probability that a state remains localized under finite resolution.

* **(\lambda)** (*Lu Threshold*): Empirically observed equilibrium point ((\lambda \approx 1.05)) marking the onset of the intermediate “blur” regime.

* **(k)** (*Rendering Slope*): Controls the sharpness of the transition; models observer-smearing and coarse-graining.

> **Why logistic?**
> The logistic function is physically motivated: it arises naturally when independent thresholded microstates are coarse-grained under finite information flux. It smoothly interpolates between stable (matter-like) and unstable (blur/metadata) states. Alternative smooth monotone functions (e.g., tanh, arctan) produce qualitatively similar transitions, but the logistic is chosen for simplicity and analytic convenience.

---

## Experimental Calibration Matrix

| Scale    | Scenario       | (\zeta) | Resultant Regime      |
| -------- | -------------- | ------- | --------------------- |
| Micro    | Lu Atom (2026) | 0.5000  | Intermediate Blur     |
| Standard | Stable Fermion | 0.9948  | Matter-Like Stability |
| Macro†   | Sgr A* Horizon | ~0.0000 | Saturation-Dominated  |

† Macroscopic values are extrapolated informational regimes, not direct measurements of fermionic stability.

---

## Interpretation

* The **Lu experiment establishes** the intermediate regime.
* **HPF reproduces this structure** using a single dimensionless information-satiation parameter.
* Wave- and particle-like behavior emerge as **regime descriptions**, not ontological absolutes.
* HPF provides an **informational interpretation** of operational ambiguity highlighted by the historical Einstein–Bohr debate.

---

## Scope and Limits

* HPF is an **effective, empirically calibrated framework**, not a fundamental theory.
* It clarifies **how finite resolution and bounded update capacity produce stability regimes**.
* Extrapolation to large-scale systems (e.g., black holes) is illustrative and must be treated with caution.

---

## Runnable Implementation

A minimal HPF engine is provided in:

```bash
hpf_engine.py
```

Run the engine to reproduce the calibration table above and explore how (\zeta) transitions across scales:

```bash
python hpf_engine.py
```

---

## References

* Einstein & Bohr (1927)
* Lu et al., USTC (2026)
* Event Horizon Telescope Collaboration, Sgr A* (2026)
