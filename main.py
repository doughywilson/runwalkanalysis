import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_files = sorted(glob.glob("./csv/*P0*.csv"))

z_thresh = 30.0
fS = 1000  # Sampling rate.
fL = 20  # Cutoff frequency.
N = 115  # Filter length, must be odd.

#FILTER - https://fiiir.com/
h = np.sinc(2 * fL / fS * (np.arange(N) - (N - 1) / 2.))
h *= np.blackman(N)
h /= np.sum(h) #Normalize

for file in data_files:

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

    #Apply the filter
    force_x = np.convolve(h, force_x)
    force_y = np.convolve(h, force_y)
    force_z = np.convolve(h, force_z)

    #Noise gate
    force_x[np.abs(force_x) < z_thresh] = 0.0
    force_y[np.abs(force_y) < z_thresh] = 0.0
    force_z[np.abs(force_z) < z_thresh] = 0.0

    #Calculations
    duty = np.count_nonzero(force_z) / len(force_z)
    horizontal_energy = np.abs(force_x).mean()*duty*meters_per_second
    
    print("{} - vel: {:.2f}, pace: {:.2f}, duty: {:.2f}, Eh: {:.2f}".format(file[6:], meters_per_second, min_per_mile, duty, horizontal_energy))
    # plt.grid()
    # plt.plot(force_x, 'r', label='x')
    # plt.plot(force_y, 'b', label='y')
    # plt.plot(force_z, 'g', label='z')
    # plt.legend()
    # plt.show()

