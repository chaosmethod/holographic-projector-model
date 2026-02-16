# HPF Modules

**Executable + theoretical components of the Holographic Projection Framework (HPF)**  
organized as a **conditional stack**:


- **HPF** — regulation & applicability (when emergence is required)
- **UHET** — entropy, saturation, and breakdown limits
- **QPRCA** — reversible microscopic update rules

> **Engagement rule:**  
> HPF is active *only* when increasing resolution fails to eliminate irreversibility  
> (i.e. instability migrates rather than disappears).

---

## What’s in this folder

### ▶️ Executable simulations

**`HPF_2D_Gauge-Metric_Walk.py`**  
2D regulated quantum walk demonstrating HPF in action.  
Gauge fields + reversible QPRCA dynamics + local regulator **α** produce emergent
time dilation, redshift-like behavior, and horizon formation via update throttling.

*Layer:* `HPF + QPRCA`

---

### 🧠 Regulation & interpretation

**`HPF_Evolutionary_Regulator.py`**  
Adaptive regulator logic governing **α(x)**.  
Encodes congestion, saturation, healing, and bounded update capacity — without
assuming geometry or stress–energy tensors.

*Layer:* `HPF`

---

**`HPF_Gravity_Metric.md`**  
Explains when **α(x)** may be interpreted as an *effective metric* after
coarse-graining, and where that interpretation fails.  
Geometry is emergent, approximate, and invalid at lattice scale.

*Layer:* `Semiclassical interpretation`

---

### ⚙️ Reversible microdynamics (QPRCA)

**`QPRCA_Block-Gate_Reference.py`**  
Reference notes and implementations for reversible, block-partitioned update rules.
Defines the microscopic “gate grammar” used by QPRCA substrates.

*Layer:* `QPRCA`

---

**`qprca_block_gate_1d.py`**  
Minimal 1D QPRCA example.  
Useful for testing reversibility and locality in isolation, without HPF regulation.

*Layer:* `QPRCA (minimal)`

---

### 🧱 Limits & integration

**`UHET.md`**  
Ultra-High-Entropy Theory (UHET): entropy bounds, saturation limits, and failure of
geometric descriptions in finite-resolution systems.  
Explains why horizons and projection are unavoidable.

*Layer:* `UHET`

---

**`UHET_HPF_QPRCA.md`**  
Glue document describing how **UHET**, **HPF**, and **QPRCA** fit together.
Clarifies roles, boundaries, and non-overlap across the stack.

*Layer:* `Stack integration`

---

## TL;DR

- **QPRCA** defines *how* states update  
- **UHET** defines *where* limits appear  
- **HPF** decides *when* regulation is required — and when it should remain inactive
