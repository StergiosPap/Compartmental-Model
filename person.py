import numpy as np
import random
from scipy.stats import truncnorm
from town import Town

class Person:
    '''
    Class that represents each resident of the town.
    The constructor creates their characteristics that differentiate them from each other.
    
    ID: Unique identifier for each object.
    House ID: Represents the person's home ID. People in the same family have the same House ID.    
    Agegroups:  18-: Underage
                19-25: Young Adult
                26-40: Adult
                41-65: Middle Aged
                66+: Elderly
    Health Factor: Determines the person's likelihood of being hospitalized during their illness period. It is entirely age-dependent.
    Hygiene Factor: Affects the person's likelihood to transmit and receive the virus.
    Legality Factor: Determines the person's likelihood to obey the government's protection measures during the pandemic.
    '''

    def __init__(self, ID=None, houseID=None, agegroup=None, town=None):
        # Basic characteristics
        self.ID = ID
        self.houseID = houseID
        self.agegroup = agegroup
        self.town = town
        
        self.isHospitalized = False
        
        # Personality characteristics (Health/Hygiene/Legality factor).
        self.healthFactor = self.CreateHealthFactor(self)
        
        normalDistGenerator = self.get_truncated_normal(mean=1.0, sd=0.7, low=0.1, upp=5)
        self.hygieneFactor = normalDistGenerator.rvs()

        normalDistGenerator =  self.get_truncated_normal(mean=1.0, sd=0.3, low=0.5, upp=2)
        self.legalityFactor = normalDistGenerator.rvs()
        
        self.defaultRoutine = self.CreateRoutine(self)
        self.routine = self.defaultRoutine # The person's active routine. It is the same as defaultRoutine under normal circumstances but might change with certain conditions (e.g. Hospitalization).
        self.interactions = self.ExpectedDailyInteractions(self.routine) # The person's expected interactions per hour of the day.


        
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
            
        else: # Elderly  
            schedule = self.CreateRoutineElderly(person)

        return schedule


    
    def CreateRoutineUnderage(self, person):
        # Initialization
        routine = [None] * 24
        for i in range(24): # Default
            routine[i] = ['House', person.houseID]
            
        routine[8] = ['Outdoors', 0]
        
        # School in the morning
        schoolID = random.randint(0, len(person.town.schools)) - 1
        for i in range(9, 15):
            routine[i] = ['School', schoolID]
            
        routine[15] = ['Outdoors', 0]
        
        if (random.randint(1,100)<84): # 83% chance to participate in extracurricular activities
            extracurricularID = random.randint(0, len(person.town.extracurriculars)) - 1
            starting_hour = random.randint(16,20)
            routine[starting_hour-1] = ['Transportation', random.randint(0, len(person.town.transportations)) - 1] # Transportation from home to activity
            routine[starting_hour+3] = ['Transportation', random.randint(0, len(person.town.transportations)) - 1] # Transportation from activity to home
            for i in range(starting_hour, starting_hour+3):
                routine[i] = ['Extracurricular', extracurricularID]
                
        return routine


    def CreateRoutineYoungAdult(self, person):
        # Initialization
        routine = [None] * 24
        for i in range(24): # Default
            routine[i] = ['House', person.houseID]
            
        if (random.randint(1,100)<64): # 63% chance to attend college/university
            schoolID = random.randint(0, len(person.town.schools)) - 1
            endtime = 14
            for i in range(9, endtime+1):
                routine[i] = ['School', schoolID]
        else: # 37% chance to work
            workplaceID = random.randint(0, len(person.town.workplaces)) - 1
            endtime = 17
            for i in range(9, endtime+1):
                routine[i] = ['Workplace', workplaceID]

        self.Transport(routine, person.town, 8, endtime+1)

        entertainmentID = random.randint(0, len(person.town.entertainments)) - 1
        starting_hour = random.randint(18,20)
        for i in range(starting_hour, starting_hour+3): # 3 afternoon/night hours for entertainment
            routine[i] = ['Entertainment', entertainmentID]
        
        return routine
        
        
    def CreateRoutineAdult(self, person):
        # Initialization
        routine = [None] * 24
        for i in range(24): # Default
            routine[i] = ['House', person.houseID]
            
        # Work
        workplaceID = random.randint(0, len(person.town.workplaces)) - 1
        for i in range(9, 18):
            routine[i] = ['Workplace', workplaceID]
     
        self.Transport(routine, person.town, 8, 18)
        
        if (random.randint(1,10)<9): # 80% chance for nighttime enternainment
            entertainmentID = random.randint(0, len(person.town.entertainments)) - 1
            starting_hour = random.randint(19,20)
            for i in range(starting_hour, starting_hour+3): # 3 afternoon/night hours for entertainment
                routine[i] = ['Entertainment', entertainmentID]
                
            self.Transport(routine, person.town, starting_hour-1, starting_hour+3)
        
        return routine
        
        
    def CreateRoutineMiddleAged(self, person):
        # Initialization
        routine = [None] * 24
        for i in range(24): # Default
            routine[i] = ['House', person.houseID]

        # Work
        workplaceID = random.randint(0, len(person.town.workplaces)) - 1
        for i in range(9, 18):
            routine[i] = ['Workplace', workplaceID]

        self.Transport(routine, person.town, 8, 18)
        
        if (random.randint(1,2)==1): # 50% chance for nighttime enternainment
            entertainmentID = random.randint(0, len(person.town.entertainments)) - 1
            starting_hour = random.randint(19,22)
            for i in range(starting_hour, starting_hour+2): # 2 afternoon/night hours for entertainment
                routine[i] = ['Entertainment', entertainmentID]
        
        return routine
        
        
    def CreateRoutineElderly(self, person):
        # Initialization
        routine = [None] * 24
        for i in range(24): # Default
            routine[i] = ['House', person.houseID]
            
        starting_hour = random.randint(10,18)
        for i in range (starting_hour, starting_hour+4): # Morning or afternoon walk
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
        else: # Elderly  
            return 9.67



    def get_truncated_normal(self, mean, sd, low, upp):
        '''
        Generates a function based on the normal distribution, given an upper and lower bound (truncation).
        Used to generate the hygiene and legality factor for each person.
        
        ex: generator = get_truncated_normal(...)
            value = generator.rvs()
        
        (Source: https://stackoverflow.com/questions/36894191/how-to-get-a-normal-distribution-within-a-range-in-numpy)
        '''
        return truncnorm((low-mean)/sd, (upp-mean)/sd, loc=mean, scale=sd)



    def Transport(self, routine, town, starttime, endtime):
        '''
        Determines when the person uses transportations means (before or after the activity) and updates the routine.
        '''
        if (random.randint(1,2)==1): # 50/50 chance
            routine[starttime] = ['Outdoors', 0]
            routine[endtime] = ['Transportation', random.randint(0, len(town.transportations)) - 1]
        else:
            routine[endtime] = ['Outdoors', 0]
            routine[starttime] = ['Transportation', random.randint(0, len(town.transportations)) - 1]   
        return routine
        


    def ModifyRoutine(self, level):
        '''
        Modifies the person's routine whenever the Emergency Level changes in order to abide with the government's laws.
        '''
        if (level < 2): # People return to their default routines.
            self.routine = self.defaultRoutine
            return
    
        modifiedRoutine = []
        
        for activity in self.defaultRoutine:
            if (activity[0] == 'School' or activity[0] == 'Extracurricular'):
                if (level == 3):  # 100% chance for distance learning in level 3.
                    modifiedRoutine.append(['House', self.houseID])
                else:
                    modifiedRoutine.append(activity)
            elif (activity[0] == 'Workplace'): # Working from home. 50% chance in level 2, 100% chance in level 3.
                if (level == 2):
                    if (random.randint(1,2)==1):
                        modifiedRoutine.append(['House', self.houseID])
                    else:
                        modifiedRoutine.append(activity)
                elif (level == 3):
                    modifiedRoutine.append(['House', self.houseID])
                else:
                    modifiedRoutine.append(activity)
            else: # Any other activity works as normal in any level.
                modifiedRoutine.append(activity)
                
        self.routine = modifiedRoutine
        
    
    
    def Hospitalize(self):
        if (self.town.hospitals[0].IsFull()): # If the hospital is full, the person stays in home instead (until they recover).
            self.routine = [['House', self.houseID]] * 24
        else: # Their entire routine is replaced with "Hospital" entries.
            self.routine = [['Hospital', 0]] * 24
        
        self.isHospitalized = True
    
    
    
    def ExpectedDailyInteractions(self, routine):
        '''
        Input: A person's daily routine.
        Output: A 24-element list (one for each hour of the day) that contains the expected number of interactions 
                with other people, depending on their corresponding location.
                The reasoning for the hourly value for each location is explained in the documentation.    
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
        
        
        
    def IsWearingMask(self, location, emergencyLevel):
        '''
        Returns a boolean value depending if the person is currently wearing a mask.
        '''
        if (emergencyLevel == 0): # No protection measures necessary.
            return False
            
        elif (emergencyLevel == 1): # Mandatory masks in all closed spaces (except home).
            if (location == "Transportation" or location == "School" or location == "Workplace" or location == "Extracurricular" or location == "Entertainment"):
                return self.IsWearingMaskUtil()
            else:
                return False
        
        else: # (Levels 2-3) Mandatory masks in all closed spaces (except home) and outdoors.
            if (location == "Transportation" or location == "School" or location == "Workplace" or location == "Extracurricular" or location == "Entertainment" or location == "Outdoors"):
                return self.IsWearingMaskUtil()
            else:
                return False

    def IsWearingMaskUtil(self):
        '''
        Auxiliary function for "IsWearingMask" that takes into consideration the person's legalityFactor.
        '''
        obedience_chance = 1 if (self.legalityFactor >= 1) else self.legalityFactor        
        return (random.random() <= obedience_chance)

    
    

    