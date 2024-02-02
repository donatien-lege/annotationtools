import glob
import matplotlib.pyplot as plt
import pandas as pd
from annoter import Annoter
from os.path import basename

if __name__ == '__main__':

    file = glob.glob("data/to_label/*")[0]
    df = pd.read_csv(file, skiprows=100, encoding='cp1252', dtype=float)
    data = (df/10).to_numpy().squeeze()
    annoter = Annoter()
    folder = f"data/labels/{basename(file[:-4])}"
    try:
        annoter.load(folder)
    except FileNotFoundError:
        annoter.set_handlers([data])
        annoter.set_names(["ICP"])
    plt.show()
    annoter.save()