import random
import math
import numpy as np
import plot
import matplotlib.pyplot as plt
import time
from numpy.random import choice
import routine as rt
from person import Person
from family import Family
from town import Town, House, School, Workplace, Hospital, Entertainment, Extracurricular, Transportation, Outdoors


class Model():
    def __init__(self, numberOfPpl=500, startingInfectiousPercentage=10, daysOfInfection=5, daysOfSimulation=7, r0=1, modelType="SIR", resultsType="graph"):
        self.numberOfPpl = numberOfPpl
        self.startingInfectiousPercentage = startingInfectiousPercentage
        self.daysOfInfection = daysOfInfection
        self.daysOfSimulation = daysOfSimulation
        self.r0 = r0
        self.modelType = modelType
        self.resultsType = resultsType
        
        self.currentDay = 0
        self.currentHour = 0
        
        self.locs = []
        
        self.StartSimulation(self.numberOfPpl, self.startingInfectiousPercentage, self.daysOfInfection, self.daysOfSimulation, self.r0)
        

        

    def CreateHouses(self):
        for i in range(self.familiesCreated):
            self.town.houses.append(House())


    def CreatePopulation(self, numberOfPeople):        
        while (self.peopleCreated < numberOfPeople):
            
            if (numberOfPeople-self.peopleCreated >= 5):
                numberOfFamilyMembers = choice([1, 2, 3, 4, 5], 1, p=[0.325, 0.312, 0.163, 0.136, 0.064])[0]
            else:
                numberOfFamilyMembers = numberOfPeople - self.peopleCreated
                
            #print (numberOfFamilyMembers)
            self.CreateFamily(numberOfFamilyMembers)
            #peopleCreated += numberOfFamilyMembers
            self.familiesCreated += 1



    def CreateFamily(self, numberOfFamilyMembers):
        for i in range (numberOfFamilyMembers):
            agegroup = choice(["Underage", "Young Adult", "Adult", "Middle Aged", "Elderly"], 1, p=[0.2035, 0.054, 0.192, 0.349, 0.2015])[0]
            self.CreatePerson(agegroup)
        
        
        
    def CreatePerson(self, agegroup):
        newPerson = Person(ID=self.peopleCreated, houseID=self.familiesCreated, agegroup=agegroup, town=self.town)
        self.people.append(newPerson)
        self.people_S.append(newPerson)
        self.peopleCreated = self.peopleCreated + 1
        
        

    #Returns the percentage of people with the given state ('S/I/R').
    def Percentage(self, state):
        if (state == "S"):
            return round(len(self.people_S)/self.peopleCreated*100, 2)
        elif (state == "I"):
            return round(len(self.people_I)/self.peopleCreated*100, 2)
        elif (state == "R"):
            return round(len(self.people_R)/self.peopleCreated*100, 2)
            
        return 0
        
        


    def InitRecoveryLog(self):
        for i in range(1, self.daysOfSimulation + self.daysOfInfection+2):
            self.recoveryLog[i] = []
       

    def ExecRecoveryLog(self):
        for person in self.recoveryLog[self.currentDay]:
            self.Recover(person)


    #Converts the state of the given person
    def Infect(self, person):
        self.recoveryLog[self.currentDay+self.daysOfInfection+1].append(person)
        
        self.people_S.remove(person)
        self.people_I.append(person)
        
        #print ("Infecting person: " + str(person.ID))
        #print ("Percentage: " + str(self.Percentage('I')))


    def Recover(self, person):    
        self.people_I.remove(person)

        if (self.modelType == "SIS"):
            self.people_S.append(person)
        elif (self.modelType == "SIR"):
            self.people_R.append(person)        
        
        #print ("Recovering person: " + str(person.ID))




    def FillBuildings(self):
        for person in self.people:
            location = person.routine[self.currentHour][0]
            locationID = person.routine[self.currentHour][1]
            
            if (location == "House"):
                self.town.houses[locationID].currentVisitors.append(person)
            elif (location == "School"):
                self.town.schools[locationID].currentVisitors.append(person)
            elif (location == "Workplace"):
                self.town.workplaces[locationID].currentVisitors.append(person)
            elif (location == "Transportation"):
                self.town.transportations[locationID].currentVisitors.append(person)
            elif (location == "Extracurricular"):
                self.town.extracurriculars[locationID].currentVisitors.append(person)
            elif (location == "Entertainment"):
                self.town.entertainments[locationID].currentVisitors.append(person)
            elif (location == "Outdoors"):
                self.town.outdoors[locationID].currentVisitors.append(person)
            elif (location == "Hospital"):
                self.town.hospitals[locationID].currentVisitors.append(person)





    def EmptyBuildings(self):
        for location in self.town.locations:
            location.currentVisitors.clear()
        



    def PeopleInteractions(self):    
        for infectedPerson in self.people_I:
            location = infectedPerson.routine[self.currentHour][0]
            locationID = infectedPerson.routine[self.currentHour][1]
            
            if (location == "House"):
                currentLocation = self.town.houses[locationID]
            elif (location == "School"):
                currentLocation = self.town.schools[locationID]
            elif (location == "Workplace"):
                currentLocation = self.town.workplaces[locationID]
            elif (location == "Transportation"):
                currentLocation = self.town.transportations[locationID]
            elif (location == "Extracurricular"):
                currentLocation = self.town.extracurriculars[locationID]
            elif (location == "Entertainment"):
                currentLocation = self.town.entertainments[locationID]
            elif (location == "Outdoors"):
                currentLocation = self.town.outdoors[locationID]
            elif (location == "Hospital"):
                currentLocation = self.town.hospitals[locationID]

            otherVisitors = [p for p in currentLocation.currentVisitors if p != infectedPerson]
            
            if (len(currentLocation.currentVisitors) > 0):
                
                if (len(currentLocation.currentVisitors) > math.ceil(infectedPerson.interactions[self.currentHour])):               
                    otherPeople = random.sample(otherVisitors, math.ceil(infectedPerson.interactions[self.currentHour]))
                else:
                    otherPeople = otherVisitors 

                for otherPerson in otherPeople:
                    self.Interaction(infectedPerson, otherPerson)
                    

    def Interaction(self, person1, person2):
        if (person2 not in self.people_S):
            return
            
        total_interactions = sum(person1.interactions) * self.daysOfInfection #Daily interactions * Infectious period
        

        if (random.random() <= 1/total_interactions):
            self.Infect(person2)
            self.UpdateLocs(person1.routine[self.currentHour][0])





    def RunSimulation(self, days):
        #At the beginning, infect x random people (Where x = startingInfectiousPopulation)...
        randomPeople = random.sample(self.people_S, self.startingInfectiousPopulation)
        for person in randomPeople:   
            self.Infect(person)
            
        self.percentagesPerDay.append([self.Percentage("S"), self.Percentage("I"), self.Percentage("R")])
        
        while (self.currentDay < days):
            self.currentDay += 1
            self.currentHour = 0
            print ("Day " + str(self.currentDay))
            
            for i in range(24):
                self.EmptyBuildings()
                self.FillBuildings()
                self.PeopleInteractions()
                self.currentHour += 1

                
            self.ExecRecoveryLog()           
            self.percentagesPerDay.append([self.Percentage("S"), self.Percentage("I"), self.Percentage("R")])
            #self.percentagesPerDay.append([len(self.people_S)/len(self.people), len(self.people_I)/len(self.people), len(self.people_R)/len(self.people)])



    def StartSimulation(self, numberOfPpl, startingInfectiousPercentage, daysOfInfection, daysOfSimulation, r0):
        self.startingInfectiousPopulation = round(numberOfPpl*startingInfectiousPercentage/100)
        
        self.peopleCreated = 0
        self.familiesCreated = 0

        self.people = []
        self.people_S = []
        self.people_I = []
        self.people_R = []
     
        self.percentagesPerDay = []
        
        self.recoveryLog = {}
        self.InitRecoveryLog()

        self.town = Town(numberOfPpl)

        self.CreatePopulation(numberOfPpl)

        self.CreateHouses()

        self.town.locations = self.town.houses + self.town.schools + self.town.workplaces + self.town.hospitals + self.town.entertainments + self.town.transportations + self.town.extracurriculars + self.town.outdoors

        self.emergencyLevel = 0

        self.RunSimulation(daysOfSimulation)

        self.PrintLocs()
        
        self.ShowResults()
        
        
    def ShowResults(self):
        if (self.resultsType == "graph"):
            if (self.modelType == "SIR"):
                plot.showPlot(list(range(0,self.daysOfSimulation+1)), [item[1] for item in self.percentagesPerDay], [item[2] for item in self.percentagesPerDay], xlabel="Days", ylabel="Percentage", title="Simulation Results")
            elif (self.modelType == "SIS"):
                plot.showPlot(list(range(0,self.daysOfSimulation+1)), [item[1] for item in self.percentagesPerDay], xlabel="Days", ylabel="Percentage", title="Simulation Results")
        elif (self.resultsType == "pie"):
            plot.Pie(np.array(self.percentagesPerDay),  title="Simulation Results")
        
        
    def UpdateLocs(self, location):
        if (location == "House"):
            self.locs.append(1)
        elif (location == "School"):
            self.locs.append(2)
        elif (location == "Workplace"):
            self.locs.append(3)
        elif (location == "Transportation"):
            self.locs.append(4)
        elif (location == "Extracurricular"):
            self.locs.append(5)
        elif (location == "Entertainment"):
            self.locs.append(6)
        elif (location == "Outdoors"):
            self.locs.append(7)
        elif (location == "Hospital"):
            self.locs.append(8)
            

    def PrintLocs(self):
        print ("House: " + str(self.locs.count(1)))
        print ("School: " + str(self.locs.count(2)))
        print ("Workplace: " + str(self.locs.count(3)))
        print ("Transportation: " + str(self.locs.count(4)))
        print ("Extracurricular: " + str(self.locs.count(5)))
        print ("Entertainment: " + str(self.locs.count(6)))
        print ("Outdoors: " + str(self.locs.count(7)))
        print ("Hospital: " + str(self.locs.count(8)))
        
        
        
    
#model = Model(1000, 5, 4, 105, 5, "SIR", "graph")



