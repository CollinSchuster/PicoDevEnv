import matplotlib.pyplot as plt  # for plotting
from scipy.signal import lfilter, firwin
import numpy as np  # for sine function
import csv

# Import the CSV data
time_values_d = []  # column 0
data1 = []  # column 1

with open('sigD.csv') as file_d:
    # Open the CSV file
    reader_d = csv.reader(file_d)
    for row_d in reader_d:
        # Read the rows one by one
        time_values_d.append(float(row_d[0]))  # leftmost column
        data1.append(float(row_d[1]))  # second column

# Implement FFT
sample_rate_d = len(time_values_d) / time_values_d[-1]  # sample rate = total number of samples / total time of samples
sampling_interval_d = 1.0 / sample_rate_d  # sampling interval
time_vector_d = np.arange(0, time_values_d[-1], sampling_interval_d)  # time vector
signal_d = data1  # data to make the FFT from
signal_length_d = len(signal_d)  # length of the signal
frequency_indices_d = np.arange(signal_length_d)
total_time_d = signal_length_d / sample_rate_d
frequency_range_d = frequency_indices_d / total_time_d  # two-sided frequency range
frequency_range_d = frequency_range_d[range(int(signal_length_d / 2))]  # one-sided frequency range
fft_result_d = np.fft.fft(signal_d) / signal_length_d  # FFT computation and normalization
fft_result_d = fft_result_d[range(int(signal_length_d / 2))]

# Plotting FFT
fig1_d, (ax1_d, ax2_d) = plt.subplots(2, 1)
ax1_d.plot(time_values_d, signal_d, 'b')
ax1_d.set_xlabel('Time [s]')
ax1_d.set_ylabel('Amplitude')
ax1_d.set_title('Time Domain Signal')
ax2_d.loglog(frequency_range_d, abs(fft_result_d), 'b')  # plotting the FFT
ax2_d.set_xlabel('Freq (Hz)')
ax2_d.set_ylabel('|Y (freq)| [Amplitude]')
ax2_d.set_title('Frequency Domain Signal')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement moving average low-pass filter
data_array_d = data1
window_size_d = 50
i_d = 0

moving_averages_d = []  # Initialize an empty list to store moving averages
  
# Loop through the array to consider every window of size 50
while i_d < len(data_array_d) - window_size_d + 1:
    if i_d < window_size_d - 1:
        moving_averages_d.append(0)
    window_d = data_array_d[i_d : i_d + window_size_d]
    window_average_d = round(sum(window_d) / window_size_d, 2)
    moving_averages_d.append(window_average_d)
    i_d += 1
moving_averages_d = list(moving_averages_d)

fft_filtered_result_d = np.fft.fft(moving_averages_d) / signal_length_d
fft_filtered_result_d = fft_filtered_result_d[range(int(signal_length_d / 2))]

fig2_d, (ax1_d, ax2_d) = plt.subplots(2, 1)
ax1_d.plot(time_values_d, signal_d, 'k', time_values_d, moving_averages_d, 'r')
ax1_d.set_xlabel('Time [s]')
ax1_d.set_ylabel('Amplitude')
ax1_d.set_title('Time Domain Signal with Moving Average')
ax2_d.loglog(frequency_range_d, abs(fft_result_d), 'k', frequency_range_d, abs(fft_filtered_result_d), 'r')
ax2_d.set_xlabel('Freq (Hz)')
ax2_d.set_ylabel('|Y (freq)| [Amplitude]')
ax2_d.set_title('Frequency Domain Signal with Moving Average Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement IIR Filter
filtered_data_d = []
A_d = 0.90
B_d = 0.1

for data_point_d in data1:
    if len(filtered_data_d) == 0:
        filtered_data_d.append(0)
    else:
        filtered_data_d.append(filtered_data_d[-1] * A_d + data_point_d * B_d)

fft_iir_result_d = np.fft.fft(filtered_data_d) / signal_length_d
fft_iir_result_d = fft_iir_result_d[range(int(signal_length_d / 2))]

fig3_d, (ax1_d, ax2_d) = plt.subplots(2, 1)
ax1_d.plot(time_values_d, signal_d, 'k', time_values_d, filtered_data_d, 'r')
ax1_d.set_xlabel('Time [s]')
ax1_d.set_ylabel('Amplitude')
ax1_d.set_title('Time Domain Signal with IIR Filter')
ax2_d.loglog(frequency_range_d, abs(fft_result_d), 'k', frequency_range_d, abs(fft_iir_result_d), 'r')
ax2_d.set_xlabel('Freq (Hz)')
ax2_d.set_ylabel('|Y (freq)| [Amplitude]')
ax2_d.set_title('Frequency Domain Signal with IIR Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement FIR Filter
nyq_rate_d = sample_rate_d / 2. # Nyquist rate

# The cutoff frequency of the filter
cutoff_hz_d = 60

# Length of the filter (number of coefficients, i.e. the filter order + 1)
len_filt_d = 49

# Use firwin to create a lowpass FIR filter
fir_coeff_d = firwin(len_filt_d, cutoff_hz_d / nyq_rate_d)

# Use lfilter to filter the signal with the FIR filter
filtered_signal_d = lfilter(fir_coeff_d, 1.0, data1)

fft_fir_result_d = np.fft.fft(filtered_signal_d) / signal_length_d
fft_fir_result_d = fft_fir_result_d[range(int(signal_length_d / 2))]

fig4_d, (ax1_d, ax2_d) = plt.subplots(2, 1)
ax1_d.plot(time_values_d, signal_d, 'k', time_values_d, filtered_signal_d, 'r')
ax1_d.set_xlabel('Time [s]')
ax1_d.set_ylabel('Amplitude')
ax1_d.set_title('Time Domain Signal with FIR Filter')
ax2_d.loglog(frequency_range_d, abs(fft_result_d), 'k', frequency_range_d, abs(fft_fir_result_d), 'r')
ax2_d.set_xlabel('Freq (Hz)')
ax2_d.set_ylabel('|Y (freq)| [Amplitude]')
ax2_d.set_title('Frequency Domain Signal with FIR Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
