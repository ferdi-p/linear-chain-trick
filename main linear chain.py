from nicegui import ui
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ---- math ----
def linear_chain_pdf(mu: float, k: int, tmax: float, npts: int = 600):
    r = k / mu
    def rhs(t, y):
        dy = np.empty_like(y)
        dy[0] = r * (0.0 - y[0])
        dy[1:] = r * (y[:-1] - y[1:])
        return dy

    y0 = np.zeros(k)
    y0[0] = 1.0
    t_eval = np.linspace(0.0, float(tmax), int(npts))
    sol = solve_ivp(rhs, (0.0, float(tmax)), y0, t_eval=t_eval, rtol=1e-7, atol=1e-9, method='LSODA')
    if not sol.success:
        raise RuntimeError(sol.message)
    Jk = sol.y[-1]
    pdf = np.clip((k / mu) * Jk, 0.0, None)
    return sol.t, pdf

ui.page_title('Linear-chain (gamma) delay demo')

with ui.row().classes('w-full items-start'):
    # -------- controls --------
    with ui.card().classes('min-w-[320px] max-w-[420px]'):
        ui.label('Parameters').classes('text-lg font-medium')

        mu_slider = ui.slider(min=1.0, max=15.0, value=5.0, step=0.1).props('label-always').classes('w-full')
        ui.label().bind_text_from(mu_slider, 'value', backward=lambda v: f'μ (mean delay): {v:.2f}')

        k_slider = ui.slider(min=1, max=20, value=10, step=1).props('label-always').classes('w-full')
        ui.label().bind_text_from(k_slider, 'value', backward=lambda v: f'k (number of substages): {int(v)}')

        tmax_slider = ui.slider(min=0.001, max=40.0, value=15.0, step=0.1).props('label-always').classes('w-full')
        ui.label().bind_text_from(tmax_slider, 'value', backward=lambda v: f't_max (plot horizon): {v:.2f}')

        with ui.row():
            recompute_btn = ui.button('Recompute')
            auto_toggle = ui.toggle(['auto']).props('color=primary')  # [] or ['auto']

        mean_label = ui.label()
        var_label = ui.label()

    # -------- plot --------
    with ui.card().classes('w-full'):
        ui.label('Distribution of delay r · J_k(t)').classes('text-lg font-medium')

        # Create ONE persistent figure/axes and bind to the ui element
        fig, ax = plt.subplots()
        ax.set_xlabel('t')
        ax.set_ylabel('density')
        ax.set_title('Distribution of delay')

        plot = ui.pyplot().classes('w-full')
        plot.figure = fig        # bind the matplotlib figure
        plot.update()            # initial render

# -------- update logic --------
def update_plot(*_):
    mu = float(mu_slider.value)
    k = int(k_slider.value)
    tmax = float(tmax_slider.value)

    mean_label.text = f'mean = μ = {mu:.4g}'
    var_label.text = f'variance = μ / k = {mu/k:.4g}'

    t, pdf = linear_chain_pdf(mu, k, tmax)

    # redraw on the SAME axes
    ax.clear()
    ax.plot(t, pdf)
    ax.fill_between(t, pdf, alpha=0.3)
    ax.set_xlabel('t')
    ax.set_ylabel('density')
    ax.set_title('Distribution of delay')
    ax.set_xlim(0.0, tmax)
    plot.update()               # refresh the canvas

# auto-update when sliders move (if toggle is on)
def maybe_auto(_):
    if 'auto' in (auto_toggle.value or []):
        update_plot()

for s in (mu_slider, k_slider, tmax_slider):
    s.on_value_change(maybe_auto)

recompute_btn.on('click', update_plot)

# initial draw
update_plot()

ui.run(host='0.0.0.0', port=8080)
