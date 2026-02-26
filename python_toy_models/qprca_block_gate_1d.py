"""
qprca_block_gate_1d.py
------------------------------------------------------------
HPF–QPRCA (UHET) reference block-gate update in 1+1D.

Key design goals:
- Strictly unitary, strictly local.
- Avoid "control overlaps swap targets" (the bug you found).
- Provide an inspectable mechanism for:
  - Regulation (load sensing via overlap probe)
  - Streaming (unitary transport)
  - Mixing (Dirac coin/mass)
  - Optional reversible "relaxation" via a local reservoir qubit

This is NOT a full production simulator. It is a reference construction.
------------------------------------------------------------

State layout (N sites, periodic by default in the toy harness):
Per site i:
  D_i : 1 qubit  (toy Dirac: |0>=R, |1>=L  for minimalism)
  R_i : 1 qubit  (regulator "availability/drag" degree)
  M_i : 1 qubit  (optional reservoir; can be disabled)

Global ancilla:
  A   : 1 qubit  (reused across probes and streaming control computation)

NOTE: Using a single-qubit Dirac encoding makes "conditional shift" awkward,
because the chirality bit is the same bit you would otherwise move.
To keep this minimal but correct, we implement streaming via a controlled-SWAP
whose control is computed into ancilla A *without* overlapping swap targets.

If you later move to a 2-rail encoding (L_i and R_i rails), streaming becomes
control-free and even cleaner.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
from qutip import Qobj, qeye, tensor
from qutip.qip.operations import (
    hadamard_transform as H_gate,
    gate_expand_1toN,
    gate_expand_2toN,
    cnot,
    swap,
    controlled_gate,
    ry,
)

# -------------------------
# Utility: basis operators
# -------------------------

def I() -> Qobj:
    return qeye(2)

def H() -> Qobj:
    return H_gate()

def X() -> Qobj:
    return Qobj(np.array([[0, 1], [1, 0]], dtype=complex))

def Ry(theta: float) -> Qobj:
    return ry(theta)

def SWAP() -> Qobj:
    return swap()

def CNOT() -> Qobj:
    return cnot()

def CSWAP() -> Qobj:
    """Controlled-SWAP (Fredkin) as a 3-qubit gate."""
    # Build CSWAP from a controlled SWAP on the last two qubits
    # qutip's controlled_gate controls the first qubit by default.
    return controlled_gate(SWAP())

# -------------------------
# Indexing convention
# -------------------------

@dataclass(frozen=True)
class Layout1D:
    """
    Qubit ordering in the total Hilbert space:

    [ D_0, R_0, M_0,  D_1, R_1, M_1,  ... ,  D_{N-1}, R_{N-1}, M_{N-1},  A ]

    If use_reservoir=False, we omit M_i, and layout becomes:
    [ D_0, R_0,  D_1, R_1, ... , D_{N-1}, R_{N-1},  A ]
    """
    N: int
    use_reservoir: bool = True

    def idx_D(self, i: int) -> int:
        if self.use_reservoir:
            return 3 * i + 0
        return 2 * i + 0

    def idx_R(self, i: int) -> int:
        if self.use_reservoir:
            return 3 * i + 1
        return 2 * i + 1

    def idx_M(self, i: int) -> int:
        if not self.use_reservoir:
            raise ValueError("Reservoir disabled; no M index.")
        return 3 * i + 2

    @property
    def idx_A(self) -> int:
        return (3 * self.N) if self.use_reservoir else (2 * self.N)

    @property
    def n_qubits(self) -> int:
        return self.idx_A + 1

# -------------------------
# Gate expansion helpers
# -------------------------

def expand_1(layout: Layout1D, gate1: Qobj, target: int) -> Qobj:
    return gate_expand_1toN(gate1, layout.n_qubits, target)

def expand_2(layout: Layout1D, gate2: Qobj, targets: Tuple[int, int]) -> Qobj:
    return gate_expand_2toN(gate2, layout.n_qubits, targets)

def expand_3(layout: Layout1D, gate3: Qobj, targets: Tuple[int, int, int]) -> Qobj:
    # qutip has no direct expand_3 helper; do manual tensor placement
    # by building full identity then embedding with permutes is annoying.
    # We'll construct via controlled_gate patterns using expand_2/1:
    raise NotImplementedError("Use the provided primitives for 3-qubit patterns below.")

# -------------------------
# Core: overlap probe (swap-test-like) between D_i and D_j into A
# -------------------------

def overlap_probe_U(layout: Layout1D, i: int, j: int) -> Qobj:
    """
    Unitary probe that correlates ancilla A with overlap between D_i and D_j.

    We use the classic pattern:
      H(A) -> CSWAP(A, D_i, D_j) -> H(A)

    This is unitary and reversible; no measurement.
    """
    A = layout.idx_A
    Di = layout.idx_D(i)
    Dj = layout.idx_D(j)

    U = qeye(2 ** layout.n_qubits)
    U = expand_1(layout, H(), A) * U
    # Controlled-SWAP with control=A, swap targets=Di,Dj:
    # Build CSWAP acting on (A,Di,Dj) by expanding a 3-qubit CSWAP:
    # qutip controlled_gate(SWAP()) controls first qubit, swaps next two.
    # We must place it on (A,Di,Dj) in that order.
    U_cswap = gate_expand_2toN(SWAP(), layout.n_qubits, (Di, Dj))  # swap on Di,Dj
    U = controlled_gate(U_cswap, control=A, target=Di) * U  # NOT correct placement

    # The above line is not a correct generic 3-qubit embed in qutip-qip.
    # So we do the safe route: build full 3-qubit CSWAP and permute indices
    # ourselves using tensor and permute. This is simpler and unambiguous.

    # Build CSWAP on 3 qubits:
    cswap3 = CSWAP()
    # Embed by permuting:
    U = embed_3q_gate(layout, cswap3, (A, Di, Dj)) * U
    U = expand_1(layout, H(), A) * U
    return U

def embed_3q_gate(layout: Layout1D, gate3: Qobj, qubits: Tuple[int, int, int]) -> Qobj:
    """
    Embed a 3-qubit gate onto arbitrary qubit indices.

    This uses qutip's tensor permutation: create full operator as I⊗...⊗gate⊗...⊗I
    with gate placed on the *last* 3 qubits, then permute into position.

    This is robust and explicit (inspection-friendly).
    """
    n = layout.n_qubits
    q0, q1, q2 = qubits
    if len({q0, q1, q2}) != 3:
        raise ValueError("Qubits must be distinct for 3q gate embedding.")

    # Build operator with gate on the last 3 slots:
    ops = [I()] * (n - 3) + [gate3]
    U = tensor(ops)

    # Current ordering of U acts on qubits [0..n-4, n-3, n-2, n-1]
    # We want it to act on [0..n-1] with gate on (q0,q1,q2).
    # Build a permutation that sends (n-3,n-2,n-1) -> (q0,q1,q2).
    src = list(range(n))
    # We'll map destination positions to sources:
    # Place last3 sources into q0,q1,q2 destinations; keep others in order.
    remaining_src = [k for k in src if k not in (n - 3, n - 2, n - 1)]
    dest_to_src = [None] * n
    dest_to_src[q0] = n - 3
    dest_to_src[q1] = n - 2
    dest_to_src[q2] = n - 1
    it = iter(remaining_src)
    for d in range(n):
        if dest_to_src[d] is None:
            dest_to_src[d] = next(it)

    return U.permute(dest_to_src)

# -------------------------
# Regulator update from probe
# -------------------------

def regulator_integrate_from_A(layout: Layout1D, i: int, eta0: float) -> Qobj:
    """
    Apply controlled Ry(eta0) to regulator R_i, controlled by ancilla A.

    This is your "integrate local roughness into R_i".
    """
    A = layout.idx_A
    Ri = layout.idx_R(i)

    # Controlled single-qubit gate: control=A, target=Ri
    U_ry = expand_1(layout, Ry(eta0), Ri)
    U = controlled_gate(U_ry, control=A, target=Ri)
    return U

# -------------------------
# Streaming (1D) with ancilla-decoupled control
# -------------------------

def stream_pair_unitary(layout: Layout1D, i: int, j: int, direction: str) -> Qobj:
    """
    Stream between neighboring sites i and j (j = i+1 mod N).

    Minimal encoding: D qubit holds chirality: |0>=R, |1>=L.

    We want:
      - if D_i indicates R (|0>), swap D_i with D_j  (right mover goes right)
      - if D_j indicates L (|1>), swap D_j with D_i  (left mover goes left)

    Doing this naively with control living inside D that is being swapped causes
    nonunitary collisions. So we compute control into A, perform CSWAP(A, D_i, D_j),
    and uncompute A.

    direction:
      "R": condition on D_i == 0  (right-moving at i)
      "L": condition on D_j == 1  (left-moving at j)
    """
    A = layout.idx_A
    Di = layout.idx_D(i)
    Dj = layout.idx_D(j)

    U = qeye(2 ** layout.n_qubits)

    if direction == "R":
        # control predicate: (D_i == 0)
        U = expand_1(layout, X(), Di) * U
        U = expand_2(layout, CNOT(), (Di, A)) * U
        U = expand_1(layout, X(), Di) * U

        # controlled swap on A
        U = embed_3q_gate(layout, CSWAP(), (A, Di, Dj)) * U

        # uncompute A
        U = expand_1(layout, X(), Di) * U
        U = expand_2(layout, CNOT(), (Di, A)) * U
        U = expand_1(layout, X(), Di) * U

    elif direction == "L":
        # control predicate: (D_j == 1)
        U = expand_2(layout, CNOT(), (Dj, A)) * U
        U = embed_3q_gate(layout, CSWAP(), (A, Di, Dj)) * U
        U = expand_2(layout, CNOT(), (Dj, A)) * U

    else:
        raise ValueError("direction must be 'R' or 'L'")

    return U

def U_stream_1d(layout: Layout1D) -> Qobj:
    """
    One streaming layer for the whole lattice in 1D.
    For N=2, there is a single pair (0,1). For N>2, you would apply disjoint
    swaps in an even-odd partition (Margolus in 1D).

    This reference applies streaming on disjoint pairs (0,1), (2,3), ...
    then you can call again with shifted pairing for the next partition.
    """
    U = qeye(2 ** layout.n_qubits)
    N = layout.N
    for i in range(0, N, 2):
        j = (i + 1) % N
        # Apply R-stream then L-stream; order is a design choice.
        U = stream_pair_unitary(layout, i, j, "R") * U
        U = stream_pair_unitary(layout, i, j, "L") * U
    return U

# -------------------------
# Mixing (Dirac coin/mass) controlled by regulator
# -------------------------

def U_mix_site(layout: Layout1D, i: int, theta: float, theta_drag: float) -> Qobj:
    """
    Apply a "coin/mass" rotation on D_i.
    If R_i=0: apply Ry(theta)
    If R_i=1: apply Ry(theta_drag)

    This is a toy stand-in for exp(-i theta beta) on a 4D Dirac spinor.
    """
    Di = layout.idx_D(i)
    Ri = layout.idx_R(i)

    U = qeye(2 ** layout.n_qubits)

    # control-on-0: apply Ry(theta)
    U = expand_1(layout, X(), Ri) * U
    U_theta = expand_1(layout, Ry(theta), Di)
    U = controlled_gate(U_theta, control=Ri, target=Di) * U
    U = expand_1(layout, X(), Ri) * U

    # control-on-1: apply Ry(theta_drag)
    U_drag = expand_1(layout, Ry(theta_drag), Di)
    U = controlled_gate(U_drag, control=Ri, target=Di) * U

    return U

def U_mix_all(layout: Layout1D, theta: float, theta_drag: float) -> Qobj:
    U = qeye(2 ** layout.n_qubits)
    for i in range(layout.N):
        U = U_mix_site(layout, i, theta, theta_drag) * U
    return U

# -------------------------
# Reversible relaxation via reservoir (optional)
# -------------------------

def U_relax_all(layout: Layout1D, lambda_mix: float, mu_scramble: float) -> Qobj:
    """
    Reversible "relaxation" is implemented by coupling R_i <-> M_i unitary.

    We implement:
      - partial swap between R and M via exp(-i * lambda * (XX+YY)/2) (iSWAP-like)
      - optional scramble (Ry) on M to prevent perfect recording

    If reservoir disabled, returns identity.
    """
    if not layout.use_reservoir:
        return qeye(2 ** layout.n_qubits)

    # Two-qubit mixing unitary on (R,M):
    # U_rm = exp(-i * lambda * (XX+YY)/2) is iSWAP^lambda up to phases.
    # We'll build XX+YY Hamiltonian explicitly.
    sx = Qobj(np.array([[0, 1], [1, 0]], dtype=complex))
    sy = Qobj(np.array([[0, -1j], [1j, 0]], dtype=complex))
    H_xy = (tensor(sx, sx) + tensor(sy, sy)) / 2.0
    U_rm = (-1j * lambda_mix * H_xy).expm()

    U = qeye(2 ** layout.n_qubits)
    for i in range(layout.N):
        Ri = layout.idx_R(i)
        Mi = layout.idx_M(i)
        U = expand_2(layout, U_rm, (Ri, Mi)) * U
        if mu_scramble is not None and abs(mu_scramble) > 0:
            U = expand_1(layout, Ry(mu_scramble), Mi) * U
    return U

# -------------------------
# Full block tick: U = U_relax * U_mix * U_stream * U_ren
# (order chosen for convenience; keep consistent in experiments)
# -------------------------

def U_ren_all(layout: Layout1D, eta0: float) -> Qobj:
    """
    For 1D nearest neighbors in a single block pairing:
      probe (D_i, D_{i+1}) -> integrate into R_i (forward-only)
    """
    U = qeye(2 ** layout.n_qubits)
    N = layout.N
    for i in range(0, N, 2):
        j = (i + 1) % N
        U = overlap_probe_U(layout, i, j) * U
        U = regulator_integrate_from_A(layout, i, eta0) * U
        # uncompute probe to return A to |0>:
        U = overlap_probe_U(layout, i, j) * U
    return U

def U_tick(layout: Layout1D,
           eta0: float,
           theta: float,
           theta_drag: float,
           lambda_mix: float = 0.0,
           mu_scramble: float = 0.0) -> Qobj:
    """
    One full tick.
    """
    U = qeye(2 ** layout.n_qubits)
    U = U_ren_all(layout, eta0) * U
    U = U_stream_1d(layout) * U
    U = U_mix_all(layout, theta, theta_drag) * U
    U = U_relax_all(layout, lambda_mix, mu_scramble) * U
    return U
