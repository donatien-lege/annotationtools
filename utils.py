from monitoring import Monitoring

class Displayer():
    def __init__(self, monit: Monitoring, fig, ax):
        self.monit = monit
        self.fig = fig
        self.ax = ax

    def plot(self, lim_a, lim_b):
        self.ax.cla()
        self.ax.plot(self.monit.df[lim_a: lim_b], color='black')
        in_window = (self.monit.onsets > lim_a) & (self.monit.onsets < lim_b)
        for onset in self.monit.onsets[in_window]:
            self.ax.axvline(onset, color="red")
        self.ax.set_xlim(lim_a, lim_b)
        self.fig.canvas.draw()

    def plot_current(self, pos):
        cut = len(self.monit.onsets[self.monit.onsets < pos])
        self.ax.plot(self.monit.df[cut - 1: cut])
        self.fig.canvas.draw()

    