import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, lfilter

# Функція для генерації сигналу
def harmonic(t, amplitude, frequency, phase):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

# Функція для генерації шуму
def create_noise(t, noise_mean, noise_covariance):
    return np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))

# Функція для комбінації сигналу і шуму
noise_g = None
noise_g_mean = None
noise_g_covariance = None

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, noise=None):
    global noise_g, noise_g_mean, noise_g_covariance
    harmonic_signal = harmonic(t, amplitude, frequency, phase)
    if noise is not None:
        return harmonic_signal + noise
    else:
        if noise_g is None or len(noise_g) != len(t) or noise_mean != noise_g_mean or noise_covariance != noise_g_covariance:
            noise_g = create_noise(t, noise_mean, noise_covariance)
            noise_g_mean = noise_mean
            noise_g_covariance = noise_covariance
        if show_noise:
            return harmonic_signal + noise_g
        else:
            return harmonic_signal

# Функція для фільтрації сигналу
def lowpass_filter(signal, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, signal)

# Початкові параметри
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
initial_cutoff_frequency = 1.0

t = np.arange(0.0, 10.0, 0.01)
sampling_frequency = len(t) / (t[-1] - t[0])

fig, ax = plt.subplots(2, figsize=(8, 6))
plt.subplots_adjust(left=0.1, bottom=0.4, hspace=0.5)

# Малюємо початковий графік
ax[0].set_title('Graph of harmonic with noise')
harmonic_line, = ax[0].plot(t, harmonic(t, initial_amplitude, initial_frequency, initial_phase), lw=2, color='green')
with_noise_line, = ax[0].plot(t, harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase, initial_noise_mean, initial_noise_covariance, True), lw=2, color='green')
ax[1].set_title('Filtered harmonic')
l_filtered, = ax[1].plot(t, harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase, initial_noise_mean, initial_noise_covariance, True), lw=2, color='purple')

# Створюємо слайдери
axcolor = 'lightgoldenrodyellow'
ax_amplitude = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_frequency = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_noise_mean = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_noise_covariance = plt.axes([0.1, 0.0, 0.65, 0.03], facecolor=axcolor)
ax_cutoff_frequency = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=axcolor)

s_amplitude = Slider(ax_amplitude, 'Amplitude', 0.1, 10.0, valinit=initial_amplitude)
s_frequency = Slider(ax_frequency, 'Frequency', 0.1, 10.0, valinit=initial_frequency)
s_phase = Slider(ax_phase, 'Phase', 0.0, 2 * np.pi, valinit=initial_phase)
s_noise_mean = Slider(ax_noise_mean, 'Noise Mean', -1.0, 1.0, valinit=initial_noise_mean)
s_noise_covariance = Slider(ax_noise_covariance, 'Noise Covariance', 0.0, 1.0, valinit=initial_noise_covariance)
s_cutoff_frequency = Slider(ax_cutoff_frequency, 'Cutoff Frequency', 0.1, 5.0, valinit=initial_cutoff_frequency)

# Функція для оновлення графіку
def update(val):
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val
    noise_mean = s_noise_mean.val
    noise_covariance = s_noise_covariance.val
    show_noise = cb_show_noise.get_status()[0]

    harmonic_line.set_ydata(harmonic(t, amplitude, frequency, phase))
    with_noise_line.set_ydata(harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise))

    cutoff_frequency = s_cutoff_frequency.val
    filtered_signal = lowpass_filter(with_noise_line.get_ydata(), cutoff_frequency, sampling_frequency)
    l_filtered.set_ydata(filtered_signal)

    fig.canvas.draw_idle()

# Призначаємо функцію оновлення слайдерам
s_amplitude.on_changed(update)
s_frequency.on_changed(update)
s_phase.on_changed(update)
s_noise_mean.on_changed(update)
s_noise_covariance.on_changed(update)
s_cutoff_frequency.on_changed(update)

# Додамо чекбокс для перемикання шуму
rax = plt.axes([0.8, 0.1, 0.1, 0.04], facecolor=axcolor)
cb_show_noise = CheckButtons(rax, ('Show Noise',), (True,))
cb_show_noise.on_clicked(update)

# Додамо кнопку для скидання параметрів
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    s_amplitude.reset()
    s_frequency.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_covariance.reset()
    s_cutoff_frequency.reset()
    global noise_g, noise_g_mean, noise_g_covariance
    noise_g = None
    noise_g_mean = None
    noise_g_covariance = None
    update(None)

button.on_clicked(reset)

plt.show()