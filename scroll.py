import matplotlib.pyplot as plt
import glob
import pandas as pd
from scholkmann import modified_scholkmann
from preprocessing import butter_lowpass_filter
import numpy as np


class Monitoring():
    def __init__(self, data: np.array, fig, ax, fs=100) -> None:
        self.df = pd.DataFrame(butter_lowpass_filter(data))
        self.onsets = modified_scholkmann(self.df.values, fs=fs)
        self.dots = None
        self.fig = fig
        self.ax = ax

    def plot(self, lim_a, lim_b):
        self.ax.cla()
        self.ax.plot(self.df[lim_a: lim_b], color='black')
        in_window = (self.onsets > lim_a) & (self.onsets < lim_b)
        for onset in self.onsets[in_window]:
            plt.axvline(onset, color="red")
        self.ax.set_xlim(lim_a, lim_b)
        self.fig.canvas.draw()
    
        
class Scroller:
    def __init__(self, data: Monitoring, chunk: int, button=3):
        data.fig.canvas.mpl_connect('button_press_event', self.on_press)
        data.fig.canvas.mpl_connect('button_release_event', self.on_release)
        data.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.data = data
        self.repair = 0
        self.pressevent = None
        self.chunk = chunk
        self.button = button

    def check_button(self, event):
        return self.button == event.button
    
    def on_press(self, event):
        if self.check_button(event):
            if event.inaxes != ax:
                return None
            self.pressevent = event

    def on_release(self, event):
        if self.check_button(event):
            self.repair = event.xdata
            self.pressevent = None
        
    def on_move(self, event):
        if self.pressevent is None or\
              event.inaxes != self.pressevent.inaxes or\
                  not self.check_button(event):
            return 
        
        dx = event.xdata - self.pressevent.xdata
        try:
            self.repair = self.repair + dx
        except TypeError:
            return
        lim_a = int(self.repair)
        lim_b = int(self.repair + self.chunk)
        if lim_a > 0:
            self.data.plot(lim_a, lim_b)
            self.pressevent = event
    
    def first_plot(self):
        self.data.plot(0, self.chunk)

if __name__ == '__main__':

    CHUNK = 1_000
    file = glob.glob("data/*")[0]
    df = pd.read_csv(file, skiprows=100, encoding='cp1252', dtype=float)
    df = (df/10)[:500_000].to_numpy().squeeze()
    fig, ax = plt.subplots()
    icp_signal = Monitoring(df, fig, ax)
    handler = Scroller(icp_signal, CHUNK, button=3)
    handler.first_plot()
    plt.show()