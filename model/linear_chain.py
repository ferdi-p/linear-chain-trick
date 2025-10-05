from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp

def linear_chain(mu: float, k: int, tmax: float = 10.0, npts: int = 800):
    r = k / mu
    def rhs(_t, y):
        dy = np.empty_like(y)
        dy[0] = r * (0.0 - y[0])
        dy[1:] = r * (y[:-1] - y[1:])
        return dy
    y0 = np.zeros(k); y0[0] = 1.0
    t_eval = np.linspace(0.0, float(tmax), int(npts))
    sol = solve_ivp(rhs, (0.0, float(tmax)), y0, t_eval=t_eval, method='LSODA', rtol=1e-7, atol=1e-9)
    if not sol.success:
        raise RuntimeError(sol.message)
    Jk = sol.y[-1]
    pdf = np.clip((k / mu) * Jk, 0.0, None)
    return sol.t.tolist(), pdf.tolist()
