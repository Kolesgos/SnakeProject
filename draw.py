import os
import matplotlib.pyplot as plt

def drawStep(dirr_name = "Analise", color = "blue", return_data = False):
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
            if (len(results) == 0):
                ans = 0
            else:
                ans = sum(results)/len(results)
        X.append(int(dirr)/1000)
        Y.append(ans)
    if (return_data):
        return X, Y
    fig, axs = plt.subplots()
    axs.scatter(X, Y, s = 5, color = color)
    axs.plot(X, Y, color = color)
    axs.set_ylim([0, max(Y)*1.1])
    
def drawPopulation(dirr_name):
    file = open(f'{dirr_name}/population.txt', 'r')
    data = file.read().split('\n')[:-1]
    file.close()
    fig, axs = plt.subplots()
    X = list(map(lambda x: int(x.split()[0])/1000000, data))
    Y = list(map(lambda x: int(x.split()[1]), data))
    axs.plot(X, Y)
    axs.set_ylim([0, max(Y)*1.1])
    axs.set_xlim([min(X), max(X)])
    for i in range(len(X)):
        dt = min(i, len(X) - i, 15)
        Delta = Y[i-dt: i+dt+1]
        Y[i] = sum(Delta)/len(Delta)
    axs.plot(X, Y, color = 'red')
    axs.set_title("Population")
    
if __name__ == '__main__':
    drawPopulation('Brains1')
    '''X1, Y1 = drawStep(dirr_name = 'Analise1', return_data = True)
    #X2, Y2 = drawStep(dirr_name = 'Analise2', return_data = True)
    ##########
    X = [X1]
    Y = [Y1]
    ##########
    Xstart = []
    Ystart = []
    for ind in range(len(X)-1):
        for i in range(len(X[ind])):
            if (X[ind][i] < min(list(map(min, X[ind+1:])))):
                Xstart.append(X[ind][i])
                Ystart.append(Y[ind][i])
            
    fig, axs = plt.subplots()
    for i in range(len(X) - 1):
        axs.scatter(X[i], Y[i], s = 5, color = str(1 - (i+1)/len(X)))
        axs.plot(X[i], Y[i], color = str(1 - (i+1)/len(X)))          
    axs.scatter(Xstart + X[-1], Ystart + Y[-1], s = 5, color = 'red')
    axs.plot(Xstart + X[-1], Ystart + Y[-1], color = 'red')
    axs.set_ylim([min(min(Y, key = lambda x: min(x)))*0.9, max(max(Y, key = lambda x: max(x)))*1.1])'''