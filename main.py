import random
import math
import numpy as np
import plot
import time
from numpy.random import choice
import routine as rt
from person import Person
from family import Family
from town import Town, House, School, Workplace, Hospital, Entertainment, Extracurricular, Transportation, Outdoors




def CreateHouses():
    for i in range(familiesCreated):
        town.houses.append(House())


def CreatePopulation(numberOfPeople):   
    global familiesCreated, peopleCreated    
    
    while (peopleCreated < numberOfPeople):
        
        if (numberOfPeople-peopleCreated >= 5):
            numberOfFamilyMembers = choice([1, 2, 3, 4, 5], 1, p=[0.325, 0.312, 0.163, 0.136, 0.064])[0]
        else:
            numberOfFamilyMembers = numberOfPeople - peopleCreated
            
        #print (numberOfFamilyMembers)
        CreateFamily(numberOfFamilyMembers)
        #peopleCreated += numberOfFamilyMembers
        familiesCreated += 1



def CreateFamily(numberOfFamilyMembers):
    for i in range (numberOfFamilyMembers):
        agegroup = choice(["Underage", "Young Adult", "Adult", "Middle Aged", "Elderly"], 1, p=[0.2035, 0.054, 0.192, 0.349, 0.2015])[0]
        CreatePerson(agegroup)
    
    
    
def CreatePerson(agegroup):
    global peopleCreated    
    newPerson = Person(ID=peopleCreated, houseID=familiesCreated, agegroup=agegroup, town=town)
    people.append(newPerson)
    people_S.append(newPerson)
    peopleCreated = peopleCreated + 1
    
    
    



#Returns the percentage of people with the given state ('S/I/R').
def Percentage(state):
    count = 0
    
    if (state == "S"):
        return round(len(people_S)/peopleCreated*100, 2)
    elif (state == "I"):
        return round(len(people_I)/peopleCreated*100, 2)
    elif (state == "R"):
        return round(len(people_R)/peopleCreated*100, 2)
        
    return 0
    
    


def InitRecoveryLog():
    for i in range(1, daysOfSimulation+daysOfInfection+2):
        recoveryLog[i] = []
   

def ExecRecoveryLog():
    for person in recoveryLog[currentDay]:
        Recover(person)


#Converts the state of the given person
def Infect(person):
    recoveryLog[currentDay+daysOfInfection+1].append(person)
    
    people_S.remove(person)
    people_I.append(person)
    
    print ("Infecting person: " + str(person.ID))
    print ("Percentage: " + str(Percentage('I')))


def Recover(person):    
    people_I.remove(person)
    people_R.append(person)
    
    print ("Recovering person: " + str(person.ID))




def FillBuildings():
    for person in people:
        location = person.routine[currentHour][0]
        locationID = person.routine[currentHour][1]
        
        if (location == "House"):
            town.houses[locationID].currentVisitors.append(person)
        elif (location == "School"):
            town.schools[locationID].currentVisitors.append(person)
        elif (location == "Workplace"):
            town.workplaces[locationID].currentVisitors.append(person)
        elif (location == "Transportation"):
            town.transportations[locationID].currentVisitors.append(person)
        elif (location == "Extracurricular"):
            town.extracurriculars[locationID].currentVisitors.append(person)
        elif (location == "Entertainment"):
            town.entertainments[locationID].currentVisitors.append(person)
        elif (location == "Outdoors"):
            town.outdoors[locationID].currentVisitors.append(person)





def EmptyBuildings():
    for location in town.locations:
        location.currentVisitors.clear()
    



def PeopleInteractions():
    '''
    For each location in the town (each house, school, building, outside, etc):    
    
    '''
    
    for location in town.locations:
        for visitor1 in location.currentVisitors:
            #visitor2 = random.choice(location.currentVisitors)
            
            if (len(location.currentVisitors)>1):            
                otherVisitors = [p for p in location.currentVisitors if p != visitor1]
                
                visitor2 = random.choice(otherVisitors)
                
                Interaction(visitor1, visitor2)
                
                # if (visitor1 in people_I and visitor2 in people_S and random.randint(1,100)<21):
                    # Infect(visitor2)

                    
                    
                    
def Interaction(person1, person2):
    if (person1 not in people_I or person2 not in people_S):
        return
        
    total_interactions = person1.interactions * daysOfInfection #Daily interactions * Infectious period
    
    if (random.random() <= 1/total_interactions):
        Infect(person2)








def RunSimulation(days):
    global currentDay
    global currentHour
    currentDay = 0
    currentHour = 0
    
    #Infecting x random people (x == startingInfectiousPopulation)...
    randomPeople = random.sample(people_S, startingInfectiousPopulation)
    for person in randomPeople:   
        Infect(person)
        
    infectedPerDay.append(Percentage("I"))
    
    while (currentDay < days):
        currentDay += 1
        currentHour = 0
        print ("Day " + str(currentDay))
        
        for i in range(24):
            EmptyBuildings()
            FillBuildings()
            PeopleInteractions()
            currentHour += 1
            pass
            
        ExecRecoveryLog()
        infectedPerDay.append(Percentage("I"))





numberOfPpl = 1000
daysOfInfection = 7
daysOfSimulation = 30
r0 = 1

startingInfectiousPercentage = 10
startingInfectiousPopulation = round(numberOfPpl/startingInfectiousPercentage)

peopleCreated = 0
familiesCreated = 0

people = []
people_S = []
people_I = []
people_R = []

infectedPerDay = []
recoveryLog = {}
InitRecoveryLog()

town = Town(numberOfPpl)

CreatePopulation(numberOfPpl)

CreateHouses()


town.locations = town.houses + town.schools + town.workplaces + town.hospitals + town.entertainments + town.transportations + town.extracurriculars + town.outdoors


emergencyLevel = 0


RunSimulation(daysOfSimulation)


plot.showPlot(list(range(0,daysOfSimulation+1)), infectedPerDay, xlabel="Days", ylabel="Percentage of infected", title="Simulation Results")






