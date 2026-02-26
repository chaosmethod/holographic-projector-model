---

## Update Dynamics (Gate Interpretation)

This engine can be promoted from a stability evaluator to a minimal *dynamical realization* by interpreting the Zeta Stability Function as an **update-acceptance gate**.

### State and local load

Let the system state at step $t$ be a lattice/graph configuration:

- $X_t$: the full configuration (fields, occupancies, phases, etc.)
- $S_f(i,t)$: a local information-flux ratio computed at site/region $i$ over the update neighborhood

A minimal operational definition is:

- $S_f(i,t) = load(i,t) / capacity(i)$

where $load(i,t)$ is a coarse-grained proxy for local update demand (entropy throughput, defect density, field gradients, etc.), and $capacity(i)$ is the local reversible update bandwidth.

### Update proposal (reversible)

At each step, propose a **bijective** local update map on a neighborhood $N(i)$:

- $X'_t = U_i(X_t)$

where $U_i$ is invertible (reversible) by construction.

### Zeta-gated acceptance / rejection

Compute:

$\zeta_i(t) = \zeta(S_f(i,t)) = \frac{1}{1 + e^{k(S_f(i,t) - \lambda)}}$

Then:

- With probability $\zeta_i(t)$, accept the local update: $X_{t+1} = X'_t$
- With probability $1 - \zeta_i(t)$, reject the local update and apply a reversible redistribution rule (below)

### Rejection handling (reversible redistribution)

Rejected updates are not discarded (no information loss). Instead, the update "pressure" is redistributed through a reversible map $R_i$ that preserves global bijectivity:

- $X_{t+1} = R_i(X_t)$

$R_i$ can be implemented as a reversible permutation / swap / phase-scramble across an expanded neighborhood $N*(i)$ such that:

- information is delocalized (blur regime)
- singular localization is prevented (saturation regime)
- global reversibility is maintained (no entropy destruction at the fundamental level)

### Regimes become dynamical phases

Under this gate interpretation, the three HPF regimes correspond to distinct update behavior:

- **Stable (matter-like):** $S_f << λ$ ⇒ $ζ ~ 1$ ⇒ local reversible updates dominate
- **Intermediate (blur):** $S_f ~ λ$ ⇒ $0 < ζ < 1$ ⇒ stochastic acceptance + reversible redistribution
- **Saturation-dominated (core/void):** $S_f >> λ$ ⇒ $ζ → 0$ ⇒ locality fails; delocalized reversible mixing prevents further compression

This defines a minimal dynamical realization: *finite update bandwidth appears as probabilistic acceptance of reversible local updates, with rejected updates redistributed reversibly rather than collapsed into singular states.*

> Note: HPF does not require uniqueness of $U_i$ or $R_i$. This section demonstrates existence of at least one consistent update architecture; alternative reversible update families yield equivalent phase structure under the same zeta gate.
