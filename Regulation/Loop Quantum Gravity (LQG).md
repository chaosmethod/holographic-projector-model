# Loop Quantum Gravity (LQG) — HPF Routing Entry

## Status
Conditionally executable under HPF legality constraints.

---

## Hard legality gates (must pass first)

- **Resolution saturation**  
  $\sigma_{\max} < 1$  
  If violated → **UHET override**

- **Geometric health**  
  $G_{\text{health}} \ge 0.3$  
  If violated → **QPRCA override**

- **Executable update rule exists**  
  A finite, schedulable update law on the LQG state representation (spin networks / spin foams or equivalent).

- **Operational observables defined**  
  Regime-local, computable observables with explicit measurement protocol.

- **Explicit exit / handoff condition**  
  Defined signal for breakdown and transfer to semiclassical gravity, EFT ladder, or non-metric routing.

Failure of any condition renders execution illegal.

---

## Soft authority score (not truth)

$v_{\text{LQG}} = f_{\text{resolution}} \cdot f_{\text{dynamics}} \cdot f_{\text{observables}} \cdot f_{\text{semiclassical}} \cdot U_{\text{health}}$

---

## Factors

### Resolution legality — $f_{\text{resolution}}$
Discrete kinematics are admissible only if effective degrees of freedom are explicitly bounded and schedulable.

### Dynamics coherence — $f_{\text{dynamics}}$
Authority depends on a closed, stable update implementation that does not rely on refinement-to-continuum as physics.

### Observable anchoring — $f_{\text{observables}}$
Formal spectra alone do not grant authority; measurable, operational quantities are required.

### Semiclassical recoverability — $f_{\text{semiclassical}}$
A controlled route to classical GR (and QFT on curved spacetime where applicable) must exist without invented precision.

### Unitarity health — $U_{\text{health}}$
Tracked by MDEA-HPF.

---

## Domain of dominance

LQG can dominate when:
- $\sigma$ remains sub-saturated
- $G_{\text{health}} \approx 1$
- Update rules remain stable under refinement
- Relational observables are well-conditioned

---

## Domain of failure

LQG becomes non-executable when:
- Dynamics are formal but not executable
- Predictions rely on uncontrolled continuum limits
- Observables are missing or only asymptotic
- Semiclassical recovery requires invented precision

---

## Termination

If legality gates fail, evaluation halts.

LQG is neither accepted nor rejected — execution ends.
