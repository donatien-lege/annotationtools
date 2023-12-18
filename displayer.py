from monitoring import Monitoring

class Displayer():
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
        self.fig.canvas.draw()
    
    def plot_sep(self, lim_a, lim_b):
        in_window = (self.monit.p1p2 > lim_a) & (self.monit.p1p2 < lim_b)
        for peak in self.monit.p1p2[in_window]:
            self.ax.scatter(peak, self.monit.df.iloc[peak, 0], color='red')
        self.fig.canvas.draw()

    def plot_p1p2(self, lim_a, lim_b):
        in_window = (self.monit.onsets > lim_a) & (self.monit.onsets < lim_b)
        for onset in self.monit.onsets[in_window]:
            self.ax.axvline(onset, color="white")
        self.fig.canvas.draw()

    def plot_pulse(self, pos, **kwargs):
        cut = len(self.monit.onsets[self.monit.onsets < pos])
        start, stop = self.monit.onsets[cut - 1], self.monit.onsets[cut]
        self.ax.plot(self.monit.df[start: stop], **kwargs)
        self.fig.canvas.draw()

    