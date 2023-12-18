from displayer import Displayer
import inspect
import numpy as np

class AnnotationTool():

    def __init__(self, displayer: Displayer, button: int):
        self.displayer = displayer
        self.button = button

    def connect(self, type_event: str, meth: str):
        methods = dict(inspect.getmembers(self))
        self.displayer.fig.canvas.mpl_connect(type_event, methods[meth])
    
    def check_button(self, event):
        return self.button == event.button


class Scroller(AnnotationTool):
    def __init__(self, displayer: Displayer, button: int, chunk: int):
        super().__init__(displayer, button)
        self.connect('key_press_event', 'on_press')
        self.repair = 0
        self.pressevent = None
        self.chunk = chunk
    
    def on_press(self, event):
        if event.key not in ['right', 'left']:
            return
        if event.key == 'right':
            repair = self.repair + self.chunk // 10
        if event.key == 'left':
            repair = self.repair - self.chunk // 10
        if repair > 0 and repair < len(self.displayer.monit.df) - self.chunk:
            self.repair = repair
            self.displayer.plot(self.repair, self.repair + self.chunk)

    def first_plot(self):
        self.displayer.plot(0, self.chunk)


class Highlighter(AnnotationTool):
    def __init__(self, displayer: Displayer, button: int):
        super().__init__(displayer, button)
        self.connect('button_press_event', 'on_press')
        self.color = 'green'
        self.n = 0
    
    def on_press(self, event):
        if self.check_button(event):
            self.displayer.plot_pulse(event.xdata, color=self.color[self.n])

class PeakMover(AnnotationTool):
    def __init__(self, displayer: Displayer, button: int):
        super().__init__(displayer, button)
        self.connect('button_press_event', 'on_press')
        self.connect('button_release_event', 'on_release')
        self.index_to_modify = None
    
    def on_press(self, event):
        if self.check_button(event):
            scores = np.abs(self.displayer.monit.p1p2 - event.xdata)
            self.index_to_modify = np.argmin(scores)
            print("press")

    def on_release(self, event):
        if self.check_button(event):
            peaks = self.displayer.monit.candidates
            new_value = peaks[np.argmin(np.abs(peaks - event.xdata))]
            self.displayer.monit.p1p2[self.index_to_modify] = new_value
            lim_a, lim_b = map(int, self.displayer.ax.get_xlim())
            self.displayer.plot(lim_a, lim_b)
            print("release")
