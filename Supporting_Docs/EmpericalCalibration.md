
# HPF Engine – Module Description

**File:** `HPF_Engine.py`
**Author:** Eric Keaton Porter
**Date:** 2026

---

## Purpose

`HPF_Engine.py` implements the **Holographic Projection Framework (HPF) Stability Function**.

The engine:

1. Applies the **Zeta Stability Function ($\zeta$)** calibrated against the **Lu 2026 intermediate-resolution experiment**.
2. Demonstrates how **finite information flux ($S_f$)** produces three distinct regimes:

   * Stable (matter-like)
   * Intermediate (blur)
   * Saturation-dominated (void/metadata)
3. Provides a **practical demonstration** of HPF’s interpretive model.

> **Note:** The engine does **not predict or derive the Lu experiment**; it reproduces the observed structure under finite-resolution constraints.

---

## Core Concept

The stability function is defined as:

$$
\zeta(S_f) = \frac{1}{1 + e^{k(S_f - \lambda)}}
$$

Where:

* $S_f$      : Information Flux Ratio (Input Density / Capacity Limit)
* $\zeta$    : Probability of a state remaining localized
* $\lambda$  : Empirically calibrated Lu-equilibrium threshold (~1.05)
* $k$       : Slope of the transition

**Why logistic?**

* Chosen for analytic simplicity
* Reflects a generic smooth transition from independent, thresholded microstates
* Alternative smooth monotone functions (tanh, arctan) produce similar qualitative behavior

---

## How to Use

Run the engine with Python 3:

```bash
python HPF_Engine.py
```

* Prints a table of stability probabilities ($\zeta$) for example scenarios across **micro**, **standard**, and **macro** scales
* Macro-scale (e.g., Sgr A* horizon) is **illustrative**, not an experimental measurement

---

## Example Output

| Scale    | Scenario       | $\zeta$ | Regime               |
| -------- | -------------- | ------- | -------------------- |
| Micro    | Lu Atom (2026) | 0.50    | Intermediate Blur    |
| Standard | Stable Fermion | 0.99    | Matter-Like          |
| Macro†   | Sgr A* Horizon | ~0.00   | Saturation-Dominated |

† Extrapolated for illustration only

---

## Notes

* Runs on any Python 3 environment; GPU optional
* Parameters are **empirically calibrated** and adjustable for testing
* **Falsifiability:** the transition from stable → blur → saturation is smooth and monotone; abrupt or non-monotone behavior at calibrated flux would contradict the model
