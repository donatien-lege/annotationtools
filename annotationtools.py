from utils import Displayer
import inspect

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
        self.connect('button_press_event', 'on_press')
        self.connect('button_release_event', 'on_release')
        self.connect('motion_notify_event', 'on_move')
        self.repair = 0
        self.pressevent = None
        self.chunk = chunk
    
    def on_press(self, event):
        if self.check_button(event):
            if event.inaxes != self.displayer.ax:
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
            self.displayer.plot(lim_a, lim_b)
            self.pressevent = event

    def first_plot(self):
        self.displayer.plot(0, self.chunk)
