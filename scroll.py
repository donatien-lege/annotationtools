import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from monitoring import Monitoring
from utils import Displayer
from annotationtools import Scroller


if __name__ == '__main__':

    CHUNK = 1_000
    file = glob.glob("data/*")[0]
    df = pd.read_csv(file, skiprows=100, encoding='cp1252', dtype=float)
    data = (df/10)[:500_000].to_numpy().squeeze()
    fig, ax = plt.subplots()
    icp_signal = Monitoring(data, fs=100)
    displayer = Displayer(icp_signal, fig, ax)
    handler = Scroller(displayer, 3, CHUNK)
    handler.first_plot()
    plt.show()