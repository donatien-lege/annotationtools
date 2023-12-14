import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np
import matplotlib.pyplot as plt
import sys

def modified_scholkmann(data: np.array,
                        fs: int = 100,
                        return_output: bool = False):
    
    os = sys.platform
    os_used = "windows" if os.startswith("win") else "linux"
    file = f"cfunc/peaks_{os_used}.so"
    length = len(data)
    output = np.zeros_like(data, dtype='int32')
    lib = ctypes.cdll.LoadLibrary(file)
    func = lib.peaks
    func.argtypes = [ndpointer(ctypes.c_float),
                ctypes.c_int,
                ctypes.c_int,
                ndpointer(ctypes.c_int)]
    func(data.astype('float32'), length, fs, output)
    
    segm = np.where(output==min(output))[0]
    segm = np.append(segm, len(data))
    segm = np.unique(segm)
    if return_output:
        return output
    return segm

def plot_seps(data: np.array,
              segm: np.array):
    plt.plot(data)
    for tick in segm:
        plt.axvline(tick, color='red')
        
def extracted_pulses(data: np.array,
              segm: np.array):
    return [data[i: j] for i, j in zip(segm, segm[1:])]

def lengths(segm):
    return np.array([j-i for i, j in zip(segm, segm[1:])])
