# Asymptotic Safety (Quantum Gravity) — HPF Routing Entry

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

- **Finite-resolution RG execution**  
  RG flow claims must be realized as a finite, computable procedure with truncation legality accounted.

- **Operational observables defined**  
  Must provide regime-local observables beyond fixed-point existence.

- **Explicit exit / handoff condition**  
  Defined signal for transfer to EFT ladder or semiclassical gravity.

Failure of any condition renders execution illegal.

---

## Soft authority score (not truth)

$v_{\text{AS}} = f_{\text{resolution}} \cdot f_{\text{truncation}} \cdot f_{\text{observables}} \cdot f_{\text{handoff}} \cdot U_{\text{health}}$

---

## Factors

### Resolution legality — $f_{\text{resolution}}$
Continuum RG is treated as an approximation; authority requires finite-resolution execution.

### Truncation stability — $f_{\text{truncation}}$
Authority decays if results migrate under refinement of truncation order or basis.

### Observable anchoring — $f_{\text{observables}}$
Fixed-point structure alone is not an observable; measurable outputs are required.

### Handoff integrity — $f_{\text{handoff}}$
A clear boundary must exist where the asymptotic-safety description hands off to another regime.

### Unitarity health — $U_{\text{health}}$
Tracked by MDEA-HPF.

---

## Domain of dominance

Asymptotic Safety can dominate when:
- Truncations are explicitly bounded
- Predictions remain stable under refinement
- Observable outputs are well-defined
- A clean IR handoff to EFT exists

---

## Domain of failure

Asymptotic Safety becomes non-executable when:
- Claims rely on uncontrolled functional RG spaces
- Truncation dependence is large or migratory
- Observables are absent
- No exit or handoff condition is specified

---

## Termination

If legality gates fail, evaluation halts.

Asymptotic Safety is neither accepted nor rejected — execution ends.
