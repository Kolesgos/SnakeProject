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
    
if __name__ == '__main__':
    X1, Y1 = drawStep(dirr_name = 'Analise1', return_data = True)
    X2, Y2 = drawStep(dirr_name = 'Analise2', return_data = True)
    fig, axs = plt.subplots()
    axs.scatter(X1, Y1, s = 5, color = 'blue')
    axs.plot(X1, Y1, color = 'blue')    
    axs.scatter(X2, Y2, s = 5, color = 'red')
    axs.plot(X2, Y2, color = 'red')      