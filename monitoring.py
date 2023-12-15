import pandas as pd
from scholkmann import modified_scholkmann
from preprocessing import butter_lowpass_filter
from typing import Iterable

class Monitoring():
    def __init__(self, data: Iterable, fs=100):
        self.df = pd.DataFrame(butter_lowpass_filter(data))
        self.onsets = modified_scholkmann(self.df.values, fs=fs)
        self.dots = None
