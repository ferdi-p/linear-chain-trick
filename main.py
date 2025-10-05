from nicegui import ui
from model import linear_chain
from content import background_markdown
from ui_helpers import section_header, divider, param_row, build_info_dialog, header_with_info, make_echart_card

ui.page_title('Linear-chain (gamma) delay — ECharts')

info_dialog, open_info = build_info_dialog(background_markdown())
header_with_info('Linear-chain (gamma) delay demo', open_info)

with ui.element('div').classes('flex flex-col md:flex-row gap-6 p-6 w-full max-w-[1800px] mx-auto'):
    with ui.card().classes('w-full md:w-[420px] shrink-0 shadow-md p-6'):
        section_header('Parameters').classes('mb-4')

        mu, _ = param_row('Mean delay μ', min=1.0, max=15.0, value=5.0, step=0.1, fmt=lambda v: f'{v:.2f}')
        divider()
        k, _ = param_row('Number of sub-stages k', min=1, max=20, value=10, step=1, fmt=lambda v: f'{int(v)}')
        divider()
        section_header('Properties of the delay').classes('mb-2')
        mean_label = ui.label().classes('mt-1')
        var_label  = ui.label().classes('text-gray-600')

    chart = make_echart_card('Distribution of delay r · Jₖ(t)', height='70vh')

def update_chart(_=None):
    mu_val = float(mu.value)
    k_val = int(k.value)
    tmax_val = 10.0
    mean_label.text = f'mean = μ = {mu_val:.4g}'
    var_label.text  = f'variance = μ / k = {mu_val/k_val:.4g}'
    t, pdf = linear_chain(mu_val, k_val, tmax=tmax_val)
    data = [[t[i], pdf[i]] for i in range(len(t))]
    chart.options['series'][0]['data'] = data
    chart.options['series'][1]['data'] = data
    chart.options['xAxis']['max'] = tmax_val
    chart.update()

for w in (mu, k):
    w.on('change', update_chart)

update_chart()
ui.run(host='0.0.0.0', port=8080)
