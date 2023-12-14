from scipy.signal import filtfilt, butter
import numpy as np

def butter_lowpass_filter(data: np.array, cutoff=20, fs=100, order=4):
    
    assert data.ndim == 1, f"""input data must be 1-dimensional,\\
        found {data.shape}"""
        
    normal_cutoff = cutoff / (0.5*fs)
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y
