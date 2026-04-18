#!/usr/bin/env python3
"""
Fluid simulation + visualization → Max/MSP via OSC UDP 7400
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket, struct, math

# ── Parameters ─────────────────────────────────────────────────────────────
N      = 50
ITER   = 4
DT     = 0.1
DIFF   = 0.00005
VISC   = 0.000005
TOP_N  = 20
UDP_HOST = '127.0.0.1'
UDP_PORT = 7400

S = N + 2
def g(): return np.zeros((S, S), dtype=np.float32)

dens  = g(); dens0 = g()
u     = g(); u0    = g()
v     = g(); v0    = g()
p     = g(); div   = g()

# ── Solver ─────────────────────────────────────────────────────────────────
def set_bnd(b, x):
    x[0,  1:-1] = -x[1,  1:-1] if b == 1 else x[1,  1:-1]
    x[-1, 1:-1] = -x[-2, 1:-1] if b == 1 else x[-2, 1:-1]
    x[1:-1,  0] = -x[1:-1,  1] if b == 2 else x[1:-1,  1]
    x[1:-1, -1] = -x[1:-1, -2] if b == 2 else x[1:-1, -2]
    x[0,  0]  = 0.5*(x[1,0]  +x[0,1]);  x[0, -1] = 0.5*(x[1,-1] +x[0,-2])
    x[-1, 0]  = 0.5*(x[-2,0] +x[-1,1]); x[-1,-1] = 0.5*(x[-2,-1]+x[-1,-2])

def lin_solve(b, x, x0, a, c):
    inv = 1.0/c
    for _ in range(ITER):
        x[1:-1,1:-1] = (x0[1:-1,1:-1]+a*(x[:-2,1:-1]+x[2:,1:-1]+x[1:-1,:-2]+x[1:-1,2:]))*inv
        set_bnd(b, x)

def diffuse(b, x, x0, coef):
    a = DT*coef*N*N; lin_solve(b, x, x0, a, 1+4*a)

def advect(b, d, d0, uf, vf):
    dt0 = DT*N
    ii = np.arange(1,N+1)[:,None]; jj = np.arange(1,N+1)[None,:]
    x = np.clip(ii - dt0*uf[1:-1,1:-1], 0.5, N+0.5)
    y = np.clip(jj - dt0*vf[1:-1,1:-1], 0.5, N+0.5)
    i0=x.astype(int); i1=i0+1; j0=y.astype(int); j1=j0+1
    s1=x-i0; s0=1-s1; t1=y-j0; t0=1-t1
    d[1:-1,1:-1]=(s0*(t0*d0[i0,j0]+t1*d0[i0,j1])+s1*(t0*d0[i1,j0]+t1*d0[i1,j1]))
    set_bnd(b, d)

def project():
    div[1:-1,1:-1]=-0.5/N*(u[2:,1:-1]-u[:-2,1:-1]+v[1:-1,2:]-v[1:-1,:-2])
    p[:]=0; set_bnd(0,div); set_bnd(0,p); lin_solve(0,p,div,1,4)
    u[1:-1,1:-1]-=0.5*N*(p[2:,1:-1]-p[:-2,1:-1])
    v[1:-1,1:-1]-=0.5*N*(p[1:-1,2:]-p[1:-1,:-2])
    set_bnd(1,u); set_bnd(2,v)

def vel_step():
    u[:] += DT*u0; v[:] += DT*v0
    u0[:]=u; v0[:]=v; diffuse(1,u,u0,VISC); diffuse(2,v,v0,VISC)
    project(); u0[:]=u; v0[:]=v
    advect(1,u,u0,u0,v0); advect(2,v,v0,u0,v0); project()

def dens_step():
    dens[:] += DT*dens0; dens0[:]=dens
    diffuse(0,dens,dens0,DIFF); dens0[:]=dens; advect(0,dens,dens0,u,v)

# ── OSC ────────────────────────────────────────────────────────────────────
def osc_str(s):
    b=(s+'\x00').encode(); return b+b'\x00'*((4-len(b)%4)%4)
def osc_msg(addr,*args):
    return osc_str(addr)+osc_str(','+('f'*len(args)))+b''.join(struct.pack('>f',float(a)) for a in args)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_to_max():
    inner = dens[1:-1,1:-1]; max_d = inner.max()
    if max_d < 1e-6: return
    flat = inner.flatten(); indices = np.argsort(flat)[-TOP_N:][::-1]
    for idx in indices:
        yi,xi = divmod(int(idx),N)
        d = float(dens[yi+1,xi+1])/max_d
        if d < 0.05: continue
        vx_v=float(u[yi+1,xi+1]); vy_v=float(v[yi+1,xi+1])
        spd=math.sqrt(vx_v**2+vy_v**2); spd_n=min(spd,1.0)
        vx_n=(vx_v/spd*spd_n if spd>1e-4 else 0.0)
        vy_n=(vy_v/spd*spd_n if spd>1e-4 else 0.0)
        sock.sendto(osc_msg('/grain',xi/(N-1),yi/(N-1),d,vx_n,vy_n),(UDP_HOST,UDP_PORT))

def add(x_n, y_n, d_amt, ux_amt, vy_amt):
    ix=max(1,min(N,int(x_n*(N-1))+1)); iy=max(1,min(N,int(y_n*(N-1))+1))
    dens0[ix,iy]+=d_amt; u0[ix,iy]+=ux_amt; v0[ix,iy]+=vy_amt

# ── Visualization ──────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6,6), facecolor='black')
ax.set_facecolor('black')
ax.set_xticks([]); ax.set_yticks([])
ax.set_title('Fluid → Max/MSP', color='white', pad=8)

im = ax.imshow(
    dens[1:-1,1:-1].T, origin='lower',
    cmap='inferno', vmin=0, vmax=1,
    extent=[0,N,0,N], interpolation='bilinear'
)

# Quiver (velocity arrows, subsampled)
step = 5
qi = np.arange(step//2, N, step)
qj = np.arange(step//2, N, step)
QI, QJ = np.meshgrid(qi, qj)
Q = ax.quiver(
    QI, QJ,
    u[qi+1][:,qj+1].T, v[qi+1][:,qj+1].T,
    color='cyan', alpha=0.5, scale=30, width=0.003
)

t_state = [0.0]

def update(frame):
    t = t_state[0]
    dens0[:]=0; u0[:]=0; v0[:]=0

    cx=0.5+0.28*math.sin(t*0.4); cy=0.5+0.28*math.cos(t*0.25)
    angle=t*1.3
    add(cx,cy,90.0,math.cos(angle)*6.0,math.sin(angle)*6.0)
    add(1-cx,1-cy,45.0,-math.cos(angle+1.0)*4.0,-math.sin(angle+1.0)*4.0)
    if math.sin(t*0.8)>0.95:
        rx=0.3+0.4*abs(math.sin(t*2.3)); ry=0.3+0.4*abs(math.cos(t*1.7))
        add(rx,ry,60.0,math.sin(t*3.1)*5.0,math.cos(t*2.7)*5.0)

    vel_step(); dens_step(); send_to_max()

    # Update density heatmap
    d = dens[1:-1,1:-1]
    mx = max(float(d.max()), 1.0)
    im.set_data(d.T); im.set_clim(0, mx)

    # Update velocity arrows
    ux = u[qi+1][:,qj+1]; vx = v[qi+1][:,qj+1]
    Q.set_UVC(ux.T, vx.T)

    t_state[0] += DT
    return [im, Q]

ani = animation.FuncAnimation(fig, update, interval=33, blit=True)
plt.tight_layout()
print(f"Fluid viz → Max UDP {UDP_PORT}  (close window to stop)")
plt.show()
