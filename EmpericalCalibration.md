
# HPF Engine – Usage & Purpose

**File:** `HPF_Engine.py`
**Author:** Eric Keaton Porter
**Date:** 2026

---

## Purpose

`HPF_Engine.py` implements the **Holographic Projector Framework (HPF) Stability Function**.

The engine:

1. Applies a **Zeta Stability Function** ((\zeta(S_f))) calibrated against the **Lu 2026 intermediate-resolution experiment**.
2. Demonstrates how **finite information flux** produces three distinct regimes:

   * Stable (matter-like)
   * Intermediate (blur)
   * Saturation-dominated (void / metadata)
3. Provides a **practical, runnable demonstration** of HPF’s interpretive model.

> Note: The engine does **not predict or derive the Lu experiment**. It reproduces the observed structure under finite-resolution constraints.

---

## Core Concept

The stability function is defined as:

[
\zeta(S_f) = \frac{1}{1 + e^{k(S_f - \lambda)}}
]

* (S_f) = information flux / “satiation”
* (\zeta) = probability of a state remaining localized
* (\lambda) = empirically calibrated Lu-equilibrium threshold (~1.05)
* (k) = slope of the transition

> The logistic form is chosen for analytic simplicity and reflects a **generic smooth transition** expected from independent, thresholded microstates. Other monotone functions (tanh, arctan) produce similar qualitative behavior.

---

## How to Run

```bash
python HPF_Engine.py
```

* The script prints a table of stability probabilities ((\zeta)) for example scenarios across **micro**, **standard**, and **macro** scales.
* The macro scale (e.g., Sgr A* horizon) is **illustrative**, not an experimental measurement.

---

## Output Example

| Scale    | Scenario       | ζ     | Regime               |
| -------- | -------------- | ----- | -------------------- |
| Micro    | Lu Atom (2026) | 0.50  | Intermediate Blur    |
| Standard | Stable Fermion | 0.99  | Matter-Like          |
| Macro†   | Sgr A* Horizon | ~0.00 | Saturation-Dominated |

†Extrapolated for illustration only.

---

## Notes

* Designed to run on any Python 3 environment; GPU is optional.
* Parameters are **empirically calibrated** and intended for demonstration; they can be adjusted for testing.
* Falsifiability check: the transition from stable → blur → saturation is smooth and monotone; abrupt or non-monotone behavior at calibrated flux would contradict the model.
