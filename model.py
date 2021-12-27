import random
import math
import numpy as np
import plot
import matplotlib.pyplot as plt
import time
from numpy.random import choice
import routine as rt
from person import Person
from town import Town, House, School, Workplace, Hospital, Entertainment, Extracurricular, Transportation, Outdoors
from progressbar import printProgressBar

class Model():
    '''
    Class that manages the simulation. Creates objects for each location and person, then runs the simulation with the given parameters.
    
    numberOfPpl: Number of the town's residents.
    startingInfectiousPercentage: Infectious percentage for day 0.
    daysOfInfection: Infectious period. Number of days from infection to recovery.
    daysOfSimulation: Days to run the simulation.
    r0: Basic reproduction number. Average number of people that each sick person will infect.
    modelType: SIR or SIS model.
    resultsType: View results in Graph or Pie Chart.
    '''

    def __init__(self, numberOfPpl=500, startingInfectiousPercentage=10, daysOfInfection=5, daysOfSimulation=7, r0=1.0, modelType="SIR", resultsType="graph"):
        self.numberOfPpl = numberOfPpl
        self.startingInfectiousPercentage = startingInfectiousPercentage
        self.daysOfInfection = daysOfInfection
        self.daysOfSimulation = daysOfSimulation
        self.r0 = r0
        self.modelType = modelType
        self.resultsType = resultsType
        
        self.currentDay = 0 # Day counter
        self.currentHour = 0 # Hour counter
        
        self.CreateObjects(self.numberOfPpl, self.startingInfectiousPercentage, self.daysOfInfection, self.daysOfSimulation, self.r0)
        
 

    def CreateHouses(self):
        '''
        Creates a "House" object for each family.
        '''
        for i in range(self.familiesCreated):
            self.town.houses.append(House())


    def CreatePopulation(self, numberOfPeople):
        '''
        Creates the town's population with the given size (numberOfPpl).
        '''
        while (self.peopleCreated < numberOfPeople):            
            if (numberOfPeople-self.peopleCreated >= 5):
                numberOfFamilyMembers = choice([1, 2, 3, 4, 5], 1, p=[0.325, 0.312, 0.163, 0.136, 0.064])[0] # Random choice for family members. Percentages based on studies.
            else:
                numberOfFamilyMembers = numberOfPeople - self.peopleCreated
                
            self.CreateFamily(numberOfFamilyMembers)
            self.familiesCreated += 1


    def CreateFamily(self, numberOfFamilyMembers):
        '''
        Creates family members.
        '''
        for i in range (numberOfFamilyMembers):
            agegroup = choice(["Underage", "Young Adult", "Adult", "Middle Aged", "Elderly"], 1, p=[0.2035, 0.054, 0.192, 0.349, 0.2015])[0] # Random choice for person's age group. Percentages based on studies.
            self.CreatePerson(agegroup)


    def CreatePerson(self, agegroup):
        '''
        Creation of Person object. houseID is the current family's number. In other words, how many families have been created so far.
        '''
        newPerson = Person(ID=self.peopleCreated, houseID=self.familiesCreated, agegroup=agegroup, town=self.town)
        self.people.append(newPerson)
        self.people_S.append(newPerson) # Susceptible by default.
        self.peopleCreated = self.peopleCreated + 1



    def Percentage(self, state):
        '''
        Returns the percentage of people with the given state ('S/I/R').
        '''        
        if (state == "S"):
            return round(len(self.people_S)/self.peopleCreated*100, 2)
        elif (state == "I"):
            return round(len(self.people_I)/self.peopleCreated*100, 2)
        elif (state == "R"):
            return round(len(self.people_R)/self.peopleCreated*100, 2)
            
        return 0
        


    def InitRecoveryLog(self):
        '''
        Initialization of recoveryLog (dictionary of people who recover at the end of each day).
        Key: day number
        Value: list with "Person" objects that need to be recovered
        '''
        for i in range(1, self.daysOfSimulation + self.daysOfInfection+2):
            self.recoveryLog[i] = [] # Empty list for each day of simulation.
       

    def ExecRecoveryLog(self):
        '''
        Checks if there are any people who need to recover today and executes the command.
        '''
        for person in self.recoveryLog[self.currentDay]:
            self.Recover(person)

   
   
    def InitHospitalizationLog(self):
        '''
        Initialization of hospitalizationLog (dictionary of people who need to be hospitalized at the end of each day).
        Key: day number
        Value: list with "Person" objects that need to be hospitalized
        '''
        for i in range(0, self.daysOfSimulation + self.daysOfInfection+2):
            self.hospitalizationLog[i] = [] # Empty list for each day of simulation.
       

    def ExecHospitalizationLog(self):
        '''
        Checks if there are any people who need to be hospitalized today and executes the command.
        '''
        for person in self.hospitalizationLog[self.currentDay]:
            person.Hospitalize()



    def Infect(self, person):
        '''
        Converts the state of the given person from Susceptible to Infected and checks if they will need hospitalization.
        '''
        self.recoveryLog[self.currentDay+self.daysOfInfection+1].append(person)
        
        self.people_S.remove(person)
        self.people_I.append(person)
        
        '''
        Hospitalization:
        First, we set an arbitrary value for the base percentage of people that will need medical care.
        Then, the percentage increases depending on the person's age (healthFactor).        
        For example, 66+ y.o. people are 9.67 times more likely to need medical care than the base case (25- y.o. people).
        If the person is decided to need medical care he is hospitalized exactly D days after his infection, where D = ceil(infectious_period * 1/3).
        '''                
        hospitalizationPercentage = 1
        hospitalizationPercentage = hospitalizationPercentage * person.healthFactor
        
        if (random.random()*100 <= hospitalizationPercentage):
            dayOfHospitalization = math.ceil(self.daysOfInfection*1/3)
            self.hospitalizationLog[dayOfHospitalization].append(person)


    def Recover(self, person):
        '''
        Converts the state of the given person from Infected to Recovered (or Susceptible, depending on the model type).
        '''    
        self.people_I.remove(person)

        if (self.modelType == "SIS"):
            self.people_S.append(person)
        elif (self.modelType == "SIR"):
            self.people_R.append(person)        
        
        if (person.isHospitalized): # If the person was hospitalized, they are discharged and return to their daily routine.
            person.ModifyRoutine(self.emergencyLevel)        
            person.isHospitalized = False



    def FillBuildings(self):
        '''
        Fills each location's list with "Person" objects that should be there during the current hour.
        '''
        for person in self.people:
            location = person.routine[self.currentHour][0]
            locationID = person.routine[self.currentHour][1]
            
            if (location == "School"):
                self.town.schools[locationID].currentVisitors.append(person)
            elif (location == "Workplace"):
                self.town.workplaces[locationID].currentVisitors.append(person)
            elif (location == "Transportation"):
                if (not self.town.transportations[locationID].IsFull(self.emergencyLevel)): # Transportation is not full.
                    self.town.transportations[locationID].currentVisitors.append(person)
                else: # If transportation is full, move by foot.
                    self.town.outdoors[0].currentVisitors.append(person)
            elif (location == "Extracurricular"):
                self.town.extracurriculars[locationID].currentVisitors.append(person)
            elif (location == "Entertainment" and not self.town.entertainments[locationID].IsFull(self.emergencyLevel)): # If the place is full, the person stays at home.
                self.town.entertainments[locationID].currentVisitors.append(person)
            elif (location == "Outdoors"):
                self.town.outdoors[locationID].currentVisitors.append(person)
            elif (location == "Hospital"):
                self.town.hospitals[locationID].currentVisitors.append(person)
            else:
                self.town.houses[person.houseID].currentVisitors.append(person)


    def EmptyBuildings(self):
        '''
        Clears each location's current visitors.
        '''
        for location in self.town.locations:
            location.currentVisitors.clear()
        


    def PeopleInteractions(self):
        '''
        Each infectious person interacts with other people in the same location.
        The number of "other people" is based on the location and the Emergency Level.
        '''    
        for infectedPerson in self.people_I:
            location = infectedPerson.routine[self.currentHour][0]
            locationID = infectedPerson.routine[self.currentHour][1]
            
            # Get the person's location.
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

            otherVisitors = [p for p in currentLocation.currentVisitors if p != infectedPerson] # People in the same location (except the person itself).
            
            if (len(currentLocation.currentVisitors) > 0): # If the person is not alone in the location...
                sdf = 1 - 0.2 * self.emergencyLevel # Social Distacing Factor
                numberOfInteractions = math.ceil(infectedPerson.interactions[self.currentHour] * sdf)
                numberOfInteractions = math.ceil(numberOfInteractions * infectedPerson.legalityFactor)
                
                if (len(currentLocation.currentVisitors) > numberOfInteractions):               
                    otherPeople = random.sample(otherVisitors, numberOfInteractions)
                else: # Interact with all of them.
                    otherPeople = otherVisitors 

                for otherPerson in otherPeople:
                    self.Interaction(infectedPerson, otherPerson, location)
                    

                    
    def Interaction(self, person1, person2, location):
        '''
        person1 (I) "interacts" with person2 (S) and has a possibility to infect them.
        '''
        
        if (person2 not in self.people_S): # Continue only if the second person is Susceptible.
            return
            
        total_interactions = sum(person1.interactions) * self.daysOfInfection # Total number of person1's interactions during the infectious period (Daily interactions * Infectious period).
        
        transmission_chance = self.r0/total_interactions # Chance for transmission for each person that interacts with "person1" (r0 / person1's total interactions).
        
        transmission_chance = transmission_chance * person1.hygieneFactor * person2.hygieneFactor # The chance is affected by both people's hygiene factor.

        # For each person wearing a mask, the transmission chance is reduced by 80%.
        if (person1.IsWearingMask(location, self.emergencyLevel)):
            transmission_chance = transmission_chance * 0.2
            
        if (person2.IsWearingMask(location, self.emergencyLevel)):
            transmission_chance = transmission_chance * 0.2

        
        if (random.random() <= transmission_chance):
            self.Infect(person2)
            


    def SetEmergencyLevel(self):
        '''
        Sets the current day's Emergency Level depending on the infectious percentage.
        '''    
        percentage_I = self.Percentage("I") # Percentage of infectious people at the start of the day.
        
        if (percentage_I < 5):
            if (self.emergencyLevel > 0): # Cannot drop back to Level 0.
                newEmergencyLevel = 1
            else:
                newEmergencyLevel = 0
        elif (percentage_I < 10):
            newEmergencyLevel = 1
        elif (percentage_I < 20):
            newEmergencyLevel = 2
        elif (percentage_I >= 20):
            newEmergencyLevel = 3
            
        if (newEmergencyLevel != self.emergencyLevel): # If the Emergency Level changed, modify each person's schedule.
            for person in self.people:
                person.ModifyRoutine(newEmergencyLevel)
                
        self.emergencyLevel = newEmergencyLevel


        
    def RunSimulation(self, days):
        # At the beginning, infect x random people (Where x = startingInfectiousPopulation)...
        randomPeople = random.sample(self.people_S, self.startingInfectiousPopulation)
        for person in randomPeople:   
            self.Infect(person)
            
        self.percentagesPerDay.append([self.Percentage("S"), self.Percentage("I"), self.Percentage("R")]) # Day 0 percentages
        self.emergencyLevelsPerDay.append(0)
        
        while (self.currentDay < days): # Days loop
            self.currentDay += 1
            self.currentHour = 0
            printProgressBar(self.currentDay, self.daysOfSimulation, prefix = 'Running Simulation...', length = 50) # Update the progress bar.
            
            self.SetEmergencyLevel() # Update Emergency Level depending on the infectious percentage.
            self.emergencyLevelsPerDay.append(self.emergencyLevel) # Update emergencyLevels
            self.percentagesPerDay.append([self.Percentage("S"), self.Percentage("I"), self.Percentage("R")]) # Update percentagesPerDay

            for i in range(24): # Hours loop
                self.EmptyBuildings()
                self.FillBuildings()
                self.PeopleInteractions()
                self.currentHour += 1

            self.ExecRecoveryLog() # Check if there are people that should recover.
            self.ExecHospitalizationLog() # Check if there are people that should be hospitalized.



    def CreateObjects(self, numberOfPpl, startingInfectiousPercentage, daysOfInfection, daysOfSimulation, r0):
        '''
        Creates objects for each location and person.
        '''
        self.startingInfectiousPopulation = round(numberOfPpl*startingInfectiousPercentage/100) # Converting percentage to number.
        
        self.peopleCreated = 0
        self.familiesCreated = 0

        # Initializing lists that will contain "Person" objects.
        self.people = [] # All people
        self.people_S = [] # Susceptible people
        self.people_I = [] # Infectious people
        self.people_R = [] # Recovered people
     
        # Lists that store the simulation results per day.
        self.percentagesPerDay = []
        self.emergencyLevelsPerDay = []

        self.recoveryLog = {} # Dictionary that stores the people that need to recover at the end of each day. Key: number of day, Value: list of "Person" objects.
        self.InitRecoveryLog()

        self.hospitalizationLog = {} # Dictionary that stores the people that need to get hospitalized at the end of each day. Key: number of day, Value: list of "Person" objects.
        self.InitHospitalizationLog()

        self.town = Town(numberOfPpl) # Creation of Town object

        self.CreatePopulation(numberOfPpl) # Creation of Person objects

        self.CreateHouses() # Creation of House objects (one for each family)

        self.town.locations = self.town.houses + self.town.schools + self.town.workplaces + self.town.hospitals + self.town.entertainments + self.town.transportations + self.town.extracurriculars + self.town.outdoors # Gathering all created locations in a single list.

        self.emergencyLevel = 0
        
        printProgressBar(0, self.daysOfSimulation, prefix = 'Running Simulation...', length = 50) # Initialization of progress bar.

        self.RunSimulation(daysOfSimulation)

        self.ShowResults()
        
        
        
    def ShowResults(self):
        '''
        Displays the simulation results.
        '''
        if (self.resultsType == "graph"):
            if (self.modelType == "SIR"):
                plot.showPlot(list(range(0,self.daysOfSimulation+1)), [item[1] for item in self.percentagesPerDay], [item[2] for item in self.percentagesPerDay], emergencyLevels=self.emergencyLevelsPerDay, xlabel="Days", ylabel="Percentage", title="Simulation Results")
            elif (self.modelType == "SIS"):
                plot.showPlot(list(range(0,self.daysOfSimulation+1)), [item[1] for item in self.percentagesPerDay], emergencyLevels=self.emergencyLevelsPerDay, xlabel="Days", ylabel="Percentage", title="Simulation Results")
        elif (self.resultsType == "pie"):
            plot.showPieChart(np.array(self.percentagesPerDay), emergencyLevels=self.emergencyLevelsPerDay, title="Simulation Results")
        
        

    
#model = Model(numberOfPpl=1000, startingInfectiousPercentage=5, daysOfInfection=5, daysOfSimulation=30, r0=2, modelType="SIR", resultsType="graph")


