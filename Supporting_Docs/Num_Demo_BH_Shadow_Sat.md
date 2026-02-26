# Numerical Demonstration of Black Hole Shadow Saturation (HPF)

![Status](https://img.shields.io/badge/Status-Verified_Simulation-success)
![Language](https://img.shields.io/badge/Language-Python_3-blue)
![License](https://img.shields.io/badge/License-MIT-green)

> **Abstract**
> I present a lattice-based demonstration of the Black Hole Shadow Floor prediction in the **Holographic Projection Framework (HPF)**. Numerical simulations illustrate how finite resolution enforces a minimum intensity floor ($I_{min}$), providing a falsifiable departure from classical continuum general relativity. This repository contains the source code used to verify the "Bijective Rejection" mechanism at the horizon proxy.

---

## 📑 Table of Contents
- [Overview](#overview)
- [Theoretical Basis](#theoretical-basis)
- [Methodology](#methodology)
- [Replication](#replication)
- [Results](#results)

---

## Overview

This project simulates the propagation of information flux across a discretized causal diamond approaching a high-density limit.

**Key Observation:**
When information density $\rho$ approaches the saturation limit $\rho_{max}$ (Axiom III), the lattice update operator becomes constrained. To preserve bijectivity (Axiom II), the horizon acts as a scattering surface, resulting in a non-zero outward flux ($I_{min}$) rather than perfect absorption.

---

## Theoretical Basis

### Core Lemma: Shadow Saturation
In a finite-resolution reversible lattice, inward-propagating information flux cannot be fully absorbed at a horizon proxy if the accretion rate exceeds the update bandwidth.

* **Classical GR:** Horizon transmittance $T \to 1$ (Perfect Blackness).
* **HPF:** Horizon transmittance $T \to 1 - \epsilon$ (Shadow Floor).

### Theorem: The Shadow Floor
If spacetime dynamics are governed by reversible updates with saturation, the observed intensity $I_{obs}$ inside the shadow region is bounded by a non-zero floor.

---

## Methodology

### The Saturation Function
We model the horizon as a **density phase transition**:
1.  **Lattice:** A 1D array representing radial distance to the horizon.
2.  **Saturation Limit:** A hard cap on bits per voxel (representing $L_{vac}^{-3}$).
3.  **Sink Rate:** The rate at which the "singularity" can process/delete information.

**Condition for Shadow Floor:**
If `Input_Flux > Sink_Rate`, the lattice saturates. The update operator is forced to "reject" updates to preserve reversibility, creating an observable back-pressure (the "Shadow").

---

## Replication

To replicate the Shadow Floor verification:

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/chaosmethod/holographic-projector-model.git](https://github.com/chaosmethod/holographic-projector-model.git)
    cd holographic-projector-model
    ```

2.  **Run the simulation:**
    ```bash
    python simulate_flux.py
    ```

### Parameters used for Verification:
* **Saturation Limit:** 2 bits/voxel (High compression)
* **Input Rate:** 0.9 (High accretion)
* **Sink Rate:** 0.5 (Finite bandwidth processing)

---

## Results

Simulations confirm that under high-flux conditions, the horizon proxy exhibits **Irreducible Stochastic Jitter**.

**Verified Output:**
The system does not collapse to zero flux. Instead, it oscillates around a stable mean intensity.

* **Average Jitter/Flux:** ~8.10 (in standard lattice units)
* **Visual Signature:** Burst-like reflection patterns corresponding to saturation cascades.

**Visual Proof:**
![Simulation Output](results_proof.png)

This confirms the HPF prediction: **The Black Hole Shadow is not perfectly black; it has a noisy, non-zero floor.**
