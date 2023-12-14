import matplotlib.pyplot as plt
import glob
import pandas as pd


class Scroller:
    def __init__(self, df, chunk, fig, ax, button=3, fs=100):
        fig.canvas.mpl_connect('button_press_event', self.on_press)
        fig.canvas.mpl_connect('button_release_event', self.on_release)
        fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.repair = 0
        self.pressevent = None
        self.chunk = chunk
        self.button = button
        self.fig = fig
        self.ax = ax
        self.df = df

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
        self.repair = self.repair + dx
        lim_a = int(self.repair)
        lim_b = int(self.repair + self.chunk)
        if lim_a > 0:
            self.ax.cla()
            self.ax.plot(self.df[lim_a: lim_b], color='black')
            self.ax.set_xlim(lim_a, lim_b)
            self.fig.canvas.draw()
            self.pressevent = event

if __name__ == '__main__':

    CHUNK = 1_000
    file = glob.glob("data/*")[0]
    df = pd.read_csv(file, skiprows=100, encoding='cp1252')
    df = (df/10).astype(float)
    fig, ax = plt.subplots()
    ax.plot(df[:CHUNK], color='black')

    handler = Scroller(df, CHUNK, fig, ax, button=3, fs=100)
    plt.show()