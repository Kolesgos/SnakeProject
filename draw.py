import os
import time
import random
from snake import *  
from datetime import datetime
import matplotlib.pyplot as plt

def drawStep():
    dirr_name = "Analise"
    files = os.listdir(dirr_name)
    files.sort(key = lambda x: int(x)) 
    X = []
    Y = []
    for ind1 in range(len(files)):
        dirr = files[ind1]
        results = []
        dirr_files = os.listdir(f'{dirr_name}/{dirr}')
        for ind2 in range(len(dirr_files)):
            file = open(f'{dirr_name}/{dirr}/{dirr_files[ind2]}/data.txt', 'r')
            results.append(float(file.read()))
        results.sort()
        ans = sum(results[-4:])/4
        if (len(results) < 4):
            ans = sum(results)/len(results)
        X.append(int(dirr)/1000)
        Y.append(ans)
    fig, axs = plt.subplots()
    axs.scatter(X, Y, s = 5)
    axs.plot(X, Y)
    
if __name__ == '__main__':
    drawStep()