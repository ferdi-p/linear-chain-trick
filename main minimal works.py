from nicegui import ui
import numpy as np

ui.page_title('y = c · x')

# --- controls ---
with ui.card():
    ui.label('Set c')
    c_slider = ui.slider(min=0.0, max=5.0, value=1.0, step=0.1).props('label-always')
    ui.label().bind_text_from(c_slider, 'value', backward=lambda v: f'c = {float(v):.2f}')

# --- data & chart ---
x = np.linspace(0.0, 10.0, 101).tolist()

def series_data(c: float):
    return [[xi, xi * c] for xi in x]

chart = ui.echart({
    'tooltip': {'trigger': 'axis'},
    'xAxis': {'type': 'value', 'name': 'x'},
    'yAxis': {'type': 'value', 'name': 'y'},
    'series': [{
        'type': 'line',
        'showSymbol': False,
        'data': series_data(float(c_slider.value)),
    }],
}).classes('w-full')

def update_chart(_=None):
    c = float(c_slider.value)
    chart.options['series'][0]['data'] = series_data(c)
    chart.update()

c_slider.on_value_change(update_chart)

ui.run(host='0.0.0.0', port=8080)