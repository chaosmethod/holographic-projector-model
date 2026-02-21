# Consistency Check — AdS/CFT vs Semiclassical Gravity

## Purpose
Verify that HPF arbitration between experts is internally consistent, non-biased, and terminates cleanly when legality ends.

This check compares **soft authority**, not truth.

---

## Preconditions

Comparison is only meaningful if **both experts** satisfy:

- Resolution saturation  
  $\sigma_{\max} < 1$

- Geometric health  
  $G_{\text{health}} \ge 0.3$

If either condition fails, HPF overrides engage and comparison terminates.

---

## Comparison rule

Soft authority scores are compared:

$v_{\text{AdS/CFT}} \stackrel{?}{>} v_{\text{SCG}}$

Both experts share the factor $U_{\text{health}}$.  
Differences arise from remaining validity factors.

---

## Case A — Asymptotically AdS with stable boundary observables

Signals:
- $\sigma_{\max} \ll 1$
- $G_{\text{health}} \approx 1$
- Boundary observables stable under refinement

Consequences:
- $f_{\text{boundary}} \approx 1$
- $f_{\text{recon}}$ remains high if bulk claims stay resolution-legal

SCG authority may be limited if strong-coupling structure or holographic encoding is required beyond effective control.

**Outcome:**  
AdS/CFT can dominate in its natural regime.

---

## Case B — Asymptotically flat collapse / evaporation

Signals:
- No stable boundary observable set
- Dynamics dominated by local semiclassical evolution

Consequences:
- $f_{\text{boundary}} \to 0$
- $v_{\text{AdS/CFT}} \approx 0$

SCG retains authority while legality holds.

**Outcome:**  
Semiclassical gravity dominates.

---

## Case C — Approaching regime failure

As either condition approaches violation:

- $\sigma_{\max} \to 1$
- $G_{\text{health}} \to 0.3$

Overrides engage:
- $\sigma_{\max} > 1$ → **UHET**
- $G_{\text{health}} < 0.3$ → **QPRCA**

**Outcome:**  
No expert dominates. Execution terminates.

---

## Verdict

The consistency check passes.

- AdS/CFT is permitted where boundary anchoring is operational.
- Semiclassical gravity dominates where no boundary dual exists.
- Both are superseded when legality constraints fail.

HPF enforces **execution limits**, not theoretical preference.
