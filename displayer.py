from monitoring import Monitoring
import numpy as np

class Displayer():
    corresp = {0: "black", 1: "purple", 2: "red"}

    def __init__(self, monit: Monitoring, fig, ax):
        self.monit = monit
        self.fig = fig
        self.ax = ax

    def plot(self, lim_a, lim_b):
        self.ax.cla()
        self.ax.plot(self.monit.df[lim_a: lim_b], color='black')
        self.ax.set_xlim(lim_a, lim_b)
        self.plot_sep(lim_a, lim_b)
        self.plot_p1p2(lim_a, lim_b)
        self.update_colors(lim_a, lim_b)
        self.fig.canvas.draw()

    def update_colors(self, lim_a, lim_b):
        onsets = self.monit.onsets
        start = max(0, np.argmax(onsets > lim_a) - 1)
        end = np.argmin(onsets < lim_b) + 1
        disp_idx = np.arange(start, end)
        for s, e in zip(disp_idx, disp_idx[1:]):
            color = self.corresp[self.monit.category[onsets[s]]]
            if color != "black":
                self.plot_layer(onsets[s], onsets[e], color=color)

    def plot_sep(self, lim_a, lim_b):
        in_window = (self.monit.p1p2 > lim_a) & (self.monit.p1p2 < lim_b)
        for peak in self.monit.p1p2[in_window]:
            self.ax.scatter(peak, self.monit.df.iloc[peak, 0], color='red')

    def plot_p1p2(self, lim_a, lim_b):
        in_window = (self.monit.onsets > lim_a) & (self.monit.onsets < lim_b)
        for onset in self.monit.onsets[in_window]:
            self.ax.axvline(onset, color="white")

    def plot_layer(self, start, stop, **kwargs):
        self.ax.plot(self.monit.df[start: stop], **kwargs)
        self.fig.canvas.draw()

    