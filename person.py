import numpy as np
import random
from town import Town

class Person:
    '''
    ID: Unique identifier for each object.
    House ID: Represents the person's home ID. People in the same family have the same House ID.    
    Agegroups:  18-: Underage
                19-25: Young Adult
                26-40: Adult
                41-65: Middle Aged
                66+: Elderly
    Health Factor: Determines the person's likelihood of being hospitalized during their illness period. It is entirely age-dependent.
    Hygiene Factor: 
    Legality Factor: Determines the person's likelihood to obey the government's protection measures during the pandemic.
    '''

    def __init__(self, ID=None, houseID=None, agegroup=None, town=None):
        self.ID = ID
        self.houseID = houseID
        self.agegroup = agegroup
        self.town = town
        
        self.healthFactor = self.CreateHealthFactor(self)
        self.hygieneFactor = self.NormalDistributionFactor(mean=1.0, sd=0.7)
        self.legalityFactor = self.NormalDistributionFactor(mean=1.0, sd=0.7)
        
        self.routine = self.CreateRoutine(self)
        self.interactions = self.ExpectedDailyInteractions(self.routine)
        
        
    def CreateRoutine(self, person):
        '''
        Creates the daily routine of a person by calling the appropriate function. The schedule is generated in the constructor (Person) and it is age dependent. 
        
        "schedule" is a list of 24 elements. Each one represents the person's action for that specific hour.
        
        ex: schedule[2] = ['House', 27] means that the person spends every day from 02:00 to 02:59 in house #27 (probably their home).    
        '''

        if (person.agegroup == "Underage"):
            schedule = self.CreateRoutineUnderage(person)
            
        elif (person.agegroup == "Young Adult"):
            schedule = self.CreateRoutineYoungAdult(person)
            
        elif (person.agegroup == "Adult"):
            schedule = self.CreateRoutineAdult(person)
            
        elif (person.agegroup == "Middle Aged"):
            schedule = self.CreateRoutineMiddleAged(person)
            
        else: #Elderly  
            schedule = self.CreateRoutineElderly(person)

        return schedule


    def CreateRoutineUnderage(self, person):
        #Initialization
        routine = [None] * 24
        for i in range(24): #Default
            routine[i] = ['House', person.houseID]
            
        routine[8] = ['Outdoors', 0]
        
        #School in the morning
        schoolID = random.randint(0, len(person.town.schools)) - 1
        for i in range(9, 15):
            routine[i] = ['School', schoolID]
            
        routine[15] = ['Outdoors', 0]
        
        if (random.randint(1,100)<58): #57% chance to participate in extracurricular activities
            extracurricularID = random.randint(0, len(person.town.extracurriculars)) - 1
            starting_hour = random.randint(16,20)
            routine[starting_hour-1] = ['Transportation', random.randint(0, len(person.town.transportations)) - 1] #Transportation from home to activity.
            routine[starting_hour+3] = ['Transportation', random.randint(0, len(person.town.transportations)) - 1] #Transportation from activity to home.
            for i in range(starting_hour, starting_hour+3):
                routine[i] = ['Extracurricular', extracurricularID]
                
        return routine

      

    def CreateRoutineYoungAdult(self, person):
        #Initialization
        routine = [None] * 24
        for i in range(24): #Default
            routine[i] = ['House', person.houseID]
            
        if (random.randint(1,100)<64): #63% chance to attend college/university
            schoolID = random.randint(0, len(person.town.schools)) - 1
            endtime = 14
            for i in range(9, endtime+1):
                routine[i] = ['School', schoolID]
        else: #37% chance to work
            workplaceID = random.randint(0, len(person.town.workplaces)) - 1
            endtime = 17
            for i in range(9, endtime+1):
                routine[i] = ['Workplace', workplaceID]
                
        
        self.Transport(routine, person.town, 8, endtime+1)

        entertainmentID = random.randint(0, len(person.town.entertainments)) - 1
        starting_hour = random.randint(18,20)
        for i in range(starting_hour, starting_hour+3): #3 afternoon/night hours for enternainment
            routine[i] = ['Entertainment', entertainmentID]
        
        return routine
        
        

    def CreateRoutineAdult(self, person):
        #Initialization
        routine = [None] * 24
        for i in range(24): #Default
            routine[i] = ['House', person.houseID]
            

        #Work
        workplaceID = random.randint(0, len(person.town.workplaces)) - 1
        for i in range(9, 18):
            routine[i] = ['Workplace', workplaceID]
     
        self.Transport(routine, person.town, 8, 18)
        
        if (random.randint(1,10)<9): #80% chance for nighttime enternainment
            entertainmentID = random.randint(0, len(person.town.entertainments)) - 1
            starting_hour = random.randint(19,20)
            for i in range(starting_hour, starting_hour+3): #3 afternoon/night hours for enternainment
                routine[i] = ['Entertainment', entertainmentID]
                
            self.Transport(routine, person.town, starting_hour-1, starting_hour+3)

        
        return routine
        
        
        
    def CreateRoutineMiddleAged(self, person):
        #Initialization
        routine = [None] * 24
        for i in range(24): #Default
            routine[i] = ['House', person.houseID]
            
       
        #Work
        workplaceID = random.randint(0, len(person.town.workplaces)) - 1
        for i in range(9, 18):
            routine[i] = ['Workplace', workplaceID]

        self.Transport(routine, person.town, 8, 18)
        
        if (random.randint(1,2)==1): #50% chance for nighttime enternainment
            entertainmentID = random.randint(0, len(person.town.entertainments)) - 1
            starting_hour = random.randint(19,22)
            for i in range(starting_hour, starting_hour+2): #2 afternoon/night hours for enternainment
                routine[i] = ['Entertainment', entertainmentID]
        
        return routine
        

        
    def CreateRoutineElderly(self, person):
        #Initialization
        routine = [None] * 24
        for i in range(24): #Default
            routine[i] = ['House', person.houseID]
            
        starting_hour = random.randint(10,18)
        for i in range (starting_hour, starting_hour+4): #Morning or afternoon walk
            routine[i] = ['Outdoors', 0]
            
        self.Transport(routine, person.town, starting_hour-1, starting_hour+4)
            
        return routine
        

        
    def CreateHealthFactor(self, person):
        '''
        Creates the health factor for each person, depending on their age group.    
        This number represents the hospitalization rate and is used when the person gets infected.
        Underages and young adults are considered the "reference group".
        '''

        if (person.agegroup == "Underage"):
            return 1        
        elif (person.agegroup == "Young Adult"):
            return 1        
        elif (person.agegroup == "Adult"):
            return 1.5
        elif (person.agegroup == "Middle Aged"):
            return 3
        else: #Elderly  
            return 9.67
            
            
       
    def NormalDistributionFactor(self, mean, sd):
        '''
        Returns a random number based on the normal distribution.
        Used to generate the hygiene and legality factor for each person.
        '''
        
        factor = 0
        while (factor<=0): #Keep trying until a positive number is generated
            factor = np.random.normal(loc=mean, scale=sd)    
        return factor
        
        
    #Determines when the person uses transportations means (before or after the activity) and updates the routine
    def Transport(self, routine, town, starttime, endtime):
        if (random.randint(1,2)==1): #50/50 chance
            routine[starttime] = ['Outdoors', 0]
            routine[endtime] = ['Transportation', random.randint(0, len(town.transportations)) - 1]
        else:
            routine[endtime] = ['Outdoors', 0]
            routine[starttime] = ['Transportation', random.randint(0, len(town.transportations)) - 1]   
        return routine
        
        
        
    def ExpectedDailyInteractions(self, routine):
        '''
        Input: A person's daily routine.
        Output: A 24-element list (one for each hour of the day) that contains the expected number of interactions 
                with other people, depending on their corresponding location.
                The hourly value for each location is explained in the documentation.    
        '''    
        interactions = []
        
        for activity in routine:
            if (activity[0] == 'House'):
                interactions.append(0.448)
            elif (activity[0] == 'School'):
                interactions.append(5)
            elif (activity[0] == 'Workplace'):
                interactions.append(8)
            elif (activity[0] == 'Transportation'):
                interactions.append(10)
            elif (activity[0] == 'Extracurricular'):
                interactions.append(5)
            elif (activity[0] == 'Entertainment'):
                interactions.append(7)
            elif (activity[0] == 'Outdoors'):
                interactions.append(2)
        
        return interactions
        
        
        
        