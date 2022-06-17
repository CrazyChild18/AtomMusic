from matplotlib import mlab, pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion
import numpy as np
import hashlib
import config


# Use FFT to converte time domain signal to frequency domain signal.
# and get a specgram after log
def getSpecgramArr(sample, fs, nfft=config.fft_window_size, window=mlab.window_hanning,
                   noverlap=int(config.fft_window_size * config.fft_overlap_ratio)):
    """
    :param sample: one channel of audio sample
    :param fs: audio frequency
    :param nfft: The number of data points used in each block for the FFT.
    :param window : vector of length NFFT
    :param noverlap: much much is overlap in a window
    :return: spectrum(2-D array) in log space
    """
    spectrum, freqs, t = mlab.specgram(sample, NFFT=nfft, Fs=fs, window=window,
                                          noverlap=noverlap)

    # spectrum actually represent a 3-d graph of time freqs and intensity

    # transfer to log space
    # spectrum = abs(20 * np.log10(spectrum))
    # replace all0 with 1 to avoid log(0) appear since the intensity is 0 and log(1) = 0
    spectrum[spectrum == 0] = 1
    spectrum = 10 * np.log10(spectrum)
    # replace -infs with zeros since it does not effect the result(because we are choosing the maximun value)
    spectrum[spectrum == -np.inf] = 0
    # max value of freqs in log space (0-70)
    #print(np.max(spectrum))
    return spectrum


def getConstellationMap(spectrum, plot=False, min_peak_amp=config.minimun_peak_amplitude):
    """
    :param spectrum: the array of spectrum in log space (from getSpecgramArr)
    :param plot: if show the plot
    :param min_peak_amp: the minimum value to regard as peak
    :return: 2-d array of peaks [(x1,y1),(x2,y2),.......]
    """
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, config.peak_neighborhood_size)

    # find local maxima using our fliter shape
    local_max = maximum_filter(spectrum, footprint=neighborhood) == spectrum
    background = (spectrum == 0)
    eroded_background = binary_erosion(background, structure=neighborhood,
                                       border_value=1)

    # Boolean mask of arr2D with True at peaks
    detected_peaks = local_max ^ eroded_background

    # extract peaks
    amps = spectrum[detected_peaks]
    j, i = np.where(detected_peaks)


    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > min_peak_amp]  # time, freq, amp

    # get indices for frequency and time
    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]
    #print(max(time_idx))

    if plot:
        # scatter of the peaks
        fig, ax = plt.subplots()
        ax.imshow(spectrum)
        ax.scatter(time_idx, frequency_idx, marker=".")
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title("Spectrogram")
        plt.gca().invert_yaxis()
        plt.savefig("test.jpg")
        # plt.xlim(200, 800)
        plt.xlim(200, 500)
        plt.ylim(0, 400)
        plt.show()
    return list(zip(time_idx, frequency_idx))


# get Fast Combinatorial Hashing
def getFBHashGenerator(peaks, fanout_factor=config.fanout_factor):
    """

    :param peaks: 2-d array of peaks (from getConstellationMap)
    :param fanout_factor:
    :return: a FBHash list

    Hash list structure:
       sha1_hash   time_offset
    [(e05b341a9b77a51fd26, 32), ... ]
    """
    peaks.sort(key=lambda x: x[0])

    # use target zone.
    for i in range(len(peaks) - fanout_factor):
        for j in range(fanout_factor):
            t1 = peaks[i][0]  # anchor point time
            t2 = peaks[i + j][0]  # time of point in target zone
            freq1 = peaks[i][1]  # frequency of anchor point
            freq2 = peaks[i + j][1]  # frequency of point in target zone
            t_delta = t2 - t1
            if config.time_constraint_condition[0] <= t_delta <= config.time_constraint_condition[1]:
                h = hashlib.sha256(
                    ("%s_%s_%s" % (str(freq1), str(freq2), str(t_delta))).encode())
                yield h.hexdigest()[0:64 - config.fingerprint_cutoff], t1
