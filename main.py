import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_files = glob.glob("./csv/*.csv")

for file in data_files:
    print("Reading", file)

    df = pd.read_csv(file, header=0) #TODO: pandas is currently reading the first line as header
    energy_buff = np.zeros(len(df.values))
    for i, line in enumerate(df.values):
        energy_buff[i] = np.sqrt(line[2]**2 + line[3]**2 + line[4]**2)
    
    print("Mean Energy: ",energy_buff.mean())