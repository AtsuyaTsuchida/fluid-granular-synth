#!/usr/bin/env python3
"""
50x50 Stable Fluid Simulation (Jos Stam) → Max/MSP via OSC UDP 7400

Send format: /grain x y density vx vy  (top-N dense cells per frame)
  x, y    : 0.0-1.0  (normalized grid position)
  density : 0.0-1.0  (normalized)
  vx, vy  : -1.0 to 1.0 (normalized velocity direction × speed)
"""

import numpy as np
import socket
import struct
import time
import math

# ── Parameters ─────────────────────────────────────────────────────────────
N      = 50          # grid size
ITER   = 4           # linear solver iterations (more = accurate, slower)
DT     = 0.1         # time step
DIFF   = 0.00005     # density diffusion
VISC   = 0.000005    # viscosity
TOP_N  = 20          # cells to send per frame
FPS    = 30          # target framerate

UDP_HOST = '127.0.0.1'
UDP_PORT = 7400

# ── Grid setup ─────────────────────────────────────────────────────────────
S = N + 2  # with boundary padding

def g(): return np.zeros((S, S), dtype=np.float32)

dens  = g(); dens0 = g()
u     = g(); u0    = g()
v     = g(); v0    = g()
p     = g(); div   = g()

# ── Fluid solver ───────────────────────────────────────────────────────────
def set_bnd(b, x):
    x[0,  1:-1] = -x[1,  1:-1] if b == 1 else x[1,  1:-1]
    x[-1, 1:-1] = -x[-2, 1:-1] if b == 1 else x[-2, 1:-1]
    x[1:-1,  0] = -x[1:-1,  1] if b == 2 else x[1:-1,  1]
    x[1:-1, -1] = -x[1:-1, -2] if b == 2 else x[1:-1, -2]
    x[0,  0]  = 0.5 * (x[1, 0]   + x[0,  1])
    x[0,  -1] = 0.5 * (x[1, -1]  + x[0,  -2])
    x[-1, 0]  = 0.5 * (x[-2, 0]  + x[-1,  1])
    x[-1, -1] = 0.5 * (x[-2, -1] + x[-1, -2])

def lin_solve(b, x, x0, a, c):
    inv = 1.0 / c
    for _ in range(ITER):
        x[1:-1, 1:-1] = (x0[1:-1, 1:-1] + a * (
            x[:-2, 1:-1] + x[2:, 1:-1] +
            x[1:-1, :-2] + x[1:-1, 2:]
        )) * inv
        set_bnd(b, x)

def diffuse(b, x, x0, coef):
    a = DT * coef * N * N
    lin_solve(b, x, x0, a, 1 + 4 * a)

def advect(b, d, d0, uf, vf):
    dt0 = DT * N
    ii = np.arange(1, N + 1)[:, None]
    jj = np.arange(1, N + 1)[None, :]
    x = np.clip(ii - dt0 * uf[1:-1, 1:-1], 0.5, N + 0.5)
    y = np.clip(jj - dt0 * vf[1:-1, 1:-1], 0.5, N + 0.5)
    i0 = x.astype(int); i1 = i0 + 1
    j0 = y.astype(int); j1 = j0 + 1
    s1 = x - i0; s0 = 1 - s1
    t1 = y - j0; t0 = 1 - t1
    d[1:-1, 1:-1] = (
        s0 * (t0 * d0[i0, j0] + t1 * d0[i0, j1]) +
        s1 * (t0 * d0[i1, j0] + t1 * d0[i1, j1])
    )
    set_bnd(b, d)

def project():
    div[1:-1, 1:-1] = -0.5 / N * (
        u[2:,  1:-1] - u[:-2, 1:-1] +
        v[1:-1, 2:] - v[1:-1, :-2]
    )
    p[:] = 0
    set_bnd(0, div); set_bnd(0, p)
    lin_solve(0, p, div, 1, 4)
    u[1:-1, 1:-1] -= 0.5 * N * (p[2:, 1:-1] - p[:-2, 1:-1])
    v[1:-1, 1:-1] -= 0.5 * N * (p[1:-1, 2:] - p[1:-1, :-2])
    set_bnd(1, u); set_bnd(2, v)

def vel_step():
    u[:] += DT * u0; v[:] += DT * v0
    u0[:] = u;    v0[:] = v
    diffuse(1, u, u0, VISC)
    diffuse(2, v, v0, VISC)
    project()
    u0[:] = u; v0[:] = v
    advect(1, u, u0, u0, v0)
    advect(2, v, v0, u0, v0)
    project()

def dens_step():
    dens[:] += DT * dens0
    dens0[:] = dens
    diffuse(0, dens, dens0, DIFF)
    dens0[:] = dens
    advect(0, dens, dens0, u, v)

# ── OSC encoding ───────────────────────────────────────────────────────────
def osc_str(s):
    b = (s + '\x00').encode()
    return b + b'\x00' * ((4 - len(b) % 4) % 4)

def osc_msg(addr, *args):
    return (osc_str(addr) + osc_str(',' + 'f' * len(args)) +
            b''.join(struct.pack('>f', float(a)) for a in args))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_to_max():
    inner = dens[1:-1, 1:-1]
    max_d = inner.max()
    if max_d < 1e-6:
        return
    flat    = inner.flatten()
    indices = np.argsort(flat)[-TOP_N:][::-1]
    for idx in indices:
        yi, xi = divmod(int(idx), N)
        d = float(dens[yi+1, xi+1]) / max_d
        if d < 0.05:
            continue
        vx_val = float(u[yi+1, xi+1])
        vy_val = float(v[yi+1, xi+1])
        speed  = math.sqrt(vx_val**2 + vy_val**2)
        spd_n  = min(speed, 1.0)
        if speed > 1e-4:
            vx_n = vx_val / speed * spd_n
            vy_n = vy_val / speed * spd_n
        else:
            vx_n = vy_n = 0.0
        sock.sendto(
            osc_msg('/grain',
                    xi / (N - 1), yi / (N - 1),
                    d, vx_n, vy_n),
            (UDP_HOST, UDP_PORT)
        )

# ── Sources ────────────────────────────────────────────────────────────────
def add(x_n, y_n, d_amt, ux_amt, vy_amt):
    ix = max(1, min(N, int(x_n * (N - 1)) + 1))
    iy = max(1, min(N, int(y_n * (N - 1)) + 1))
    dens0[ix, iy] += d_amt
    u0[ix, iy]    += ux_amt
    v0[ix, iy]    += vy_amt

# ── Main loop ──────────────────────────────────────────────────────────────
def main():
    t = 0.0
    interval = 1.0 / FPS
    print(f"Fluid sim running → UDP {UDP_PORT}  (Ctrl+C to stop)")

    while True:
        tick = time.time()

        dens0[:] = 0; u0[:] = 0; v0[:] = 0

        # Primary source: orbits center, rotates emission direction
        cx = 0.5 + 0.28 * math.sin(t * 0.4)
        cy = 0.5 + 0.28 * math.cos(t * 0.25)
        angle = t * 1.3
        add(cx, cy, 90.0,
            math.cos(angle) * 6.0,
            math.sin(angle) * 6.0)

        # Secondary source: opposite phase
        add(1 - cx, 1 - cy, 45.0,
            -math.cos(angle + 1.0) * 4.0,
            -math.sin(angle + 1.0) * 4.0)

        # Occasional random burst
        if math.sin(t * 0.8) > 0.95:
            rx = 0.3 + 0.4 * abs(math.sin(t * 2.3))
            ry = 0.3 + 0.4 * abs(math.cos(t * 1.7))
            add(rx, ry, 60.0,
                math.sin(t * 3.1) * 5.0,
                math.cos(t * 2.7) * 5.0)

        vel_step()
        dens_step()
        send_to_max()

        t += DT
        wait = interval - (time.time() - tick)
        if wait > 0:
            time.sleep(wait)

if __name__ == '__main__':
    main()
