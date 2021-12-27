import matplotlib.pyplot as plt

def showPlot(x, y, y2=None, emergencyLevels=None, title=None, xlabel=None, ylabel=None):
    '''
    Displays the simulation results as a plot function, using matplotlib.pyplot.plot.
    
    x: Days
    y: Infectious percentage per day 
    y2: Recovered percentage per day (only in SIR model)
    emergencyLevels: Emergency Level per day
    '''
    
    plt.figure().canvas.set_window_title("Εpidemiological Μodel")
    
    plt.plot(x[0], y[0], color="red", label="Infected")
    if (y2 is not None):
        plt.plot(x[0], y2[0], color="forestgreen", label="Recovered")       
    plt.legend() 
    
    for i in range (len(x)):
        plt.plot(x[0:i+1], y[0:i+1], color="red") # Infectious percentages
        if (y2 is not None):
            plt.plot(x[0:i+1], y2[0:i+1], color="forestgreen") # Recovered percentages
        
        if (emergencyLevels is not None):
            '''
            Every time the Emergency Level changes, show a vertical dashed line.
            The higher the Emergency Level, the darker the line's color.
            '''
            if (emergencyLevels[i] == 1):
                if (emergencyLevels[i-1] != 1):
                    plt.vlines(i, 0, 100, linestyles ="dashed", colors="gold", alpha=0.7, label="Level 1")
            if (emergencyLevels[i] == 2):
                if (emergencyLevels[i-1] != 2):
                    plt.vlines(i, 0, 100, linestyles ="dashed", colors="orange", alpha=0.5, label="Level 2")
            if (emergencyLevels[i] == 3):
                if (emergencyLevels[i-1] != 3):
                    plt.vlines(i, 0, 100, linestyles ="dashed", colors="red", alpha=0.5, label="Level 3")

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if (i<15):
            plt.xticks(range(i+2))
        elif (i<61):
            plt.xticks(range(0, i+2, 7))
        else:
            plt.xticks(range(0, i+2, 30))
        plt.yticks(range(0,110,10))
        plt.pause(0.05)

    plt.show(block=False)
    return
    

    
def showPieChart(x, emergencyLevels=None, title=None):
    '''
    Displays the simulation results as a pie chart, using matplotlib.pyplot.pie.
    
    x: List with 3 elements. Susceptible/Infectious/Recovered percentage per day.
    emergencyLevels: Emergency Level per day
    '''
    
    plt.figure(figsize=(7, 4)).canvas.set_window_title("Εpidemiological Μodel")

    labels = ["Susceptible", "Infectious", "Recovered"]
    colors = ["#2acaea", "red", "forestgreen"]
    
    plt.pie(x[0], colors=colors, startangle=90)    

    plt.legend(labels=labels, bbox_to_anchor=(0.98, 0.5), loc="center right", fontsize=9, bbox_transform=plt.gcf().transFigure)
    
    for i in range (len(x)):
        currentLabels = [labels[j] + ": " + str(round(x[i][j], 1)) + "%" for j in range (3)]

        plt.pie(x[i], colors=colors, startangle=90)
        plt.legend(labels=currentLabels, bbox_to_anchor=(0.98, 0.5), loc="center right", fontsize=9, bbox_transform=plt.gcf().transFigure)
        plt.title(title, fontsize=20)
        if (emergencyLevels is None):
            plt.suptitle("  Day " + str(i), y=0.13, fontsize=15)
        else:
            plt.suptitle("  Day " + str(i) + "\n   Emergency Level: " + str(emergencyLevels[i]), y=0.13, fontsize=15)
        plt.pause(0.1)   

    plt.show()
    return




