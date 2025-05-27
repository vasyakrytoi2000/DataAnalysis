from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Slider, CheckboxGroup, Button, ColumnDataSource, Div, Select
from bokeh.plotting import figure
import numpy as np
from scipy.signal import butter, filtfilt

fs = 1000
t = np.linspace(0.0, 2.0 * np.pi, fs)

# default params
initials = {
    "amp": 1.0,
    "freq": 0.5,
    "phase": 1.0,
    "noise_mean": 0.0,
    "noise_vari": 0.1,
    "cutoff": 2.0,
    "ma_window": 10
}

# filter
def low_filter(signal, cutoff_freq, fs):
    b, a = butter(N=4, Wn=cutoff_freq / (0.5 * fs))
    return filtfilt(b, a, signal)

def moving_average_filter(signal, window_size):
    window_size = max(1, int(window_size))
    cumsum = np.cumsum(np.insert(signal, 0, 0))
    filtered = (cumsum[window_size:] - cumsum[:-window_size]) / window_size
    prefix = signal[:window_size-1]
    return np.concatenate([prefix, filtered])

source = ColumnDataSource(data=dict(
    t=t,
    harmonic=np.zeros_like(t),
    noise=np.zeros_like(t),
    noisy=np.zeros_like(t),
    filtered=np.zeros_like(t)
))

# noise
_noise = np.random.normal(initials["noise_mean"], np.sqrt(initials["noise_vari"]), len(t))

# elements
plot2 = figure(title="Harmonic with noise and filter", height=250, width=600)
harm2 = plot2.line('t', 'harmonic', source=source, line_width=2, color="blue")
noise_line = plot2.line('t', 'noisy', source=source, line_width=2, color="hotpink")
filt_line = plot2.line('t', 'filtered', source=source, line_width=2, color="green")

plot3 = figure(title="Noise and filter", height=250, width=600)
noise_only_line = plot3.line('t', 'noisy', source=source, line_width=2, color="hotpink")
filt_only_line = plot3.line('t', 'filtered', source=source, line_width=2, color="green")

slider_amp = Slider(start=0.1, end=5.0, value=initials["amp"], step=0.1, title="Amplitude")
slider_freq = Slider(start=0.1, end=5.0, value=initials["freq"], step=0.1, title="Frequency")
slider_phase = Slider(start=0.0, end=2*np.pi, value=initials["phase"], step=0.1, title="Phase")
slider_noise_mean = Slider(start=-1.0, end=1.0, value=initials["noise_mean"], step=0.1, title="Noise mean")
slider_noise_vari = Slider(start=0.0, end=1.0, value=initials["noise_vari"], step=0.01, title="Noise variance")
slider_cutoff = Slider(start=0.1, end=20.0, value=initials["cutoff"], step=0.1, title="Cutoff frequency")
slider_ma_window = Slider(start=3, end=100, value=initials["ma_window"], step=1, title="MA Window Size")

checkboxes = CheckboxGroup(labels=["Add Noise", "Apply Filter"], active=[])
button_reset = Button(label="Reset", button_type="warning")

select_filter = Select(title="Select Filter", value="Butterworth", options=["Butterworth", "Moving Average"])

def update_harmonic():
    amp = slider_amp.value
    freq = slider_freq.value
    phase = slider_phase.value
    cutoff = slider_cutoff.value
    ma_window = slider_ma_window.value
    selected_filter = select_filter.value

    harmonic = amp * np.sin(2 * np.pi * freq * t + phase)
    noisy_signal = harmonic + _noise

    if 1 in checkboxes.active:
        if selected_filter == "Butterworth":
            filtered_signal = low_filter(noisy_signal, cutoff, fs)
        elif selected_filter == "Moving Average":
            filtered_signal = moving_average_filter(noisy_signal, ma_window)
        else:
            filtered_signal = noisy_signal
    else:
        filtered_signal = noisy_signal

    source.data.update({
        'harmonic': harmonic,
        'noisy': noisy_signal,
        'filtered': filtered_signal
    })

    noise_visible = 0 in checkboxes.active
    filter_visible = 1 in checkboxes.active

    noise_line.visible = noise_visible
    noise_only_line.visible = noise_visible
    filt_line.visible = filter_visible
    filt_only_line.visible = filter_visible

def update_noise():
    global _noise
    noise_mean = slider_noise_mean.value
    noise_vari = slider_noise_vari.value
    cutoff = slider_cutoff.value
    ma_window = slider_ma_window.value
    selected_filter = select_filter.value

    _noise = np.random.normal(noise_mean, np.sqrt(noise_vari), len(t))
    harmonic = source.data['harmonic']
    noisy_signal = harmonic + _noise

    if 1 in checkboxes.active:
        if selected_filter == "Butterworth":
            filtered_signal = low_filter(noisy_signal, cutoff, fs)
        elif selected_filter == "Moving Average":
            filtered_signal = moving_average_filter(noisy_signal, ma_window)
        else:
            filtered_signal = noisy_signal
    else:
        filtered_signal = noisy_signal

    source.data.update({
        'noise': _noise,
        'noisy': noisy_signal,
        'filtered': filtered_signal
    })

    noise_visible = 0 in checkboxes.active
    filter_visible = 1 in checkboxes.active

    noise_line.visible = noise_visible
    noise_only_line.visible = noise_visible
    filt_line.visible = filter_visible
    filt_only_line.visible = filter_visible

def update_ma_slider_visibility(attr, old, new):
    if select_filter.value == "Moving Average":
        slider_ma_window.visible = True
        slider_cutoff.visible = False
    else:
        slider_ma_window.visible = False
        slider_cutoff.visible = True

for slider in [slider_amp, slider_freq, slider_phase, slider_cutoff, slider_ma_window]:
    slider.on_change('value', lambda attr, old, new: update_harmonic())

slider_noise_mean.on_change('value', lambda attr, old, new: update_noise())
slider_noise_vari.on_change('value', lambda attr, old, new: update_noise())

checkboxes.on_change('active', lambda attr, old, new: update_harmonic())
select_filter.on_change('value', lambda attr, old, new: (update_ma_slider_visibility(attr, old, new), update_harmonic()))

def reset_all():
    global _noise
    slider_amp.value = initials["amp"]
    slider_freq.value = initials["freq"]
    slider_phase.value = initials["phase"]
    slider_noise_mean.value = initials["noise_mean"]
    slider_noise_vari.value = initials["noise_vari"]
    slider_cutoff.value = initials["cutoff"]
    slider_ma_window.value = initials["ma_window"]
    checkboxes.active = []
    select_filter.value = "Butterworth"
    update_ma_slider_visibility(None, None, None)
    _noise = np.random.normal(slider_noise_mean.value, np.sqrt(slider_noise_vari.value), len(t))
    update_noise()
    update_harmonic()

button_reset.on_click(reset_all)

# start
update_ma_slider_visibility(None, None, None)

update_noise()
update_harmonic()

controls = column(slider_amp, slider_freq, slider_phase,
                  slider_noise_mean, slider_noise_vari,
                  slider_cutoff, slider_ma_window, select_filter,
                  checkboxes, button_reset)

layout = column(
    Div(text="<h2>Bokeh garmonicaaaaaaaa</h2>"),
    row(controls, column(plot2, plot3))
)

curdoc().add_root(layout)
curdoc().title = "Harmonic Signal with Noise and Filtering"
