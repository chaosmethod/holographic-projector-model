import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1) Physics kernels
# -----------------------------
def partial_swap_vec(u, v, s):
    c, j = np.cos(s), -1j * np.sin(s)
    return c * u + j * v, c * v + j * u

def density(phi, chi):
    return (np.abs(phi)**2 + np.abs(chi)**2).real

def stream_x(phi, chi, alpha, Ux, s0, p, dt_scale=1.0):
    H, W = phi.shape
    s_base = s0 * dt_scale
    for parity in (0, 1):
        l = np.arange(parity, W - 1, 2)
        r = l + 1
        ae = np.sqrt(alpha[:, l] * alpha[:, r])
        s = s_base * (ae ** p)

        # +x rail (phi) picks up link phase on (x -> x+1)
        phi[:, l], phi[:, r] = partial_swap_vec(phi[:, l] * Ux[:, l], phi[:, r], s)

        # -x rail (chi) uses conjugate on the same link when moving backward
        chi[:, l], chi[:, r] = partial_swap_vec(chi[:, l], chi[:, r] * np.conj(Ux[:, l]), s)
    return phi, chi

def stream_y(phi, chi, alpha, Uy, s0, p, dt_scale=1.0):
    H, W = phi.shape
    s_base = s0 * dt_scale
    for parity in (0, 1):
        d = np.arange(parity, H - 1, 2)
        u = d + 1
        ae = np.sqrt(alpha[d, :] * alpha[u, :])
        s = s_base * (ae ** p)

        # +y rail (phi) uses link phase on (y -> y+1)
        phi[d, :], phi[u, :] = partial_swap_vec(phi[d, :] * Uy[d, :], phi[u, :], s)

        # -y rail (chi) uses conjugate when moving backward along same link
        chi[d, :], chi[u, :] = partial_swap_vec(chi[d, :], chi[u, :] * np.conj(Uy[d, :]), s)
    return phi, chi

def mix_step(phi, chi, alpha, theta0):
    theta = theta0 * np.sqrt(alpha)
    c, s = np.cos(theta), -1j * np.sin(theta)
    return c * phi + s * chi, s * phi + c * chi

# -----------------------------
# 2) Geometry / regulator
# -----------------------------
def update_geometry(alpha, phi, chi, eta0=0.10, relax=0.02, heal=0.005, floor=0.02):
    d0 = np.abs(phi - chi) ** 2

    # open-boundary gradients (no wrap)
    gx = np.zeros_like(d0.real)
    gx[:, :-1] = (np.abs(phi[:, 1:] - phi[:, :-1])**2 + np.abs(chi[:, 1:] - chi[:, :-1])**2).real

    gy = np.zeros_like(d0.real)
    gy[:-1, :] = (np.abs(phi[1:, :] - phi[:-1, :])**2 + np.abs(chi[1:, :] - chi[:-1, :])**2).real

    r = d0.real + 0.5 * (gx + gy)

    # target pulls alpha down where rough, heal slowly restores toward 1
    target = np.clip(1.0 - eta0 * r, floor, 1.0)
    alpha_next = (1.0 - relax) * alpha + relax * target + heal * (1.0 - alpha)
    return np.clip(alpha_next, floor, 1.0)

# -----------------------------
# 3) Boundaries
# -----------------------------
def make_sponge(H, W, thick=8):
    sponge = np.ones((H, W), dtype=np.float64)
    for i in range(thick):
        # edge i gets mild damping; cumulative multiplication creates ramp
        damp = 0.94 + 0.06 * np.cos(0.5 * np.pi * (i / thick))
        sponge[i, :] *= damp
        sponge[-1 - i, :] *= damp
        sponge[:, i] *= damp
        sponge[:, -1 - i] *= damp
    return sponge

def apply_open_boundaries(phi, chi, sponge):
    return phi * sponge, chi * sponge

# -----------------------------
# 4) Diagnostics
# -----------------------------
def renormalize(phi, chi, eps=1e-20):
    n = np.sqrt(np.sum(np.abs(phi)**2 + np.abs(chi)**2) + eps)
    return phi / n, chi / n, n

def com_of_density(rho, xx, yy, eps=1e-20):
    m = rho.sum() + eps
    com_x = (xx * rho).sum() / m
    com_y = (yy * rho).sum() / m
    return com_x, com_y

def current_no_wrap(phi, chi):
    # forward-difference-ish current proxy without periodic wrap
    H, W = phi.shape
    Jx = np.zeros((H, W), dtype=np.float64)
    Jy = np.zeros((H, W), dtype=np.float64)

    # x-links (x -> x+1)
    Jx[:, :-1] = np.imag(np.conj(phi[:, :-1]) * phi[:, 1:] - np.conj(chi[:, :-1]) * chi[:, 1:])

    # y-links (y -> y+1)
    Jy[:-1, :] = np.imag(np.conj(phi[:-1, :]) * phi[1:, :] - np.conj(chi[:-1, :]) * chi[1:, :])
    return Jx, Jy

# -----------------------------
# 5) Main simulation
# -----------------------------
def run_v5_fixed(H=100, W=160, steps=450,
                 Bz=0.030, q=1.0,         # stronger cyclotron: Bz ~ 0.025–0.035 or q=2.0
                 s0=np.pi/2 * 0.95, p_power=2.5, theta0=0.05,
                 eta0=0.10, relax=0.02, heal=0.005,
                 renorm_every=50,
                 show_quiver=True, quiver_stride=6, quiver_scale=30):

    yy, xx = np.mgrid[0:H, 0:W]
    alpha = np.ones((H, W), dtype=np.float64)

    # Gauge links (Landau gauge): Ux=1, Uy=exp(i q B x)
    Ux = np.ones((H, W), dtype=np.complex128)
    Uy = np.exp(1j * (q * Bz) * xx).astype(np.complex128)

    sponge = make_sponge(H, W, thick=8)

    # Initial wavepacket
    env = np.exp(-((xx - W * 0.2) ** 2 + (yy - H * 0.5) ** 2) / (2 * 7 ** 2))
    phi = (env * np.exp(1j * 0.75 * (xx - W * 0.2))).astype(np.complex128)
    chi = np.zeros_like(phi)
    phi, chi, _ = renormalize(phi, chi)

    # COM history (for crude velocity)
    com_hist = []

    plt.ion()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for t in range(steps):
        # STRANG: X/2 -> Y -> Mix -> Y -> X/2
        phi, chi = stream_x(phi, chi, alpha, Ux, s0, p_power, 0.5)
        phi, chi = stream_y(phi, chi, alpha, Uy, s0, p_power, 1.0)
        phi, chi = mix_step(phi, chi, alpha, theta0)
        phi, chi = stream_y(phi, chi, alpha, Uy, s0, p_power, 1.0)
        phi, chi = stream_x(phi, chi, alpha, Ux, s0, p_power, 0.5)

        # Geometry update + absorbing boundaries
        alpha = update_geometry(alpha, phi, chi, eta0=eta0, relax=relax, heal=heal, floor=0.02)
        phi, chi = apply_open_boundaries(phi, chi, sponge)

        # Renormalize occasionally (for stable visualization / diagnostics)
        if renorm_every and (t % renorm_every == 0) and t > 0:
            phi, chi, n = renormalize(phi, chi)

        if t % 20 == 0:
            rho = density(phi, chi)
            com_x, com_y = com_of_density(rho, xx, yy)
            com_hist.append((t, com_x, com_y))

            # crude velocity over last 2 samples (in steps)
            if len(com_hist) >= 2:
                t0, x0, y0 = com_hist[-2]
                dt = (t - t0) if (t - t0) != 0 else 1
                vx, vy = (com_x - x0) / dt, (com_y - y0) / dt
            else:
                vx, vy = 0.0, 0.0

            print(f"t={t:4d}  COM=({com_x:6.2f}, {com_y:6.2f})  v≈({vx:+.3f}, {vy:+.3f})  alpha_min={alpha.min():.3f}")

            ax1.cla()
            ax2.cla()

            ax1.imshow(np.log10(rho + 1e-12), origin='lower', cmap='magma')
            ax1.set_title(f"Log Density (t={t})  Bz={Bz:.3f} q={q:.1f}")

            if show_quiver:
                Jx, Jy = current_no_wrap(phi, chi)
                ys = slice(0, H, quiver_stride)
                xs = slice(0, W, quiver_stride)
                ax1.quiver(xx[ys, xs], yy[ys, xs], Jx[ys, xs], Jy[ys, xs], scale=quiver_scale, width=0.002)

            ax2.imshow(alpha, origin='lower', vmin=0.2, vmax=1.0, cmap='viridis')
            ax2.set_title(f"Metric Alpha (min={alpha.min():.3f})")

            plt.pause(0.01)

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    run_v5_fixed()
