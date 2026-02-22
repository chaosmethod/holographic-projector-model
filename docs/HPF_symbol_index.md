# HPF–MDEA Unified Symbol & Definition Index

**Status:** Canonical Reference  
**Scope:** Definitions only (no derivations, no narrative)  
**Purpose:** Eliminate ambiguity across HPF, MDEA, UHET, and QPRCA

---

## 1. Framework Layer Map

This stack is **layered, not competitive**:

- **HPF (Holographic Projection Framework)** — legality, regime detection, and execution constraints
- **MDEA (Multi‑Domain Execution Architecture)** — orchestration and routing among domain experts
- **UHET (Unified Holographic Emergence Theory)** — phenomenological description of saturation‑regulated regimes
- **QPRCA (Quantum Partitioned Reversible Cellular Automaton)** — executable substrate candidate

No layer replaces or subsumes another.

---

## 2. Core Symbols (Global)

| Symbol | Name | Layer | Definition | Notes |
|------|------|-------|------------|-------|
| $x$ | Lattice site / region | Global | Localized execution region | Abstract index |
| $t_{sched}$ | Scheduler time | QPRCA | Absolute substrate update clock | Uniform |
| $\tau$ | Proper time | Emergent | Observable time from coherent updates | Branch‑dependent |

---

## 3. HPF — Regulation & Legality Symbols

| Symbol | Name | Definition | Valid Range | Notes |
|------|------|------------|-------------|-------|
| $b(x)$ | Badness field | Local measure of instability | $\ge 0$ | Domain‑agnostic |
| $B$ | Total badness | $\sum_x b(x)$ | $\ge 0$ | Refinement tracked |
| $\sigma(x)$ | Saturation pressure | Update demand / capacity | $[0, \infty)$ | Hard gate at $>1$ |
| $\sigma_{\max}$ | Max saturation | $\max_x \sigma(x)$ | $[0, \infty)$ | Routing trigger |
| $\sigma_*$ | Activation threshold | Persistent saturation trigger | $0.7$ (default) | HPF engage |
| $G_{health}$ | Geometry health | Metric viability score | $[0,1]$ | Revoked $<0.3$ |
| $G_{crit}$ | Geometry cutoff | Metric failure threshold | $0.3$ | Hard revoke |
| $U_{health}$ | Unitarity health | Probability conservation | $[0,1]$ | Diagnostic |
| $\tau_C$ | Convergence threshold | Refinement convergence ratio | $0.5$ | Default |
| $\tau_P$ | Persistence threshold | Instability persistence ratio | $0.8$ | Default |

---

## 4. MDEA — Execution & Routing Symbols

| Symbol | Name | Definition | Notes |
|------|------|------------|-------|
| $E_i$ | Domain expert | Theory + solver valid in a regime | GR, QFT, etc. |
| $V_i$ | Validity score | Fitness of $E_i$ for current state | Computed |
| $E^*$ | Selected expert | $\arg\max_i V_i$ | Soft selection |
| $S_{handoff}$ | Handoff state | Minimal exported state | No invented precision |

---

## 5. UHET — Saturation & Phenomenology Symbols

| Symbol | Name | Definition | Notes |
|------|------|------------|-------|
| $S_f$ | Entropic flux | External turbulence / load | Phase driver |
| $u(r)$ | Utilization | $R_s / r$ | Dimensionless |
| $\alpha(x)$ | Update availability | Fraction of coherent updates | Not a metric |
| $R_s$ | Saturation radius | Utilization $=1$ surface | Horizon‑like |
| $\gamma_{HPF}$ | Time dilation | $dt_{sched}/d\tau$ | Matches GR |

---

## 6. QPRCA — Substrate Symbols

| Symbol | Name | Definition | Notes |
|------|------|------------|-------|
| $\alpha(x)$ | Regulator field | Local coherent update availability | Quantum DOF |
| $L_{tot}(x)$ | Total load | Sum of channel activities | Universal coupling |
| $L_a(x)$ | Channel load | Activity from channel $a$ | Weighted |
| $w_a$ | Channel weight | Fixed coupling weight | Non‑geometric |

---

## 7. Phase Boundaries (Reference)

| Quantity | Boundary | Interpretation |
|---------|----------|----------------|
| $S_f < 1.4$ | Einstein phase | Laminar geometry |
| $1.4 < S_f < 5.79$ | Quantum phase | Turbulent geometry |
| $S_f > 5.79$ | Decoherence | Raw geometry collapse |
| $\sigma_{\max} \ge 1$ | Illegal | Route to UHET |
| $G_{health} < 0.3$ | Metric failure | Route to QPRCA |

---

This index defines symbols only. All derivations live in their respective documents.

---

**End of Canonical Index**

