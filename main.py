import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_files = sorted(glob.glob("./csv/G*P0*.csv"))
index_start = 5000
index_length = 2000

z_thresh = 25.0
fS = 1000  # Sampling rate.
fL = 480  # Cutoff frequency.
N = 115  # Filter length, must be odd.
dt = 1.0/1000

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
    
    #Crop the files
    force_x = force_x[index_start:index_start+index_length]
    force_y = force_y[index_start:index_start+index_length]
    force_z = force_z[index_start:index_start+index_length]

    #Noise gate
    # force_x[np.abs(force_x) < z_thresh] = 0.0
    # force_y[np.abs(force_y) < z_thresh] = 0.0
    # force_z[np.abs(force_z) < z_thresh] = 0.0
    # duty = np.count_nonzero(force_z) / float(len(force_z))
    duty = float(len(force_z[np.abs(force_z) > z_thresh])) / float(len(force_z))

    #Calculations
    Et = np.sqrt(force_y**2)
    horizontal_energy = Et.sum()*duty*meters_per_second*dt
    vertical_energy = np.abs(force_z**2).sum()
    # horizontal_energy = np.abs(force_x).sum()*duty*meters_per_second*dt
    # height = 1/8 * 9.8 * t**2

    Ih = np.abs(force_y).sum()*dt
    Iv = np.abs(force_z).sum()*dt
    Ix = np.abs(force_x).sum()*dt
    T = Ih + Iv + Ix
    
    print("{} - vel: {:.2f}, pace: {:.2f}, duty: {:.2f}, Ih: {:.2f}, Iv: {:.2f}, Ix: {:.2f}, T: {:.2f}".format(file[6:], meters_per_second, min_per_mile, duty, Ih, Iv ,Ix, T))
    plt.grid()
    plt.plot(force_x, 'r', label='x')
    plt.plot(force_y, 'b', label='y')
    plt.plot(force_z, 'g', label='z')
    plt.ylim(-2100, 400)
    plt.legend()
    plt.show()

