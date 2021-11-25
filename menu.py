from tkinter import *
import tkinter.font as font
import sys
import os
from model import Model

absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)


def StartSimulation():
    numberOfPpl = int(scale1.get())
    startingInfectiousPercentage = int(scale2.get())
    daysOfInfection = int(scale3.get())
    r0 = int(scale4.get())
    daysOfSimulation = int(scale5.get())*7
    if (checked.get()):
        modelType = "SIS"
    else:
        modelType = "SIR"
    resultsType = str(radioButtonSelection.get())
        
    window.destroy()
    model = Model(numberOfPpl, startingInfectiousPercentage, daysOfInfection, daysOfSimulation, r0, modelType, resultsType)
    

def CheckButtonClicked():
    if (checked.get()):
        mainLabel.config(text="SIS Model")
    else:
        mainLabel.config(text="SIR Model")
        
        
def HelpButtonClicked():
    helpWindow = Toplevel(window)
    helpWindow.title("Help")
    helpWindow.geometry("400x400")
    helpWindow.resizable(0,0)

    helpLabel = Label(
        helpWindow,
        text="Help",
        font = ("Arial", 40),
        pady = 10
    )
    helpLabel.pack()



    
window = Tk()
window.title("Εpidemiological Μodel")
window.geometry("840x590")
window.resizable(0,0)

mainLabel = Label(
    window,
    text="SIR Model",
    font = ("Arial", 40),
    pady = 10
)
mainLabel.grid(row=0, column=0, columnspan=3)

mainLabel2 = Label(
    window,
    text="Settings",
    font = ("Arial", 20)
)
mainLabel2.grid(row=1, column=0, columnspan=3)


buttonFont = font.Font(size=10)
helpIcon = PhotoImage(file = fileDirectory + "\\help.png")
helpButton = Button(window, image=helpIcon, font=buttonFont, height=35, width=35, command=HelpButtonClicked)
helpButton.grid(row=0, column=2, columnspan=1, sticky="E", padx=20)


label1 = Label(
    window,
    text="Population:",
    font = ("Arial", 15)
)
label1.grid(row=2, column=0)


scale1 = Scale(
    window,
    from_ = 100,
    to = 1000,
    resolution = 50,
    length = 500,
    width = 30,
    orient = HORIZONTAL
)
scale1.set(500)
scale1.grid(row=2, column=1, columnspan=2)




label2 = Label(
    window,
    text="Starting infectious population (%):",
    font = ("Arial", 15)
)
label2.grid(row=3, column=0, padx=10)

scale2 = Scale(
    window,
    from_ = 5,
    to = 20,
    resolution = 5,
    length = 500,
    width = 30,
    orient = HORIZONTAL
)
scale2.set(10)
scale2.grid(row=3, column=1, columnspan=2)





label3 = Label(
    window,
    text="Infectious period (days):",
    font = ("Arial", 15)
)
label3.grid(row=4, column=0)

scale3 = Scale(
    window,
    from_ = 1,
    to = 30,
    length = 500,
    width = 30,
    orient = HORIZONTAL
)
scale3.set(5)
scale3.grid(row=4, column=1, columnspan=2)



label4 = Label(
    window,
    text="Average infections per person:",
    font = ("Arial", 15)
)
label4.grid(row=5, column=0)

scale4 = Scale(
    window,
    from_ = 0.1,
    to = 10.0,
    resolution = 0.2,
    length = 500,
    width = 30,
    orient = HORIZONTAL
)
scale4.set(1.0)
scale4.grid(row=5, column=1, columnspan=2)



label5 = Label(
    window,
    text="Weeks of simulation:",
    font = ("Arial", 15)
)
label5.grid(row=6, column=0)

scale5 = Scale(
    window,
    from_ = 1,
    to = 52,
    length = 500,
    width = 30,
    orient = HORIZONTAL
)
scale5.set(1)
scale5.grid(row=6, column=1, columnspan=2)



checked = BooleanVar()
checkButtonFont = font.Font(size=15)
checkbutton = Checkbutton(window, text="People become susceptible again after infectious period", font=checkButtonFont, variable=checked, onvalue=True, offvalue=False, command=CheckButtonClicked)
checkbutton.grid(row=7, column=0, columnspan=3, pady=5)



radioButtonSelection = StringVar(window)

radioButtonLabel = Label(
    window,
    text="View results in:",
    font = ("Arial", 15)
)
radioButtonLabel.grid(row=8, column=0, pady=5)

radioButton1 = Radiobutton(window, text="Graph", variable=radioButtonSelection, value="graph", font = ("Arial", 15))
radioButton1.grid(row=8, column=1, pady=5)
radioButton1.select()

radioButton2 = Radiobutton(window, text="Pie Chart", variable=radioButtonSelection, value="pie", font = ("Arial", 15))
radioButton2.grid(row=8, column=2, pady=5)




buttonFont = font.Font(size=20)
button = Button(window, text="Start Simulation", font=buttonFont, height=1, width=20, command=StartSimulation)
button.grid(row=9, column=0, columnspan=3, pady=20)


window.mainloop()













