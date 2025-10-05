from nicegui import ui
import numpy as np
from scipy.integrate import solve_ivp

# ---- math: k-stage linear chain -> pdf = (k/mu) * J_k(t) ----
def linear_chain(mu: float, k: int, tmax: float, npts: int = 800):
    r = k / mu
    def rhs(t, y):
        dy = np.empty_like(y)
        dy[0] = r * (0.0 - y[0])           # J1' = r(0 - J1)
        dy[1:] = r * (y[:-1] - y[1:])      # Ji' = r(J_{i-1} - Ji)
        return dy
    y0 = np.zeros(k); y0[0] = 1.0
    t_eval = np.linspace(0.0, float(tmax), int(npts))
    sol = solve_ivp(rhs, (0.0, float(tmax)), y0, t_eval=t_eval,
                    method='LSODA', rtol=1e-7, atol=1e-9)
    if not sol.success:
        raise RuntimeError(sol.message)
    Jk = sol.y[-1]
    pdf = np.clip((k / mu) * Jk, 0.0, None)
    return sol.t.tolist(), pdf.tolist()

ui.page_title('Linear-chain (gamma) delay — ECharts')

with ui.row().classes('w-full items-start'):
    # -------- controls --------
    with ui.card().classes('min-w-[320px] max-w-[420px]'):
        ui.label('Parameters').classes('text-lg font-medium')

        mu = ui.slider(min=1.0, max=15.0, value=5.0, step=0.1).props('label-always').classes('w-full')
        ui.label().bind_text_from(mu, 'value', backward=lambda v: f'μ (mean delay): {float(v):.2f}')

        k = ui.slider(min=1, max=20, value=10, step=1).props('label-always').classes('w-full')
        ui.label().bind_text_from(k, 'value', backward=lambda v: f'k (number of substages): {int(v)}')

        tmax = ui.slider(min=0.1, max=40.0, value=15.0, step=0.1).props('label-always').classes('w-full')
        ui.label().bind_text_from(tmax, 'value', backward=lambda v: f't_max (plot horizon): {float(v):.2f}')

        with ui.row():
            recompute = ui.button('Recompute')
            auto = ui.toggle(['auto']).props('color=primary')  # [] or ['auto']

        mean_label = ui.label()
        var_label = ui.label()

    # -------- chart --------
    with ui.card().classes('w-full'):
        ui.label('Distribution of delay r · J_k(t)').classes('text-lg font-medium')

        chart = ui.echart({
            'tooltip': {'trigger': 'axis'},
            'grid': {'left': 50, 'right': 20, 'top': 30, 'bottom': 40},
            'xAxis': {'type': 'value', 'name': 't'},
            'yAxis': {'type': 'value', 'name': 'density'},
            'series': [
                {'type': 'line', 'name': 'pdf', 'showSymbol': False, 'data': []},
                # area fill
                {'type': 'line', 'name': 'fill', 'showSymbol': False, 'areaStyle': {}, 'data': []},
            ],
        }).style('height:420px;width:100%')

def update_chart():
    mu_val = float(mu.value)
    k_val = int(k.value)
    tmax_val = float(tmax.value)

    mean_label.text = f'mean = μ = {mu_val:.4g}'
    var_label.text  = f'variance = μ / k = {mu_val/k_val:.4g}'

    tt, pdf = linear_chain(mu_val, k_val, tmax_val)
    data = [[tt[i], pdf[i]] for i in range(len(tt))]
    chart.options['series'][0]['data'] = data
    chart.options['series'][1]['data'] = data  # reuse for the area fill
    # keep axes nice
    chart.options['xAxis']['min'] = 0.0
    chart.options['xAxis']['max'] = tmax_val
    chart.update()

def maybe_auto(_):
    if 'auto' in (auto.value or []):
        update_chart()

for s in (mu, k, tmax):
    s.on_value_change(maybe_auto)

recompute.on('click', lambda: update_chart())

# initial render
update_chart()

ui.run(host='0.0.0.0', port=8080)
