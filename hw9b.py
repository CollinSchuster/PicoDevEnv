import matplotlib.pyplot as plt  # for plotting
from scipy.signal import lfilter, firwin
import numpy as np  # for sine function
import csv

# Import the CSV data
time_values_b = []  # column 0
signal_data_b = []  # column 1

with open('sigB.csv') as file_b:
    # Open the CSV file
    reader_b = csv.reader(file_b)
    for row_b in reader_b:
        # Read the rows one by one
        time_values_b.append(float(row_b[0]))  # leftmost column
        signal_data_b.append(float(row_b[1]))  # second column

# Implement FFT
sample_rate_b = len(time_values_b) / time_values_b[-1]  # sample rate = total number of samples / total time of samples
sampling_interval_b = 1.0 / sample_rate_b  # sampling interval
time_vector_b = np.arange(0, time_values_b[-1], sampling_interval_b)  # time vector
signal_b = signal_data_b  # data to make the FFT from
signal_length_b = len(signal_b)  # length of the signal
frequency_indices_b = np.arange(signal_length_b)
total_time_b = signal_length_b / sample_rate_b
frequency_range_b = frequency_indices_b / total_time_b  # two-sided frequency range
frequency_range_b = frequency_range_b[range(int(signal_length_b / 2))]  # one-sided frequency range
fft_result_b = np.fft.fft(signal_b) / signal_length_b  # FFT computation and normalization
fft_result_b = fft_result_b[range(int(signal_length_b / 2))]

# Plotting FFT
fig1_b, (ax1_b, ax2_b) = plt.subplots(2, 1)
ax1_b.plot(time_values_b, signal_b, 'b')
ax1_b.set_xlabel('Time [s]')
ax1_b.set_ylabel('Amplitude')
ax1_b.set_title('Time Domain Signal')
ax2_b.loglog(frequency_range_b, abs(fft_result_b), 'b')  # plotting the FFT
ax2_b.set_xlabel('Freq (Hz)')
ax2_b.set_ylabel('|Y (freq)| [Amplitude]')
ax2_b.set_title('Frequency Domain Signal')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement moving average low-pass filter
data_array_b = signal_data_b
window_size_b = 100
  
i_b = 0
# Initialize an empty list to store moving averages
moving_averages_b = []
  
# Loop through the array to consider every window of size 100
while i_b < len(data_array_b) - window_size_b + 1:
    if i_b < window_size_b - 1:
        moving_averages_b.append(0)
    window_b = data_array_b[i_b : i_b + window_size_b]
    window_avg_b = round(sum(window_b) / window_size_b, 2)
    moving_averages_b.append(window_avg_b)
    i_b += 1
moving_averages_b = list(moving_averages_b)

fft_filtered_result_b = np.fft.fft(moving_averages_b) / signal_length_b
fft_filtered_result_b = fft_filtered_result_b[range(int(signal_length_b / 2))]

fig2_b, (ax1_b, ax2_b) = plt.subplots(2, 1)
ax1_b.plot(time_values_b, signal_b, 'k', time_values_b, moving_averages_b, 'r')
ax1_b.set_xlabel('Time [s]')
ax1_b.set_ylabel('Amplitude')
ax1_b.set_title('Time Domain Signal with Moving Average')
ax2_b.loglog(frequency_range_b, abs(fft_result_b), 'k', frequency_range_b, abs(fft_filtered_result_b), 'r')
ax2_b.set_xlabel('Freq (Hz)')
ax2_b.set_ylabel('|Y (freq)| [Amplitude]')
ax2_b.set_title('Frequency Domain Signal with Moving Average Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement IIR Filter
filtered_data_b = []
A_b = 0.99
B_b = 0.01

for data_point_b in signal_data_b:
    if len(filtered_data_b) == 0:
        filtered_data_b.append(0)
    else:
        filtered_data_b.append(filtered_data_b[-1] * A_b + data_point_b * B_b)

fft_iir_result_b = np.fft.fft(filtered_data_b) / signal_length_b
fft_iir_result_b = fft_iir_result_b[range(int(signal_length_b / 2))]

fig3_b, (ax1_b, ax2_b) = plt.subplots(2, 1)
ax1_b.plot(time_values_b, signal_b, 'k', time_values_b, filtered_data_b, 'r')
ax1_b.set_xlabel('Time [s]')
ax1_b.set_ylabel('Amplitude')
ax1_b.set_title('Time Domain Signal with IIR Filter')
ax2_b.loglog(frequency_range_b, abs(fft_result_b), 'k', frequency_range_b, abs(fft_iir_result_b), 'r')
ax2_b.set_xlabel('Freq (Hz)')
ax2_b.set_ylabel('|Y (freq)| [Amplitude]')
ax2_b.set_title('Frequency Domain Signal with IIR Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Implement FIR Filter
nyquist_rate_b = sample_rate_b / 2.  # Nyquist rate of the signal (highest discernable frequency)
cutoff_frequency_b = 10  # Cutoff Frequency
len_filt_b = 79  # Length of the filter (number of coefficients)

# Use firwin to create a lowpass FIR filter
firwin_coeff_b = firwin(len_filt_b, cutoff_frequency_b / nyquist_rate_b)

# Use lfilter to filter the signal with the FIR filter
filt_sig_b = lfilter(firwin_coeff_b, 1.0, signal_data_b)

fft_fir_result_b = np.fft.fft(filt_sig_b) / signal_length_b
fft_fir_result_b = fft_fir_result_b[range(int(signal_length_b / 2))]

fig4_b, (ax1_b, ax2_b) = plt.subplots(2, 1)
ax1_b.plot(time_values_b, signal_b, 'k', time_values_b, filt_sig_b, 'r')
ax1_b.set_xlabel('Time [s]')
ax1_b.set_ylabel('Amplitude')
ax1_b.set_title('Time Domain Signal with FIR Filter')
ax2_b.loglog(frequency_range_b, abs(fft_result_b), 'k', frequency_range_b, abs(fft_fir_result_b), 'r')
ax2_b.set_xlabel('Freq (Hz)')
ax2_b.set_ylabel('|Y (freq)| [Amplitude]')
ax2_b.set_title('Frequency Domain Signal with FIR Filter')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
