import pandas as pd
import numpy as np
from scholkmann import modified_scholkmann
from preprocessing import butter_lowpass_filter, curvature
from typing import Iterable
from scipy.signal import argrelmax
from collections import defaultdict


class Monitoring():

    def __init__(self, data: Iterable, fs=100):
        self.df = pd.DataFrame(butter_lowpass_filter(data))
        self.onsets = modified_scholkmann(self.df.values, fs=fs)
        self.candidates, self.p1p2 = self.proposal()
        self.category = {k: 0 for k in self.onsets}

    def proposal(self):
        curve = curvature(self.df.values.squeeze())
        local_max = argrelmax(curve)[0]
        corresp = defaultdict(list)
        start = 0

        for c in local_max:
            if c > self.onsets[start]:
                start += 1
            corresp[self.onsets[start]].append(c)

        final_array = []
        for v in corresp.values():
            three_peaks = sorted(v, key=lambda x: curve[x])[-3:]
            final_array += sorted(three_peaks)[:2]
    
        return local_max, np.array(final_array)