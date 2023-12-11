
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

def analyseFile(file):
    reader = csv.reader(open(file, encoding = "utf-8"))
    
    line_count = 0
    
    allIterations = np.array([])
    
    for line in reader:
        if (line_count % 2) == 0:
            labels = line
            line_count += 1
        else:
            line = zip(labels, line)
            # for item in line:    
            #     print(f"{item[0]} - {item[1]}")
                
            allIterations = np.concatenate((allIterations, line), axis = None)
            
            line_count += 1
    
    CDF(allIterations)
    # parity(allIterations)
        
def CDF(allIterations):
    allDiametersDict = np.array([])
    
    currentAlgorithm = ""
    
    for iteration in allIterations:
        for item in iteration:
            if "Current algorithm" in item[0]:
                currentAlgorithm = item[1]
                
            if "Diameter" in item[0]:
                number = int(item[0][-2:])
                
                position = number - 1
                
                if len(allDiametersDict) < number:
                    newDiametersDict = {}
                    allDiametersDict = np.concatenate((allDiametersDict, newDiametersDict), axis = None)
                
                diameter = int(float(item[1]))
                
                if diameter in allDiametersDict[position]:
                    allDiametersDict[position][diameter] += 1
                else:
                    allDiametersDict[position][diameter] = 1
                    
    current = 1

    for x in allDiametersDict:
        
        #CDF
        
        keys = list(x.keys())
        keys.sort()
        sortedX = {i: x[i] for i in keys}
        
        keys = np.array([])
        for item in list(sortedX.keys()):
            keys = np.concatenate((keys, item), axis = None)
        
        values = list(sortedX.values())
        
        total = 0
        for value in values:
            total += value
        
        for i in range(len(values)):
            if i == 0:
                values[i] = values[i] / total
            else:
                values[i] = values[i - 1] + (values[i] / total)
        
        outValues = []
        j = 0
        for i in range(13):
            if i + 1 in sortedX:
                outValues = np.concatenate((outValues, values[j]), axis = None)
                j += 1
            else:
                if i == 0:
                    outValues = np.concatenate((outValues, 0), axis = None)
                else:
                    outValues = np.concatenate((outValues, outValues[i - 1]), axis = None)
    
        fig,ax = plt.subplots()
        
        ax.bar(range(1, 14), outValues, width=1, edgecolor="white", linewidth = 0.7)
        
        # ax.set(xlim=(0, max(list(sortedX.keys())) + 1), xticks=np.arange(1, max(list(sortedX.keys())) + 1), ylim=(0, 1), yticks=np.arange(0, 1))
        
        # ax.ecdf(list(item.values()))
        
        # plt.show()

        if not os.path.exists(f"DataAnalysis/out/CDF"): 
            os.makedirs(f"DataAnalysis/out/CDF/")
        plt.savefig(f"DataAnalysis/out/CDF/{currentAlgorithm} {current}.png")
        plt.close()
        
        current += 1
        
def parity(allIterations):
    allRI = np.array([])
    allCosts = np.array([])
    
    currentAlgorithm = ""
    
    for iteration in allIterations:
        for item in iteration:
            if "Current algorithm" in item[0]:
                currentAlgorithm = item[1]
                
            elif "Cost" in item[0]:
                allCosts = np.concatenate((allCosts, float(item[1])), axis = None)
                print(item[1])
                
            elif "SumRI" in item[0]:
                allRI = np.concatenate((allRI, float(item[1])), axis = None)
                print(item[1])
                
                if(allCosts[-1] > 9999999.9):
                    allCosts = np.delete(allCosts, -1)
                    allRI = np.delete(allRI, -1)
                
    
    fig,ax = plt.subplots()
    
    # size and color:
    sizes = np.random.uniform(15, 80, len(allRI))
    colors = np.random.uniform(15, 80, len(allRI))
    
    ax.scatter(allRI, allCosts, s = sizes, c = colors, vmin = 0, vmax = 1000)

    if not os.path.exists(f"DataAnalysis/out/parity"): 
        os.makedirs(f"DataAnalysis/out/parity/")
    plt.savefig(f"DataAnalysis/out/parity/{currentAlgorithm}.png")
    plt.close()
        
            


def scanDirectory(directory):
    for entry in os.scandir("results"):
        if entry.is_file():
            analyseFile(entry)
        elif entry.is_dir():
            scanDirectory(entry)

if __name__ == '__main__':
    scanDirectory("results")
    pass