class Ticket():

    def __init__(self,name,points,sprintName):
        """Create ticket with its name and story points"""
        self.name = name
        self.points = points or 0
        self.sprintName = sprintName

    def isSprint(self):
        """Is this ticket in a Sprint ?""" 
        return "Sprint" in self.sprintName

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name