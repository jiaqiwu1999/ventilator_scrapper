import random
from numpy import genfromtxt
import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt

DATA_DIR = '/data/ventsim/'
PERCENT = 0.1

def add_noise(data):
    n = np.random.normal(0, np.std(data), len(data)) * PERCENT
    plt.plot(data + n)
    plt.savefig('noised_data_example.png')
    return data + n

def main():
    files = (list)(glob.glob(f"{DATA_DIR}*.csv"))
    assert len(files) != 0
    for file in files:
        data = genfromtxt(file, delimiter=',')
        data = add_noise(data)
        new_name = file.split('.')[0].split('/')[-1] + '_noised.csv'
        plt.plot(data)
        np.savetxt(new_name, data, delimiter=',')
    # example = 'data/ventsim/hyperinflation_type1_flow.csv'
    # data = genfromtxt(example, delimiter=',')
    # add_noise(data)

if __name__ == '__main__':
    main()