# Regulated Effective Theories (EFT Ladder) under MDEA-HPF

## Purpose
This appendix specifies how effective theories at different scales are regulated, weighted, and transitioned under HPF legality constraints and MDEA soft authority assignment.

EFTs are treated as scale-local execution experts, not approximations that may be extrapolated arbitrarily.

---

## General Rule (Applies to All EFTs)

An effective theory $E_L$ at scale $L$ is schedulable iff:
- Its degrees of freedom are resolved at the active resolution
- Refinement does not reveal instability migration
- Predictions do not require invented precision
- No HPF hard gate is violated

EFTs are expected to lose authority as resolution increases.

---

## Global Hard Gates (HPF)

All EFT execution is immediately blocked or overridden if:
- $\sigma_{\max} > 1$ → **UHET** (saturation / throttling)
- $G_{\text{health}} < G_{\text{crit}} = 0.3$ → **QPRCA** (metric execution forbidden)

EFTs have no exemption from these gates.

---

## Authority Model (Scale-Aware)

For an EFT defined at scale $L$:

$v_{\text{EFT}}(L) = f_{\text{resolution}}(L)\cdot f_{\text{closure}}(L)\cdot f_{\text{stability}}(L)\cdot U_{\text{health}} \qquad v_{\text{EFT}}\in[0,1]$

Where:
- $f_{\text{resolution}}$: EFT degrees of freedom are resolved but not over-resolved
- $f_{\text{closure}}$: higher-order operators remain suppressed
- $f_{\text{stability}}$: no instability migration under refinement
- $U_{\text{health}}$: unitarity health

---

## Ladder Structure (Canonical)

### 1. Classical Effective Theories
Examples: Newtonian mechanics, hydrodynamics  
Status: ✅ Executable at coarse resolution

Failure mode: breakdown under relativistic or quantum refinement

Routing: smooth handoff to higher EFT

---

### 2. Quantum Effective Field Theories
Examples: Low-energy QFT, condensed-matter EFTs  
Status: ✅ Executable within cutoff

Failure mode: operator proliferation, strong coupling

Routing: authority decays as cutoff approached

---

### 3. Semiclassical Gravity (EFT)
Role: Bridge between quantum matter and classical geometry  
Status: ✅ Conditionally executable

Failure mode: non-perturbative backreaction, geometry degradation

Routing: override to UHET or QPRCA when hard gates trigger

---

### 4. UV-Sensitive EFTs
Examples: Near-cutoff theories, trans-Planckian extrapolations  
Status: ⚠️ Weakly executable (low authority)

Failure mode: invented precision, loss of closure

Routing: HPF enforces early handoff; never dominant

---

## Execution Prohibitions (Critical)

Under HPF, EFTs cannot:
- be extrapolated beyond their cutoff
- accumulate authority by refinement
- mask saturation or geometry failure
- override higher-resolution legality signals

Authority must decrease, not increase, as assumptions fail.

---

## Routing Summary

EFT Level | Executable | Authority Trend | Failure Trigger
---|---|---|---
Classical | Yes | Decreases under refinement | Relativistic / quantum effects
Quantum EFT | Yes | Decreases near cutoff | Strong coupling
Semiclassical Gravity | Yes | Decays near regime failure | Backreaction / geometry
UV-Sensitive EFT | Marginal | Near zero | Invented precision

---

## Appendix Verdict

HPF enforces a monotonic authority ladder:
- Coarser EFTs dominate at coarse resolution
- Finer EFTs take over only when justified
- No EFT gains authority by extrapolation
- All EFTs yield cleanly to UHET/QPRCA at hard limits
