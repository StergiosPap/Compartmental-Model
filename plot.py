import matplotlib.pyplot as plt

def showPlot(x, y, y2=None, title=None, xlabel=None, ylabel=None):
    plt.figure().canvas.set_window_title("Εpidemiological Μodel")
    
    plt.plot(x[0], y[0], color="red", label="Infected")
    if (y2 is not None):
        plt.plot(x[0], y2[0], color="forestgreen", label="Recovered")    
    plt.legend()
    
    for i in range (len(x)):
        plt.plot(x[0:i+1], y[0:i+1], color="red")
        if (y2 is not None):
            plt.plot(x[0:i+1], y2[0:i+1], color="forestgreen")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # plt.xticks(range(i+2))
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
    

    
    
def Pie(x, title=None):
    plt.figure(figsize=(7, 4)).canvas.set_window_title("Εpidemiological Μodel")

    labels = ["Susceptible", "Infected", "Recovered"]
    colors = ["#2acaea", "red", "forestgreen"]
    
    plt.pie(x[0], colors=colors, startangle=90)    

    plt.legend(labels=labels, bbox_to_anchor=(0.98, 0.5), loc="center right", fontsize=9, bbox_transform=plt.gcf().transFigure)
    
    for i in range (len(x)):
        currentLabels = [labels[j] + ": " + str(round(x[i][j], 1)) + "%" for j in range (3)]

        plt.pie(x[i], colors=colors, startangle=90)
        plt.legend(labels=currentLabels, bbox_to_anchor=(0.98, 0.5), loc="center right", fontsize=9, bbox_transform=plt.gcf().transFigure)
        plt.title(title, fontsize=20)
        plt.suptitle("  Day " + str(i), y=0.13, fontsize=15)
        plt.pause(0.05)   


    plt.show() 
    
    
    

    
    
