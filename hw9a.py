import matplotlib.pyplot as plt  # for plotting
from scipy.signal import lfilter, firwin
import numpy as np  # for sine function
import csv

# Import the CSV data
time_values = []  # column 0
signal_data = []  # column 1

with open('sigA.csv') as file:
    # Open the CSV file
    reader = csv.reader(file)
    for row in reader:
        # Read the rows one by one
        time_values.append(float(row[0]))  # leftmost column
        signal_data.append(float(row[1]))  # second column

# Implement FFT
sample_rate = len(time_values) / time_values[-1]  # sample rate = total number of samples / total time of samples
sampling_interval = 1.0 / sample_rate  # sampling interval
time_vector = np.arange(0, time_values[-1], sampling_interval)  # time vector
signal = signal_data  # data to make the FFT from
signal_length = len(signal)  # length of the signal
frequency_indices = np.arange(signal_length)
total_time = signal_length / sample_rate
frequency_range = frequency_indices / total_time  # two-sided frequency range
frequency_range = frequency_range[range(int(signal_length / 2))]  # one-sided frequency range
fft_result = np.fft.fft(signal) / signal_length  # FFT computation and normalization
fft_result = fft_result[range(int(signal_length / 2))]

# Plotting FFT
fig1, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(time_values, signal, 'b')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax1.set_title('Time Domain Signal')
ax2.loglog(frequency_range, abs(fft_result), 'b')  # plotting the FFT
ax2.set_xlabel('Freq [Hz]')
ax2.set_ylabel('|Y (freq)| [Amplitude]')
ax2.set_title('Frequency Domain Signal')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement moving average low-pass filter
data_array = signal_data
window_size = 50

i = 0
moving_averages = []

while i < len(data_array) - window_size + 1:
    if i < window_size - 1:
        moving_averages.append(0)
    window = data_array[i: i + window_size]
    window_average = round(sum(window) / window_size, 2)
    moving_averages.append(window_average)
    i += 1
moving_averages = list(moving_averages)

fft_filtered_result = np.fft.fft(moving_averages) / signal_length
fft_filtered_result = fft_filtered_result[range(int(signal_length / 2))]

fig2, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(time_values, signal, 'k', time_values, moving_averages, 'r')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax1.set_title('Time Domain Signal with Moving Average')
ax2.loglog(frequency_range, abs(fft_result), 'k', frequency_range, abs(fft_filtered_result), 'r')
ax2.set_xlabel('Freq [Hz]')
ax2.set_ylabel('|Y (freq)| [Amplitude]')
ax2.set_title('Frequency Domain Signal with Moving Average Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement IIR Filter
filtered_data = []
A = 0.90
B = 0.1

for data_point in signal_data:
    if len(filtered_data) == 0:
        filtered_data.append(0)
    else:
        filtered_data.append(filtered_data[-1] * A + data_point * B)

fft_iir_result = np.fft.fft(filtered_data) / signal_length
fft_iir_result = fft_iir_result[range(int(signal_length / 2))]

fig3, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(time_values, signal, 'k', time_values, filtered_data, 'r')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax1.set_title('Time Domain Signal with IIR Filter')
ax2.loglog(frequency_range, abs(fft_result), 'k', frequency_range, abs(fft_iir_result), 'r')
ax2.set_xlabel('Freq [Hz]')
ax2.set_ylabel('|Y(freq)| [Amplitude]')
ax2.set_title('Frequency Domain Signal with IIR Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement FIR Filter
nyquist_rate = sample_rate / 2.  # Nyquist rate of the signal (highest discernable frequency)
cutoff_frequency = 60  # Cutoff Frequency
filter_length = 49  # Length of the filter = (# of Coeffs / the filter order + 1)

# Use firwin to create a lowpass FIR filter
firwin_coefficients = firwin(filter_length, cutoff_frequency / nyquist_rate)

# Use lfilter to filter the signal with the FIR filter
filtered_signal = lfilter(firwin_coefficients, 1.0, signal_data)

fft_fir_result = np.fft.fft(filtered_signal) / signal_length
fft_fir_result = fft_fir_result[range(int(signal_length / 2))]

fig4, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(time_values, signal, 'k', time_values, filtered_signal, 'r')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax1.set_title('Time Domain Signal with FIR Filter')
ax2.loglog(frequency_range, abs(fft_result), 'k', frequency_range, abs(fft_fir_result), 'r')
ax2.set_xlabel('Freq [Hz]')
ax2.set_ylabel('|Y (freq)| [Amplitude]')
ax2.set_title('Frequency Domain Signal with FIR Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
