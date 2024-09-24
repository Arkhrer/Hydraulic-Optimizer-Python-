
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

def analyseFile(file, option):
    reader = csv.reader(open(file, encoding = "utf-8"))
    
    line_count = 0
    
    allIterations = np.array([])
    
    for line in reader:
        if (line_count % 2) == 0:
            labels = line
            line_count += 1
        else:
            line = zip(labels, line)
                
            allIterations = np.concatenate((allIterations, line), axis = None)
            
            line_count += 1
    if (option == "CDF"):
        CDF(allIterations)
    elif (option == "Parity"):
        parity(allIterations)
        
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

        valuesum = 0
        
        for i in range(len(values)):
            if i == 0:
                valuesum = valuesum + values[i]
                values[i] = valuesum / total
            else:
                valuesum = valuesum + values[i]
                values[i] = valuesum / total
                # values[i] = values[i - 1] + (values[i] / total)

        outValues = [0.0]
        j = 0
        for i in range(13):
            if i in sortedX:
                if i != 12:
                    outValues = np.concatenate((outValues, values[j]), axis = None)
                    j += 1
                else:
                    outValues = np.concatenate((outValues, 1.0), axis = None)
                    j += 1
            else:
                if i == 0:
                    outValues = np.concatenate((outValues, 0), axis = None)
                else:
                    outValues = np.concatenate((outValues, outValues[-1]), axis = None)
    
        fig,ax = plt.subplots()
        
        # ax.bar(range(1, 14), outValues, width=1, edgecolor="white", linewidth = 0.7)

        # ax.stairs(outValues, linewidth = 3, color = "#3CB371")
        ax.plot(outValues, linewidth = 3, color = "#3CB371")
        ax.set(xlim=(0, 13), ylim = (0.0,1.0), xlabel = "Diameter index", ylabel = "Probability", title = f"{currentAlgorithm} {current}")
        ax.grid(True, axis = 'y')
        
        # ax.set(xlim=(0, max(list(sortedX.keys())) + 1), xticks=np.arange(1, max(list(sortedX.keys())) + 1), ylim=(0, 1), yticks=np.arange(0, 1))
        
        # ax.ecdf(list(item.values()))
        
        # plt.show()

        if not os.path.exists(f"DataAnalysis/out/CDF"): 
            os.makedirs(f"DataAnalysis/out/CDF/")
        plt.savefig(f"DataAnalysis/out/CDF/{currentAlgorithm} {current}.png")
        plt.close()
        
        current += 1
        
def parity(allIterations):
    currentcolor = 0
    prevSeed = ""
    colors = {0 : '#00bfff',
    1 : '#8f6f84',
    2 : '#e36b17',  
    3 : '#2ca719',
    4 : '#daae0e',
    5 : '#f40010',
    6 : '#2d1fe3'
    }

    totalMinutes: float = 0
    totalSeconds: float = 0

    coloredSeed = dict()

    allRI = np.array([])
    allCosts = np.array([])
    
    currentAlgorithm = ""
    
    fig,ax = plt.subplots()

    ax.set(xlim=(0, 80), ylim=(0, 3000000), ylabel = "Cost ($)", xlabel = "RI", title = currentAlgorithm)
    ax.grid(True, axis = 'y')
    
    for iteration in allIterations:
        for item in iteration:
            if "Minutes" in item[0]:
                totalMinutes += float(item[1])
            if "Seconds" in item[0]:
                totalSeconds += float(item[1])

            if "Current algorithm" in item[0]:
                currentAlgorithm = item[1]

            elif "Seed" in item[0]:
                if item[1] != prevSeed:
                    if prevSeed != "":
                        ax.scatter(allRI, allCosts, c = colors[coloredSeed[prevSeed]], alpha = 0.3, s = 10)
                    
                    if item[1] not in coloredSeed:
                        coloredSeed[item[1]] = currentcolor
                        currentcolor += 1

                    #ax.scatter(allRI, allCosts, c = '#00bfff', s = 10)
                    allRI = np.array([])
                    allCosts = np.array([])
                    prevSeed = item[1]
                
                    
            elif "Cost" in item[0]:
                allCosts = np.concatenate((allCosts, float(item[1])), axis = None)
                
            elif "SumRI" in item[0]:
                allRI = np.concatenate((allRI, float(item[1])), axis = None)
                
                if(allCosts[-1] > 9999999.9):
                    allCosts = np.delete(allCosts, -1)
                    allRI = np.delete(allRI, -1)
                
    
    # ax.scatter(allRI, allCosts, s = sizes, c = colors, vmin = 0, vmax = 1000)
    ax.scatter(allRI, allCosts, c = colors[coloredSeed[prevSeed]], alpha = 0.3, s = 10)
    # ax.set(xlim=(0, 80), ylim=(0, 3000000), ylabel = "Cost ($)", xlabel = "RI", title = currentAlgorithm)
    # ax.grid(True, axis = 'y')

    if not os.path.exists(f"DataAnalysis/out/parity"): 
        os.makedirs(f"DataAnalysis/out/parity/")
    plt.savefig(f"DataAnalysis/out/parity/{currentAlgorithm}.png")
    plt.close()

    extraMinutes = int(totalSeconds/60)
    totalMinutes += extraMinutes
    totalSeconds -= extraMinutes*60
    totalHours = int(totalMinutes/60)
    totalMinutes -= totalHours * 60

    if not os.path.exists(f"DataAnalysis/out/time"): 
        os.makedirs(f"DataAnalysis/out/time/")
    f = open(f"DataAnalysis/out/time/{currentAlgorithm}_time", "w")
    f.write(f"{totalHours} horas, {totalMinutes} minutos e {totalSeconds} segundos")
        
            


def scanDirectory(directory):
    for entry in os.scandir("results"):
        if entry.is_file():
            analyseFile(entry, "CDF")
            analyseFile(entry, "Parity")
        elif entry.is_dir():
            scanDirectory(entry)

if __name__ == '__main__':
    scanDirectory("results")
    pass