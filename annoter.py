from labelling import Scroller, Highlighter, PeakMover
from monitoring import Monitoring
from displayer import Displayer
from typing import Iterable
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

class AxHandler():
    def __init__(self, signal: Monitoring, fig, ax, highlight=3, move=1):
        self.displayer = Displayer(signal, fig, ax)
        self.scroller = Scroller(self.displayer, chunk=signal.fs)
        self.highlighter = Highlighter(self.displayer, highlight)
        self.peakmover = PeakMover(self.displayer, move)
        self.scroller.first_plot()


class Annoter():
    def __init__(self) -> None:
        self.fig, self.axes = None
        self.axhandlers = None
        self.names = None

    def set_names(self, names=Iterable):
        self.names = names
        for ax, name in zip(self.axes, self.names):
            ax.set_title(name)
        self.fig.canvas.draw()

    def save(self, folder:str):
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass
        if len(self.axes) != len(self.names):
            self.names = [f"ax_{i}" for i,_ in enumerate(self.axes)]
        
        for ah, name in zip(self.axhandlers, self.names):
            prefix = f"{folder}/{name}"
            monit = ah.displayer.monit
            save_df = pd.DataFrame(monit.df)
            save_df.to_csv(f"{prefix}/df.csv", index=False)
            save_peaks = pd.DataFrame(monit.peaks)
            save_peaks.to_csv(f"{prefix}/peaks.csv", index=False)
            save_category = pd.DataFrame(tuple(monit.categories.values()))
            save_category.to_csv(f"{prefix}/peaks.csv", index=False)
            save_candidates = pd.DataFrame(monit.candidates)
            save_candidates.to_csv(f"{prefix}/candidates.csv", index=False)
            save_onsets = pd.DataFrame(monit.onsets)
            save_onsets.to_csv(f"{prefix}/onsets.csv", index=False)