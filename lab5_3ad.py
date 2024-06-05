import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Button, CheckboxGroup, Select
from bokeh.plotting import figure

# Функція для генерації сигналу
def harmonic(t, amplitude, frequency, phase):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

# Функція для генерації шуму
def create_noise(t, noise_mean, noise_covariance):
    return np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))

# Функція для комбінації сигналу і шуму
def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, noise=None):
    harmonic_signal = harmonic(t, amplitude, frequency, phase)
    if noise is not None:
        return harmonic_signal + noise
    else:
        noise = create_noise(t, noise_mean, noise_covariance)
        if show_noise:
            return harmonic_signal + noise
        else:
            return harmonic_signal

# Функція для власного фільтра
def custom_filter(signal, window_size):
    filtered_signal = np.convolve(signal, np.ones(window_size)/window_size, mode='valid')
    return np.pad(filtered_signal, (window_size - 1, 0), 'constant', constant_values=(signal[0],))

# Початкові параметри
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
initial_window_size = 5

t = np.arange(0.0, 10.0, 0.01)
signal = harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase,
                             initial_noise_mean, initial_noise_covariance, True)

source_signal = ColumnDataSource(data=dict(t=t, signal=signal))
source_filtered = ColumnDataSource(data=dict(t=t, filtered_signal=np.zeros_like(signal)))

plot_signal = figure(title="Початковий графік сигналу", height=300, width=600, y_range=(-3, 3))
plot_signal.line('t', 'signal', source=source_signal, line_width=3, line_alpha=0.6, color='green')

plot_filtered = figure(title="Графік сигналу з власним фільтром", height=300, width=600, y_range=(-3, 3))
plot_filtered.line('t', 'filtered_signal', source=source_filtered, line_width=3, line_alpha=0.6, color='purple')

amplitude_slider = Slider(start=0.1, end=10.0, value=initial_amplitude, step=0.1, title="Amplitude")
frequency_slider = Slider(start=0.1, end=10.0, value=initial_frequency, step=0.1, title="Frequency")
phase_slider = Slider(start=0, end=2*np.pi, value=initial_phase, step=0.1, title="Phase")
noise_mean_slider = Slider(start=-1.0, end=1.0, value=initial_noise_mean, step=0.1, title="Noise Mean")
noise_covariance_slider = Slider(start=0.0, end=1.0, value=initial_noise_covariance, step=0.01, title="Noise Covariance")
window_size_slider = Slider(start=1, end=50, value=initial_window_size, step=1, title="Window size")

show_noise_checkbox = CheckboxGroup(labels=["Show noise"], active=[0])

def update_data(attrname, old, new):
    new_signal = harmonic_with_noise(t, amplitude_slider.value, frequency_slider.value, phase_slider.value,
                                     noise_mean_slider.value, noise_covariance_slider.value, 0 in show_noise_checkbox.active)
    source_signal.data = dict(t=t, signal=new_signal)
    
    new_filtered_signal = custom_filter(new_signal, int(window_size_slider.value))
    source_filtered.data = dict(t=t, filtered_signal=new_filtered_signal)

for widget in [amplitude_slider, frequency_slider, phase_slider, noise_mean_slider, noise_covariance_slider, window_size_slider]:
    widget.on_change('value', update_data)

def show_noise_checkbox_changed(attrname, old, new):
    update_data(None, None, None)

show_noise_checkbox.on_change('active', show_noise_checkbox_changed)

controls = column(amplitude_slider, frequency_slider, phase_slider, noise_mean_slider, noise_covariance_slider,
                  window_size_slider, show_noise_checkbox)

curdoc().add_root(row(column(plot_signal, plot_filtered), controls))
curdoc().title = "Графіки сигналу з власним фільтром"