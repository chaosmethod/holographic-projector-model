"""
toy_1d_qutip_sim.py
------------------------------------------------------------
Runnable minimal simulation harness for qprca_block_gate_1d.py.

Default:
- N=2 sites
- 1 Dirac qubit per site (|0>=R, |1>=L)
- 1 regulator qubit per site
- optional reservoir qubit per site
- 1 global ancilla A
- runs T ticks and prints:
  - <Z_Ri> for each site
  - P(Di=0) for each site
  - state norm (should remain 1)

This harness is aimed at reproducing the exact kind of debugging you did,
but with a unitary streaming layer (no control/target overlap).
------------------------------------------------------------
"""

from __future__ import annotations
import numpy as np
from qutip import basis, tensor, expect, Qobj
from qutip.qip.operations import gate_expand_1toN

from qprca_block_gate_1d import Layout1D, U_tick

def Z() -> Qobj:
    return Qobj(np.array([[1, 0], [0, -1]], dtype=complex))

def projector_0() -> Qobj:
    v0 = basis(2, 0)
    return v0 * v0.dag()

def expand_1(n_qubits: int, gate1: Qobj, target: int) -> Qobj:
    return gate_expand_1toN(gate1, n_qubits, target)

def build_initial_state(layout: Layout1D,
                        D_bits: list[int],
                        R_bits: list[int],
                        M_bits: list[int] | None = None,
                        A_bit: int = 0) -> Qobj:
    """
    Build |D0,R0,M0, D1,R1,M1, ..., A>
    """
    kets = []
    for i in range(layout.N):
        kets.append(basis(2, D_bits[i]))
        kets.append(basis(2, R_bits[i]))
        if layout.use_reservoir:
            if M_bits is None:
                raise ValueError("Reservoir enabled, but M_bits not provided.")
            kets.append(basis(2, M_bits[i]))
    kets.append(basis(2, A_bit))
    psi0 = tensor(kets)
    return psi0

def run_case(name: str,
             layout: Layout1D,
             D_bits: list[int],
             R_bits: list[int],
             M_bits: list[int] | None,
             params: dict,
             ticks: int = 5) -> None:
    print(f"\n=== {name} ===")
    psi = build_initial_state(layout, D_bits, R_bits, M_bits, A_bit=0)

    # Observables
    Zop = Z()
    P0 = projector_0()

    for t in range(ticks + 1):
        # Report
        norm = float((psi.dag() * psi).full()[0, 0].real)

        Z_R = []
        P_D0 = []
        for i in range(layout.N):
            Zi = expand_1(layout.n_qubits, Zop, layout.idx_R(i))
            Z_R.append(float(expect(Zi, psi).real))

            Pi = expand_1(layout.n_qubits, P0, layout.idx_D(i))
            P_D0.append(float(expect(Pi, psi).real))

        print(f"t={t:02d}  norm={norm:.6f}  <Z_R>={['%+.3f'%z for z in Z_R]}  P(D=0)={['%.3f'%p for p in P_D0]}")

        # Step
        if t < ticks:
            U = U_tick(layout, **params)
            psi = U * psi

def main():
    # Toggle reservoir
    use_reservoir = True
    layout = Layout1D(N=2, use_reservoir=use_reservoir)

    # Parameters (tune freely)
    params = dict(
        eta0=np.pi / 16,      # regulator integrate strength
        theta=np.pi / 32,     # normal mixing
        theta_drag=np.pi / 128,  # dragged mixing (slower)
        lambda_mix=0.25 if use_reservoir else 0.0,  # regulator<->reservoir coupling
        mu_scramble=0.05 if use_reservoir else 0.0, # reservoir stirring
    )

    if use_reservoir:
        M0 = [0, 0]
    else:
        M0 = None

    # High mismatch
    # D0=0 (R), D1=1 (L)
    run_case(
        "High mismatch (D0=0, D1=1)",
        layout=layout,
        D_bits=[0, 1],
        R_bits=[0, 0],
        M_bits=M0,
        params=params,
        ticks=5,
    )

    # Low mismatch
    # D0=0, D1=0
    run_case(
        "Low mismatch (D0=0, D1=0)",
        layout=layout,
        D_bits=[0, 0],
        R_bits=[0, 0],
        M_bits=M0,
        params=params,
        ticks=5,
    )

if __name__ == "__main__":
    main()
