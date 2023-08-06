import ipywidgets as widgets
from IPython.display import display, clear_output
import math

# Dictionaries for dropdown options
av_values = {
    'Network': 0.85,
    'Adjacent': 0.62,
    'Local': 0.55,
    'Physical': 0.2
}
ac_values = {
    'High': 0.44,
    'Low': 0.77
}
pr_values = {
    'None': 0.85,
    'Low': 0.62,
    'High': 0.27
}
ui_values = {
    'None': 0.85,
    'Required': 0.62
}
s_values = ['Unchanged', 'Changed']
c_values = {
    'None': 0,
    'Low': 0.22,
    'High': 0.56
}
i_values = {
    'None': 0,
    'Low': 0.22,
    'High': 0.56
}
a_values = {
    'None': 0,
    'Low': 0.22,
    'High': 0.56
}

# Define labels separately from dropdowns to ensure enough space for description
av_label = widgets.Label('AV - Attack Vector')
av_dropdown = widgets.Dropdown(options=av_values.keys(), value=list(av_values.keys())[0])

ac_label = widgets.Label('AC - Attack Complexity')
ac_dropdown = widgets.Dropdown(options=ac_values.keys(), value=list(ac_values.keys())[0])

pr_label = widgets.Label('PR - Privileges Required')
pr_dropdown = widgets.Dropdown(options=pr_values.keys(), value=list(pr_values.keys())[0])

ui_label = widgets.Label('UI - User Interaction')
ui_dropdown = widgets.Dropdown(options=ui_values.keys(), value=list(ui_values.keys())[0])

s_label = widgets.Label('S - Scope')
s_dropdown = widgets.Dropdown(options=s_values, value=s_values[0])

c_label = widgets.Label('C - Confidentiality')
c_dropdown = widgets.Dropdown(options=c_values.keys(), value=list(c_values.keys())[0])

i_label = widgets.Label('I - Integrity')
i_dropdown = widgets.Dropdown(options=i_values.keys(), value=list(i_values.keys())[0])

a_label = widgets.Label('A - Availability')
a_dropdown = widgets.Dropdown(options=a_values.keys(), value=list(a_values.keys())[0])

# Use HTML widget for displaying results
big_text_style = '<style> .big_text { font-size: 20px; } </style>'
iss_field = widgets.HTML(value=big_text_style + '<span class="big_text"><strong>ISS:</strong> {}</span>'.format(0))
imp_field = widgets.HTML(value=big_text_style + '<span class="big_text"><strong>Impact (Imp):</strong> {}</span>'.format(0))
expl_field = widgets.HTML(value=big_text_style + '<span class="big_text"><strong>Exploitability (Expl):</strong> {}</span>'.format(0))
bs_field = widgets.HTML(value=big_text_style + '<span class="big_text"><strong>BaseScore (BS):</strong> {}</span>'.format(0))


# Calculation function
def calculate_metrics(change):
    # Compute ISS
    ISS = 1 - ((1-c_values[c_dropdown.value])*(1-i_values[i_dropdown.value])*(1-a_values[a_dropdown.value]))
    
    # Compute Impact (Imp)
    if s_dropdown.value == 'Unchanged':
        Imp = 6.42 * ISS
    else:
        Imp = 7.52 * (ISS-0.029) - 3.25 * math.pow(ISS, 15)
    
    # Compute Exploitability (Expl)
    Expl = 8.22 * av_values[av_dropdown.value] * ac_values[ac_dropdown.value] * pr_values[pr_dropdown.value] * ui_values[ui_dropdown.value]
    
    # not really sure how this is calculated...
    # Compute BaseScore (BS)
    if Imp == 0:
        BS = 0
    elif s_dropdown.value == 'Unchanged':
        BS = min(Imp + Expl, 10)
    else:
        BS = min(1.08*(Imp + Expl), 10)
    
    BS = round(BS, 2)  # Rounding to 2 decimal places
    
    # Update text fields
    iss_field.value = '<strong>ISS:</strong> {}'.format(round(ISS, 2))
    imp_field.value = '<strong>Impact (Imp):</strong> {}'.format(round(Imp, 2))
    expl_field.value = '<strong>Exploitability (Expl):</strong> {}'.format(round(Expl, 2))
    bs_field.value = '<strong>BaseScore (BS):</strong> {}'.format(round(BS, 2))


# Add observe to each dropdown for real-time update
dropdowns = [av_dropdown, ac_dropdown, pr_dropdown, ui_dropdown, s_dropdown, c_dropdown, i_dropdown, a_dropdown]
for dropdown in dropdowns:
    dropdown.observe(calculate_metrics, names='value')

# Initial calculation
calculate_metrics(None)

separator = widgets.HTML(value="<hr>")

# Display widgets with labels alongside for clear descriptions
display_widgets = widgets.VBox([
    widgets.HBox([av_label, av_dropdown]),
    widgets.HBox([ac_label, ac_dropdown]),
    widgets.HBox([pr_label, pr_dropdown]),
    widgets.HBox([ui_label, ui_dropdown]),
    widgets.HBox([s_label, s_dropdown]),
    widgets.HBox([c_label, c_dropdown]),
    widgets.HBox([i_label, i_dropdown]),
    widgets.HBox([a_label, a_dropdown]),
    separator,
    iss_field, imp_field, expl_field, bs_field
])

display(display_widgets)