import glob
import matplotlib.pyplot as plt
import pandas as pd
from annoter import Annoter

if __name__ == '__main__':

    file = glob.glob("data/*")[0]
    df = pd.read_csv(file, skiprows=100, encoding='cp1252', dtype=float)
    data = (df/10)[:180_000].to_numpy().squeeze()
    annoter = Annoter()
    annoter.set_handlers([data, data])
    annoter.set_names(["ICP", "ICP2"])
    plt.show()
    annoter.save()