# HPF–QPRCA Block-Gate Pseudocode (Inspectable)
# ------------------------------------------------------------
# Lattice: 3D grid with Margolus partitions P0, P1 of 2x2x2 blocks
# Per site: Dirac subspace D (dim=4) and regulator qubit R (dim=2)
# Optional block-local ancilla qubit A used transiently (must be uncomputed)
#
# One tick:
#   for b in P0: U_block(b)
#   for b in P1: U_block(b)
#
# Constraints:
#   - All operations are unitary
#   - Strictly local (within block or across a block edge via partition scheduling)
#   - Ancilla must end returned to |0>
# ------------------------------------------------------------

# ----------------------------
# Utility primitives (abstract)
# ----------------------------

def H(qubit): ...
def CNOT(ctrl, tgt): ...
def CTRL_SWAP(ctrl_qubit, regA, regB): ...
def SWAP(regA, regB): ...
def CTRL_U(ctrl_qubit, U, reg): ...
def U4_on_Dirac(U4, site): ...
def CTRL_U4_on_Dirac(ctrl_qubit, U4, site): ...
def RY(angle, qubit): ...
def CTRL_RY(ctrl_qubit, angle, qubit): ...
def PHASE(angle, qubit): ...
def CTRL_PHASE(ctrl_qubit, angle, qubit): ...

# Notes:
# - "regA/regB" can be multi-qubit registers (e.g., Dirac 4-dim encoded in 2 qubits)
# - U4 is a 4x4 unitary applied to the Dirac register (2 qubits)
# - Angles are discretized / LUT-derived, consistent with finite resolution


# --------------------------------------------
# Model parameters / LUTs (finite-resolution)
# --------------------------------------------

theta = ...            # base mixing angle ~ m * Δt
theta_drag_LUT = ...   # optional map from regulator state -> effective theta' (if multi-level)
eta0 = ...             # base regulator rotation increment per neighbor probe
kappa = ...            # stiffness / slope for LUT shaping
LUT_eta = ...          # maps probe outcome -> rotation angle increment (bounded)

# Dirac matrix exponentials (choose representation)
U_mix_normal = expm(-1j * theta * beta)      # 4x4
U_mix_drag   = expm(-1j * theta * beta * c_drag)  # 4x4, c_drag in (0,1) or LUT-driven


# ------------------------------------------------------------
# Margolus block representation
# ------------------------------------------------------------
# A block b contains 8 sites with coordinates relative to block origin:
#   (0/1, 0/1, 0/1)
# We'll refer to sites as s000, s100, s010, ..., s111
# Each site has:
#   site.D : Dirac register (dim 4; 2 qubits)
#   site.R : regulator qubit
#
# Neighbors inside a 2x2x2 block along +x, +y, +z exist when coord component = 0.
# ------------------------------------------------------------

def U_block(block):
    """
    One 2x2x2 Margolus block update:
      U_block = U_ren * U_stream * U_mix
    """
    U_ren(block)
    U_stream(block)
    U_mix(block)


# ------------------------------------------------------------
# 1) Renormalization / Regulation layer (gradient-energy proxy)
# ------------------------------------------------------------

def U_ren(block):
    """
    For each site x in block:
      For each forward neighbor (x+ex, x+ey, x+ez) that exists within block:
        - perform overlap probe (swap-test style) into ancilla A
        - rotate regulator R(x) conditioned on ancilla
        - uncompute ancilla
    Ancilla is reused; it MUST return to |0>.
    """

    # Single reusable ancilla qubit, initialized |0>
    A = block.ancilla  # exists only in pseudocode; in implementation it is a scratch qubit
    # Ensure A starts in |0> (in actual circuit, it's allocated/reset by design)
    # No measurement allowed; must be uncomputed each use.

    for site in block.sites:
        x = site

        for neighbor in forward_neighbors_within_block(block, x):
            y = neighbor

            # --- Overlap probe between Dirac registers D(x) and D(y) ---
            # Standard pattern:
            #   H(A); controlled-SWAP(A, D(x), D(y)); H(A)
            H(A)
            CTRL_SWAP(A, x.D, y.D)
            H(A)

            # --- Regulator rotation conditioned on probe ancilla ---
            # If A=1 (indicating mismatch/roughness in the swap-test basis),
            # apply a small bounded rotation to x.R
            #
            # "No-fuss" fixed increment:
            #   CTRL_RY(A, eta0, x.R)
            #
            # If you want stiffness shaping, replace eta0 with a LUT keyed by A only
            # (still bounded) or by a multi-ancilla scheme (more complex).
            CTRL_RY(A, eta0, x.R)

            # --- Uncompute overlap probe (reverse) ---
            H(A)
            CTRL_SWAP(A, x.D, y.D)
            H(A)

            # At this point A is back to |0> exactly (unitary uncompute)


def forward_neighbors_within_block(block, x):
    """
    Return neighbors y = x + ex, x + ey, x + ez that lie inside the 2x2x2 block.
    Forward-only avoids double counting; still symmetric at large scale due to partition alternation.
    """
    nbrs = []
    cx, cy, cz = x.rel_coord  # each in {0,1}
    if cx == 0: nbrs.append(block.site_at(1, cy, cz))   # +x
    if cy == 0: nbrs.append(block.site_at(cx, 1, cz))   # +y
    if cz == 0: nbrs.append(block.site_at(cx, cy, 1))   # +z
    return nbrs


# ------------------------------------------------------------
# 2) Streaming layer (Dirac transport via conditional SWAP nets)
# ------------------------------------------------------------

def U_stream(block):
    """
    Implements discrete-time Dirac streaming in x,y,z directions.
    Uses disjoint SWAP networks inside the block for each axis.
    Assumes a fixed mapping of Dirac components to propagation directions.

    Implementation approach:
      - Represent Dirac 4-dim register as 2 qubits (q0,q1)
      - Define projectors onto internal "channels" that determine shift direction.
      - In gate terms, use controlled-SWAPs between neighbor Dirac registers,
        controlled by internal-state bits (or derived control lines).

    For inspection, we express as abstract operations SHIFT_AXIS(block, axis).
    """

    SHIFT_AXIS(block, axis='x')
    SHIFT_AXIS(block, axis='y')
    SHIFT_AXIS(block, axis='z')


def SHIFT_AXIS(block, axis):
    """
    Axis shift implemented as parallel neighbor swaps.
    The exact mapping from Dirac components -> +/- direction is a design choice.
    Minimal no-fuss mapping:
      - upper two components (phi) stream +axis
      - lower two components (chi) stream -axis
    This can be implemented by conditional swaps between neighbor sites.

    Because this is within a 2x2x2 block, neighbor pairs are disjoint.
    """

    pairs_plus, pairs_minus = neighbor_pairs_for_axis(block, axis)

    # Stream phi (+axis): swap phi-subspace between x and x+axis
    for (x, y) in pairs_plus:
        # conditional swap only for phi components of Dirac register
        # Implement as controlled swaps on the Dirac register bits that encode phi-vs-chi.
        COND_SWAP_PHI(x.D, y.D)

    # Stream chi (-axis): swap chi-subspace between x and x-axis
    for (x, y) in pairs_minus:
        COND_SWAP_CHI(x.D, y.D)


def neighbor_pairs_for_axis(block, axis):
    """
    Returns disjoint neighbor pairs for +axis and -axis streaming inside the block.
    In a 2x2x2 block, these are simply edges along that axis.
    """
    plus = []
    minus = []

    for site in block.sites:
        cx, cy, cz = site.rel_coord
        if axis == 'x' and cx == 0:
            plus.append((block.site_at(0, cy, cz), block.site_at(1, cy, cz)))
            # minus uses the same physical swap set; direction is encoded by which components swap
            minus.append((block.site_at(1, cy, cz), block.site_at(0, cy, cz)))

        if axis == 'y' and cy == 0:
            plus.append((block.site_at(cx, 0, cz), block.site_at(cx, 1, cz)))
            minus.append((block.site_at(cx, 1, cz), block.site_at(cx, 0, cz)))

        if axis == 'z' and cz == 0:
            plus.append((block.site_at(cx, cy, 0), block.site_at(cx, cy, 1)))
            minus.append((block.site_at(cx, cy, 1), block.site_at(cx, cy, 0)))

    return plus, minus


def COND_SWAP_PHI(Dx, Dy):
    """
    Swap only the phi (upper) components between two Dirac registers.
    Implementation depends on Dirac encoding.
    If Dirac register is 2 qubits, you can define:
      |00>,|01> = phi components
      |10>,|11> = chi components
    Then phi swap is controlled on the MSB == 0.
    """
    # Abstract form:
    #   if MSB(D)==0: SWAP(state between Dx and Dy)
    CTRL_SWAP(ctrl_qubit=MSB_is_zero_control(Dx, Dy), regA=Dx, regB=Dy)


def COND_SWAP_CHI(Dx, Dy):
    """
    Swap only the chi (lower) components.
    Using same encoding, controlled on MSB == 1.
    """
    CTRL_SWAP(ctrl_qubit=MSB_is_one_control(Dx, Dy), regA=Dx, regB=Dy)


def MSB_is_zero_control(Dx, Dy):
    """
    Returns a control line that is 1 when the relevant internal-state MSB indicates phi.
    In practice, this is implemented by using the MSB qubit (possibly with X gates).
    Shown abstractly for inspection.
    """
    ...


def MSB_is_one_control(Dx, Dy):
    """
    Control line for chi components (MSB==1).
    """
    ...


# ------------------------------------------------------------
# 3) Mixing layer (mass term with regulator-controlled drag)
# ------------------------------------------------------------

def U_mix(block):
    """
    Apply site-local Dirac mixing U_mix, controlled by regulator R.
    - If R=0: normal mixing (theta)
    - If R=1: dragged mixing (theta')
    This is the causal mechanism for dilation/latency.
    """
    for site in block.sites:
        r = site.R
        # Control: if r==0 apply normal, if r==1 apply drag.
        # The simplest inspection-friendly implementation uses two controlled applications:
        #
        #   if r==0: apply U_mix_normal
        #   if r==1: apply U_mix_drag
        #
        # In circuit form, you implement one as control-on-1, and the other as control-on-0 (with X wrappers).
        APPLY_CONTROLLED_MIX(site, U_mix_normal, U_mix_drag)


def APPLY_CONTROLLED_MIX(site, U0, U1):
    r = site.R

    # Apply U0 when r=0
    X(r)                   # flip so r=0 becomes control=1
    CTRL_U4_on_Dirac(r, U0, site.D)
    X(r)

    # Apply U1 when r=1
    CTRL_U4_on_Dirac(r, U1, site.D)


def X(qubit): ...
