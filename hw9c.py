import matplotlib.pyplot as plt  # for plotting
from scipy.signal import lfilter, firwin
import numpy as np  # for sine function
import csv

# Import the CSV data
time_values_c = []  # column 0
data1 = []  # column 1

with open('sigC.csv') as file_c:
    # Open the CSV file
    reader_c = csv.reader(file_c)
    for row_c in reader_c:
        # Read the rows one by one
        time_values_c.append(float(row_c[0]))  # leftmost column
        data1.append(float(row_c[1]))  # second column

# Implement FFT
sample_rate_c = len(time_values_c) / time_values_c[-1]  # sample rate = total number of samples / total time of samples
sampling_interval_c = 1.0 / sample_rate_c  # sampling interval
time_vector_c = np.arange(0, time_values_c[-1], sampling_interval_c)  # time vector
signal_c = data1  # data to make the FFT from
signal_length_c = len(signal_c)  # length of the signal
frequency_indices_c = np.arange(signal_length_c)
total_time_c = signal_length_c / sample_rate_c
frequency_range_c = frequency_indices_c / total_time_c  # two-sided frequency range
frequency_range_c = frequency_range_c[range(int(signal_length_c / 2))]  # one-sided frequency range
fft_result_c = np.fft.fft(signal_c) / signal_length_c  # FFT computation and normalization
fft_result_c = fft_result_c[range(int(signal_length_c / 2))]

# Plotting FFT
fig1_c, (ax1_c, ax2_c) = plt.subplots(2, 1)
ax1_c.plot(time_values_c, signal_c, 'b')
ax1_c.set_xlabel('Time [s]')
ax1_c.set_ylabel('Amplitude')
ax1_c.set_title('Time Domain Signal')
ax2_c.loglog(frequency_range_c, abs(fft_result_c), 'b')  # plotting the FFT
ax2_c.set_xlabel('Freq (Hz)')
ax2_c.set_ylabel('|Y (freq)| [Amplitude]')
ax2_c.set_title('Frequency Domain Signal')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement moving average low-pass filter
data_array_c = data1
window_size_c = 50
  
i_c = 0
# Initialize an empty list to store moving averages
moving_averages_c = []
  
# Loop through the array to consider every window of size 50
while i_c < len(data_array_c) - window_size_c + 1:
    if i_c < window_size_c - 1:
        moving_averages_c.append(0)
    window_c = data_array_c[i_c : i_c + window_size_c]
    window_average_c = round(sum(window_c) / window_size_c, 2)
    moving_averages_c.append(window_average_c)
    i_c += 1
moving_averages_c = list(moving_averages_c)

fft_filtered_result_c = np.fft.fft(moving_averages_c) / signal_length_c
fft_filtered_result_c = fft_filtered_result_c[range(int(signal_length_c / 2))]

fig2_c, (ax1_c, ax2_c) = plt.subplots(2, 1)
ax1_c.plot(time_values_c, signal_c, 'k', time_values_c, moving_averages_c, 'r')
ax1_c.set_xlabel('Time [s]')
ax1_c.set_ylabel('Amplitude')
ax1_c.set_title('Time Domain Signal with Moving Average')
ax2_c.loglog(frequency_range_c, abs(fft_result_c), 'k', frequency_range_c, abs(fft_filtered_result_c), 'r')
ax2_c.set_xlabel('Freq (Hz)')
ax2_c.set_ylabel('|Y (freq)| [Amplitude]')
ax2_c.set_title('Frequency Domain Signal with Moving Average Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement IIR Filter
filtered_data_c = []
A_c = 0.9
B_c = 0.1

for data_point_c in data1:
    if len(filtered_data_c) == 0:
        filtered_data_c.append(0)
    else:
        filtered_data_c.append(filtered_data_c[-1] * A_c + data_point_c * B_c)

fft_iir_result_c = np.fft.fft(filtered_data_c) / signal_length_c
fft_iir_result_c = fft_iir_result_c[range(int(signal_length_c / 2))]

fig3_c, (ax1_c, ax2_c) = plt.subplots(2, 1)
ax1_c.plot(time_values_c, signal_c, 'k', time_values_c, filtered_data_c, 'r')
ax1_c.set_xlabel('Time [s]')
ax1_c.set_ylabel('Amplitude')
ax1_c.set_title('Time Domain Signal with IIR Filter')
ax2_c.loglog(frequency_range_c, abs(fft_result_c), 'k', frequency_range_c, abs(fft_iir_result_c), 'r')
ax2_c.set_xlabel('Freq (Hz)')
ax2_c.set_ylabel('|Y (freq)| [Amplitude]')
ax2_c.set_title('Frequency Domain Signal with IIR Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement FIR Filter
nyquist_rate_c = sample_rate_c / 2.  # Nyquist rate of the signal (highest discernable frequency)
cutoff_frequency_c = 60  # Cutoff Frequency
len_filt_c = 49  # Length of the filter (number of coefficients)

# Use firwin to create a lowpass FIR filter
fir_coeff_c = firwin(len_filt_c, cutoff_frequency_c / nyquist_rate_c)

# Use lfilter to filter the signal with the FIR filter
filt_sig_c = lfilter(fir_coeff_c, 1.0, data1)

fft_fir_result_c = np.fft.fft(filt_sig_c) / signal_length_c
fft_fir_result_c = fft_fir_result_c[range(int(signal_length_c / 2))]

fig4_c, (ax1_c, ax2_c) = plt.subplots(2, 1)
ax1_c.plot(time_values_c, signal_c, 'k', time_values_c, filt_sig_c, 'r')
ax1_c.set_xlabel('Time [s]')
ax1_c.set_ylabel('Amplitude')
ax1_c.set_title('Time Domain Signal with FIR Filter')
ax2_c.loglog(frequency_range_c, abs(fft_result_c), 'k', frequency_range_c, abs(fft_fir_result_c), 'r')
ax2_c.set_xlabel('Freq (Hz)')
ax2_c.set_ylabel('|Y (freq)| [Amplitude]')
ax2_c.set_title('Frequency Domain Signal with FIR Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
