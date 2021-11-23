import os
import matplotlib.pyplot as plt

def drawStep(dirr_name = "Analise", color = "blue", return_data = False, best = True):
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
            #print(f'{dirr_name}/{dirr}/{dirr_files[ind2]}')
            results.append(float(file.read()))
        results.sort()
        if (best):
            ans = sum(results[-4:])/4
            if (len(results) < 4):
                if (len(results) == 0):
                    ans = 0
                else:
                    ans = sum(results)/len(results)
        elif (len(results) != 0):
            ans = sum(results)/len(results)
        else:
            ans = 0
        X.append(int(dirr)/1000)
        Y.append(ans)
    if (return_data):
        return X, Y
    fig, axs = plt.subplots()
    axs.scatter(X, Y, s = 5, color = color)
    axs.plot(X, Y, color = color)
    axs.set_ylim([0, max(Y)*1.1])
    axs.set_title("Effectiveness")
    
def drawPopulation(dirr_name, delta = 15):
    file = open(f'{dirr_name}/population.txt', 'r')
    data = file.read().split('\n')[:-1]
    file.close()
    fig, axs = plt.subplots()
    X = list(map(lambda x: int(x.split()[0])/1000000, data))
    Y = list(map(lambda x: int(x.split()[1]), data))
    
    Y1 = []
    
    Z = list(zip(X, Y))
    Z.sort()
    X, Y = zip(*Z)    
    X = list(X)
    Y = list(Y)
    
    axs.plot(X, Y)
    axs.set_ylim([0, max(Y)*1.1])
    axs.set_xlim([min(X), max(X)])
    for i in range(len(X)):
        dt = min(i, len(X) - i, delta)
        dt1 = min(i, len(X) - i, delta*5)
        Delta = Y[i-dt: i+dt+1]
        DELTA = Y[i-dt1:i+dt1+1]
        Y[i] = sum(Delta)/len(Delta)
        Y1.append(sum(DELTA)/len(DELTA))
    axs.plot(X, Y, color = 'red')
    axs.plot(X[10:-10], Y1[10:-10], color = 'white')
    
    axs.set_title("Population")
    
if __name__ == '__main__':
    key = input("Type: ")
    if (key == '1'):
        drawPopulation('Brains1', delta = 20)
    elif (key == '2'):
        X1, Y1 = drawStep(dirr_name = 'Analise1', return_data = True)
        X2, Y2 = drawStep(dirr_name = 'Analise2', return_data = True)
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
        axs.set_ylim([min(min(Y, key = lambda x: min(x)))*0.9, max(max(Y, key = lambda x: max(x)))*1.1])        
    else:
        X, Y = drawStep(dirr_name = 'Analise1', return_data = True, best = True, color = 'blue')
        for i in range(1, len(X)):
            print(X[i], Y[i])
        fig, axs = plt.subplots()
        axs.plot(X, Y, color = 'blue')
        Xavg = []
        Yavg = []
        D = 15
        for i in range(len(X)):
            Xavg.append(X[i])
            delta = min(i, len(X)-1-i, D)
            curr = Y[i-delta:i+delta+1]
            Yavg.append(sum(curr)/len(curr)) 
        X, Y = drawStep(dirr_name = 'Analise1', return_data = True, best = False, color = 'blue')
        #axs.plot(X, Y, color = 'blue')
        axs.plot(Xavg, Yavg, color = 'red')