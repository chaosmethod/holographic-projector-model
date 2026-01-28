
# Empirical Calibration via the Lu Equilibrium (2026)

## Executive Summary

Recent experiments by **Chao-Yang Lu et al. (USTC, 2026)** demonstrated an intermediate quantum regime in which wave–particle duality manifests as a **finite, irreducible blur**, rather than a sharp dichotomy. This regime establishes an empirical resolution limit in phase space, marking a transition between stable localization and delocalized behavior.

The **Holographic Projector Framework (HPF)** does **not** derive or predict the Lu experiment. Instead, HPF **uses the Lu equilibrium as an empirical calibration point** to construct a resolution-limited stability function that *reproduces and organizes* the observed transition in a unified informational language.

HPF’s contribution is explanatory and structural: it provides a minimal mechanism for **how** such an intermediate regime necessarily arises when finite resolution and bounded information flux are imposed.

---

## The Core Axiom (HPF)

> **Stability ((\zeta)) is inversely proportional to Information Satiation ((S_f)) at the limit of finite grid resolution.**

This axiom does not replace quantum mechanics. It formalizes the idea that **localization is conditional**, not absolute, when information density approaches a system’s rendering or measurement capacity.

---

## The Unified Stability Equation

[
\zeta(S_f) ;=; \frac{1}{1 + e^{k(S_f - \lambda)}}
]

Where:

* **(S_f)** (*Flux Satiation*):
  A dimensionless measure of information pressure in phase space (e.g., (\Delta p \cdot \Delta x)) normalized by a finite resolution scale.

* **(\zeta)** (*Zeta Stability*):
  The probability that a system renders as a stable, localized excitation under finite resolution.

* **(\lambda)** (*Lu Threshold*):
  The empirically observed equilibrium point ((\lambda \approx 1.05)) where localization degrades into an intermediate “blur” regime.

* **(k)** (*Rendering Slope*):
  A phenomenological parameter encoding how sharply the transition is observed under experimental coarse-graining.

The sigmoid form reflects observer-smeared thresholding under finite resolution; it is a phenomenological transition law, not a fundamental dynamical equation.

---

## Experimental Calibration Matrix

| Scale    | Scenario       | (\zeta) | Resultant Regime      |
| -------- | -------------- | ------- | --------------------- |
| Micro    | Lu Atom (2026) | 0.5000  | Intermediate Blur     |
| Standard | Stable Fermion | 0.9948  | Matter-Like Stability |
| Macro†   | Sgr A* Horizon | ~0.0000 | Saturation-Dominated  |

† *Macroscopic values represent extrapolated informational regimes, not direct measurements of fermionic stability.*

---

## Interpretation

* The **Lu experiment establishes** the existence of an intermediate, resolution-limited regime.
* **HPF reproduces this structure** using a single dimensionless information-satiation parameter.
* Wave- and particle-like behavior emerge as **regime descriptions**, not mutually exclusive ontological states.

In this sense, HPF provides an **informational interpretation** of the operational ambiguity highlighted in the historical Einstein–Bohr debate, without making claims of ontological completeness or hidden variables.

---

## Scope and Limits

HPF is an **effective informational framework**:

* It is **calibrated**, not derived, from experiment.
* It does **not** supersede quantum mechanics.
* It is intended to clarify **how finite resolution reshapes stability and localization**, across scales.

---

## Runnable Reference Implementation

A minimal implementation of the HPF stability function is provided in:

```bash
hpf_engine.py
```

Run the engine to reproduce the calibration table above and explore how the Zeta function interpolates between regimes under finite resolution.

```bash
python hpf_engine.py
```

---

## References

* Einstein & Bohr (1927)
* Lu et al., USTC (2026)
* Event Horizon Telescope Collaboration, Sgr A* (2026)

---

### Final note (important for GitHub readers)

HPF should be read as an **interpretive and organizing layer** built on top of experimental results — not as a claim of experimental priority or a fundamental theory of nature.
