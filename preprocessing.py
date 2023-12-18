from scipy.signal import filtfilt, butter
import numpy as np

def butter_lowpass_filter(data: np.array, cutoff=20, fs=100, order=4):
    
    assert data.ndim == 1, f"""input data must be 1-dimensional,\\
        found {data.shape}"""
        
    normal_cutoff = cutoff / (0.5 * fs)
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def curvature(data: np.array):
    diff1 = np.gradient(- 100 * data)
    diff2 = np.gradient(diff1)
    return diff2/(1 + diff1 ** 2) ** (3/2)