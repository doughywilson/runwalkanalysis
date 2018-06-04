import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_files = sorted(glob.glob("./csv/J_P10*.csv"))

for file in data_files:
    print("Reading", file)

    min_per_mile = int(file[-6:-4])
    meters_per_second = (1.0/min_per_mile) / 60 * 1609.34

    df = pd.read_csv(file, header=0) #TODO: pandas is currently reading the first line as header
    force_x = np.zeros(len(df.values))
    force_y = np.zeros(len(df.values))
    force_z = np.zeros(len(df.values))
    for i, line in enumerate(df.values):
        force_x[i] = (line[2])
        force_y[i] = (line[3])
        force_z[i] = (line[4])
    
    plt.grid()
    plt.plot(force_x, 'r', label='x')
    plt.plot(force_y, 'b', label='y')
    plt.plot(force_z, 'g', label='z')
    plt.legend()
    plt.show()