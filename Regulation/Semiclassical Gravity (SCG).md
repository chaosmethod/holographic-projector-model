# Semiclassical Gravity (SCG) — HPF Routing Entry

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

- **Refinement behavior**  
  Backreaction remains perturbative.  
  No runaway branching or instability migration.  
  If violated → **HPF engagement / rerouting**

Outside this window, semiclassical gravity is non-executable.

---

## Soft authority score (not truth)

$v_{\text{SCG}} = f_{\text{geom}} \cdot f_{\text{backreaction}} \cdot f_{\text{QFTbg}} \cdot U_{\text{health}}$

---

## Factors

### Geometric validity — $f_{\text{geom}}$
Spacetime geometry remains meaningful and trackable.  
$G_{\text{health}}$ remains high.

### Backreaction control — $f_{\text{backreaction}}$
Quantum backreaction remains perturbative and non-chaotic.

### QFT-on-background validity — $f_{\text{QFTbg}}$
Background spacetime varies slowly relative to quantum field dynamics.

### Unitarity health — $U_{\text{health}}$
Tracked by MDEA-HPF.

---

## Domain of dominance

Semiclassical gravity can dominate when:
- No boundary dual is available
- Collapse and evaporation are locally semiclassical
- Strong-coupling or holographic structure is not required

---

## Domain of failure

Semiclassical gravity becomes non-executable when:
- Geometry degrades below $G_{\text{health}} = 0.3$
- Backreaction becomes nonperturbative or branching-dominated
- State dependence overwhelms effective description

---

## Termination

If legality gates fail, evaluation halts.

Semiclassical gravity is neither accepted nor rejected — execution ends.
