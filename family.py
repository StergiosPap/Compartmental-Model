class Family:
    def __init__(self, residenceNumber=None):        
        self.residenceNumber = residenceNumber
        self.members = []
    
    def AddMember(self, person=None):
        self.members.append(person)
