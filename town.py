import math

class Town:
    def __init__(self, residents):
        self.houses = []
        self.schools = []
        self.workplaces = []
        self.hospitals = []
        self.entertainments = []
        self.transportations = []
        self.extracurriculars = []
        self.outdoors = []
        
        self.hospitals.append(Hospital())
        
        for i in range(math.ceil(residents/1500)):
            self.schools.append(School())
            
        for i in range(math.ceil(residents/50)):
            self.workplaces.append(Workplace())
        
        for i in range(math.ceil(residents/500)):
            self.entertainments.append(Entertainment())
            self.extracurriculars.append(Extracurricular())
   
        for i in range(math.ceil(residents/1000)):
            self.transportations.append(Transportation())

        self.outdoors.append(Outdoors())
        
        # print ("Houses: " + str(len(self.houses)))
        # print ("Schools: " + str(len(self.schools)))
        # print ("Workplaces: " + str(len(self.workplaces)))
        # print ("Hospitals: " + str(len(self.hospitals)))
        # print ("Entertainments/Extracurriculars: " + str(len(self.entertainments)))
        # print ("Transportations: " + str(len(self.transportations)))

            
class House:
    def __init__(self):    
        self.currentVisitors = []

class School:
    def __init__(self):   
        self.currentVisitors = []

class Workplace:
    def __init__(self):  
        self.currentVisitors = []    

class Hospital:
    def __init__(self):  
        self.currentVisitors = []    
    
class Entertainment:
    def __init__(self):  
        self.currentVisitors = []
        
class Extracurricular:
    def __init__(self):   
        self.currentVisitors = []  
        
class Transportation:
    def __init__(self):   
        self.currentVisitors = []  
        
class Outdoors:
    def __init__(self):   
        self.currentVisitors = []  



