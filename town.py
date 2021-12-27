import math

class Town:
    '''
    Class that represents the entire city and its components.
    The constructor initializes the locations depending on the number of residents.
    '''
    
    def __init__(self, residents):
        # Lists that contain the corresponding location's objects.
        self.houses = []
        self.schools = []
        self.workplaces = []
        self.hospitals = []
        self.entertainments = []
        self.transportations = []
        self.extracurriculars = []
        self.outdoors = []
        
        for i in range(math.ceil(residents/1500)): # Create 1 school for every 1500 residents.
            self.schools.append(School())
            
        for i in range(math.ceil(residents/50)): # Create 1 workplace for every 50 residents.
            self.workplaces.append(Workplace())
        
        for i in range(math.ceil(residents/500)):  # Create 1 entertainment and extracurricular place for every 500 residents.
            self.entertainments.append(Entertainment())
            self.extracurriculars.append(Extracurricular())
   
        for i in range(math.ceil(residents/1000)): # Create 1 transportation mean for every 1000 residents.
            self.transportations.append(Transportation())

        self.hospitals.append(Hospital()) # Create 1 hospital.
        self.outdoors.append(Outdoors()) # Create 1 outdoors location.

        
'''
Separate class for each kind of location.
Their constructor initialize a list that will contain their current visitors (Person objects). 
'''
class House:
    def __init__(self):    
        self.currentVisitors = []

class School:
    def __init__(self):   
        self.currentVisitors = []

class Workplace:
    def __init__(self):  
        self.currentVisitors = []    
   
class Entertainment:
    def __init__(self):  
        self.currentVisitors = []
        
    def IsFull(self, emergencyLevel):
        '''
        Returns a boolean value depending if the location is full or not.
        The maximum capacity depends on the current Emergency Level.
        '''
        capacity = 500
        if (emergencyLevel == 1):
            capacity = 100
        elif (emergencyLevel == 2):
            capacity = 50
        elif (emergencyLevel == 3):
            capacity = 0
            
        return (len(self.currentVisitors) >= capacity)
        
class Extracurricular:
    def __init__(self):   
        self.currentVisitors = []  
        
class Transportation:
    def __init__(self):   
        self.currentVisitors = []  
        
    def IsFull(self, emergencyLevel):
        capacity = 80 - emergencyLevel*20 # Emergency Levels: 0, 1, 2, 3. Maximum Capacities: 80, 60, 40, 20.
        return (len(self.currentVisitors) >= capacity)
        
class Outdoors:
    def __init__(self):   
        self.currentVisitors = []  

class Hospital:
    def __init__(self):  
        self.currentVisitors = []    
    
    def IsFull(self): # Maximum capacity: 200 people.
        return (len(self.currentVisitors) >= 200)


