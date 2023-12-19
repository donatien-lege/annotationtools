import pandas as pd
import numpy as np
from scholkmann import modified_scholkmann
from preprocessing import butter_lowpass_filter, curvature
from typing import Iterable
from scipy.signal import argrelmax
from collections import defaultdict


class Monitoring():

    def __init__(
        self, 
        data: Iterable = None,
        fs=100, 
        p1p2=True,
        previous: dict=None
    ):
        if previous is not None:
            self.df = previous["signal"]
            self.peaks = previous["peaks"]
            self.onsets = previous["onsets"]
            self.category = previous["category"]
            self.candidates = previous["candidates"]
        else:
            self.df = pd.DataFrame(butter_lowpass_filter(data))
            self.onsets = modified_scholkmann(self.df.values, fs=fs)
            self.category = {k: 0 for k in self.onsets}
            if p1p2:
                self.candidates, self.peaks = self.proposal_p1p2()
            else:
                self.candidates, self.peaks = self.proposal_max()
        self.fs = fs

    def proposal_p1p2(self):
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

    def proposal_max(self):
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
            final_array.append(max(v, key=lambda x: self.df.values[x]))
    
        return local_max, np.array(final_array)