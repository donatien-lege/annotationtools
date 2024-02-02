from labelling import Scroller, Highlighter, PeakMover
from monitoring import Monitoring
from displayer import Displayer
from typing import Iterable
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import ctypes

class AxHandler():
    def __init__(
            self, 
            signal: Monitoring,
            fig, 
            ax, 
            highlight=3, 
            move=1, 
            chunk=5
            ):
        self.displayer = Displayer(signal, fig, ax)
        self.scroller = Scroller(self.displayer, chunk = chunk * signal.fs)
        self.highlighter = Highlighter(self.displayer, highlight)
        self.peakmover = PeakMover(self.displayer, move)
        self.scroller.first_plot()


class Annoter():
    def __init__(self, folder="current") -> None:
        self.fig = None
        self.axes = None
        self.axhandlers = None
        self.names = None
        self.folder = folder

    def set_names(self, names=Iterable):
        self.names = names
        for ax, name in zip(self.axes, self.names):
            ax.set_title(name)
        self.fig.canvas.draw()

    def set_handlers(self, signals: Iterable):
        self.fig, self.axes = plt.subplots(len(signals), squeeze=False)
        self.axes = self.axes.reshape(1)
        params = zip(map(Monitoring, signals), self.axes)
        self.axhandlers = [AxHandler(m, self.fig, ax) for m, ax in params]
        self.fig.canvas.mpl_connect("key_press_event", self.msg_save)

    def load(self, folder: str):
        self.folder = folder
        subnames = glob.glob(f"{folder}/*")
        if len(subnames) == 0:
            raise FileNotFoundError
        self.fig, self.axes = plt.subplots(len(subnames), squeeze=False)
        self.axes = self.axes.reshape(1)
        handlers = []
        for sub in subnames:
            onsets = pd.read_csv(f"{sub}/onsets.csv").values.squeeze()
            categories = pd.read_csv(f"{sub}/category.csv").values.squeeze()
            to_append = {
                "signal": pd.read_csv(f"{sub}/df.csv"),
                "peaks": pd.read_csv(f"{sub}/peaks.csv").to_numpy(),
                "candidates": pd.read_csv(f"{sub}/candidates.csv").to_numpy(),
                "onsets": onsets,
                "category": {k: v for k, v in zip(onsets, categories)}
            }
            handlers.append(to_append)
        params = zip((Monitoring(previous=x) for x in handlers), self.axes)
        self.axhandlers = [AxHandler(m, self.fig, ax) for m, ax in params]
        self.set_names(os.listdir(folder))

    def msg_save(self, event):
        if event.key == "enter":
            msg = f"Annotations saved to folder: {self.folder}"
            ctypes.windll.user32.MessageBoxW(0, msg, "", 1)
        self.save()

    def save(self):
        print(self.folder)
        try:
            os.mkdir(self.folder)
        except FileExistsError:
            pass
        for n in self.names:
            os.makedirs(f"{self.folder}/{n}", exist_ok=True)
        if len(self.axes) != len(self.names):
            self.names = [f"ax_{i}" for i,_ in enumerate(self.axes)]
        
        for ah, name in zip(self.axhandlers, self.names):
            prefix = f"{self.folder}/{name}"
            monit = ah.displayer.monit
            monit.df.to_csv(f"{prefix}/df.csv", index=False)
            save_peaks = pd.DataFrame(monit.peaks)
            save_peaks.to_csv(f"{prefix}/peaks.csv", index=False)
            save_category = pd.DataFrame(tuple(monit.category.values()))
            save_category.to_csv(f"{prefix}/category.csv", index=False)
            save_candidates = pd.DataFrame(monit.candidates)
            save_candidates.to_csv(f"{prefix}/candidates.csv", index=False)
            save_onsets = pd.DataFrame(monit.onsets)
            save_onsets.to_csv(f"{prefix}/onsets.csv", index=False)
        
    