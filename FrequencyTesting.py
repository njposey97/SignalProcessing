"""
This program shows that a step function has a constant frequency of amplitude 1
Therefore, if this signal is plotted on the spectrum, it should be equivalent to a vertical line
"""

#https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter


import numpy as np
import matplotlib.pyplot as plt

Fs = 44100

x = [0] + [1]  + [0] * (Fs-1)
t = 1

def plot_spectrum(signal):
    N = Fs*t
    Y_k = np.fft.fft(signal)[0:int(N/2)]/N # FFT function from numpy
    Y_k[1:] = 2*Y_k[1:] # need to take the single-sided spectrum only
    Pxx = np.abs(Y_k) * 22050# be sure to get rid of imaginary part
    f = (Fs*np.arange((N/2))/N); # frequency vector
    plt.plot(f,Pxx)
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency [Hz]')
    plt.show()

plot_spectrum(x)


#The next step within this program is to determine a method for cutting specific frequencies
#This can potentially be solved be a band-pass filter implementation

"""

from scipy.signal import butter, lfilter, freqz

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Sample rate and desired cutoff frequencies (in Hz).
fs = 5000.0
lowcut = 500.0
highcut = 1500.0
order = 6

# Filter a noisy signal.
T = 0.05
nsamples = T * fs
t = np.linspace(0, T, int(nsamples), endpoint=False)
a = 0.02
f0 = 600.0
x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
x += a * np.cos(2 * np.pi * f0 * t + .11)
x += 0.03 * np.cos(2 * np.pi * 2000 * t)
plt.figure(2)
plt.clf()
plt.plot(t, x, label='Noisy signal')

y = butter_bandpass_filter(x, lowcut, highcut, fs, order=6)
plt.plot(t, y, label='Filtered signal (%g Hz)' % f0)
plt.xlabel('time (seconds)')
plt.hlines([-a, a], 0, T, linestyles='--')
plt.grid(True)
plt.axis('tight')
plt.legend(loc='upper left')

plt.show()
"""
