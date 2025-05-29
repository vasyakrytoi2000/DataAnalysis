import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, CheckButtons, Button
from scipy.signal import butter, filtfilt

def filter(signal, cutoff_freq, fs):
    b, a = butter(N=4, Wn=cutoff_freq / (0.5 * fs))
    return filtfilt(b, a, signal)

# default params
amp = 1.0
freq = 0.5
phase = 1.0
noise_avg = 0.0
noise_vari = 0.1
fs = 1000

t = np.linspace(0.0, 2.0 * np.pi, fs)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.5)

# elements
ax_slider_freq = plt.axes([0.25, 0.38, 0.65, 0.03])
ax_slider_amp = plt.axes([0.25, 0.33, 0.65, 0.03])
ax_slider_phase = plt.axes([0.25, 0.28, 0.65, 0.03])
ax_slider_noise_avg = plt.axes([0.25, 0.23, 0.65, 0.03])
ax_slider_noise_vari = plt.axes([0.25, 0.18, 0.65, 0.03])
ax_slider_cutoff_freq = plt.axes([0.25, 0.13, 0.65, 0.03])

ax_checkbox_noise = plt.axes([0.04, 0.12, 0.1, 0.1])
ax_checkbox_filter = plt.axes([0.04, 0.24, 0.1, 0.1])
ax_button_reset = plt.axes([0.47, 0.03, 0.07, 0.05])

slider_freq = Slider(ax_slider_freq, 'Frequency', 0.1, 5.0, valinit=freq)
slider_amp = Slider(ax_slider_amp, 'Amplitude', 0.1, 5.0, valinit=amp)
slider_phase = Slider(ax_slider_phase, 'Phase', 0.0, 2 * np.pi, valinit=phase)
slider_noise_avg = Slider(ax_slider_noise_avg, 'Noise mean', -1.0, 1.0, valinit=noise_avg)
slider_noise_vari = Slider(ax_slider_noise_vari, 'Noise variance', 0.0, 1.0, valinit=noise_vari)
slider_cutoff_freq = Slider(ax_slider_cutoff_freq, 'Cutoff freq', 0.1, 20.0, valinit=2.0)

checkbox_noise = CheckButtons(ax_checkbox_noise, ['Noise'], [False])
checkbox_filter = CheckButtons(ax_checkbox_filter, ['Filter'], [False])
button_reset = Button(ax_button_reset, "Reset")

# noise 
_noise = np.random.normal(noise_avg, np.sqrt(noise_vari), len(t))
harmonic = amp * np.sin(2 * np.pi * freq * t + phase)

#lines
line_clean, = ax.plot(t, harmonic, lw=2, label="Harmonic", zorder=3)
line_with_noise, = ax.plot(t, harmonic + _noise, lw=2, color='hotpink', label="With Noise", zorder=2)
line_with_noise.set_visible(False)
line_filtered, = ax.plot(t, harmonic, lw=2, color='green', label="Filtered", zorder=4)
line_filtered.set_visible(False)

def update_harmonic(val=None):
    global _noise
    freq = slider_freq.val
    amp = slider_amp.val
    phase = slider_phase.val
    noise_mean = slider_noise_avg.val
    noise_var = slider_noise_vari.val
    cutoff = slider_cutoff_freq.val

    harmonic = amp * np.sin(2 * np.pi * freq * t + phase)

    noisy_signal = harmonic + _noise
    line_clean.set_ydata(harmonic)

    if checkbox_noise.get_status()[0]:
        line_with_noise.set_ydata(noisy_signal)
        line_with_noise.set_visible(True)
    else:
        line_with_noise.set_visible(False)

    if checkbox_filter.get_status()[0]:
        filtered_signal = filter(noisy_signal, cutoff, fs)
        line_filtered.set_ydata(filtered_signal)
        line_filtered.set_visible(True)
    else:
        line_filtered.set_visible(False)

    fig.canvas.draw_idle()

def update_noise(val=None):
    global _noise
    noise_mean = slider_noise_avg.val
    noise_var = slider_noise_vari.val
    cutoff = slider_cutoff_freq.val

    _noise = np.random.normal(noise_mean, np.sqrt(noise_var), len(t))
    noisy_signal = harmonic + _noise
    line_with_noise.set_ydata(noisy_signal)

    if checkbox_filter.get_status()[0]:
        filtered_signal = filter(noisy_signal, cutoff, fs)
        line_filtered.set_ydata(filtered_signal)
        line_filtered.set_visible(True)
    else:
        line_filtered.set_visible(False)

    fig.canvas.draw_idle()

def reset(event):
    slider_freq.reset()
    slider_amp.reset()
    slider_phase.reset()
    slider_noise_avg.reset()
    slider_noise_vari.reset()
    slider_cutoff_freq.reset()
    if checkbox_noise.get_status()[0]:
        checkbox_noise.set_active(0)
    if checkbox_filter.get_status()[0]:
        checkbox_filter.set_active(0)

slider_freq.on_changed(update_harmonic)
slider_amp.on_changed(update_harmonic)
slider_phase.on_changed(update_harmonic)
slider_noise_avg.on_changed(update_noise)
slider_noise_vari.on_changed(update_noise)
slider_cutoff_freq.on_changed(update_harmonic)

checkbox_noise.on_clicked(lambda label: update_harmonic())
checkbox_filter.on_clicked(lambda label: update_harmonic())

button_reset.on_clicked(reset)

plt.show()
