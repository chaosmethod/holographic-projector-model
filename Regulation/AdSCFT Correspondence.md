# AdS/CFT Correspondence — HPF Routing Entry

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
  Convergent under refinement.  
  No instability migration.  
  If violated → **HPF engagement / rerouting**

Outside this window, AdS/CFT is non-executable.

---

## Soft authority score (not truth)

$v_{\text{AdS/CFT}} = f_{\text{boundary}} \cdot f_{\text{recon}} \cdot f_{\text{res}} \cdot U_{\text{health}}$

---

## Factors

### Boundary stability — $f_{\text{boundary}}$
Boundary observables remain stable under refinement.

### Bulk reconstruction — $f_{\text{recon}}$
Bulk claims do not require invented precision beyond boundary resolution.

### Resolution consistency — $f_{\text{res}}$
No reliance on infinite- $N$ or continuum extrapolation as physical input.

### Unitarity health — $U_{\text{health}}$
Tracked by MDEA-HPF.

---

## Domain of dominance

AdS/CFT can dominate when:
- Asymptotically AdS geometry is well-defined
- Boundary observables provide the primary operational anchor
- Bulk claims remain resolution-legal

---

## Domain of failure

AdS/CFT becomes non-executable when:
- No stable boundary observable set exists
- Bulk reconstruction demands precision beyond HPF capacity
- Claims migrate instability under refinement

---

## Termination

If legality gates fail, evaluation halts.

AdS/CFT is neither accepted nor rejected — execution ends.
