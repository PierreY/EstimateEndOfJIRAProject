from tabulate import tabulate
from itertools import groupby

class TicketList():

    def __init__(self, tickets):
        self.tickets = tickets

    def backlogTickets(self):
        """Get the lists of tickets that are in the backlog"""
        return [ticket for ticket in self.tickets if not ticket.isSprint()]
    
    def nbEstimated(self, tickets):
        """Count the number of tickets that have already been estimated"""
        return sum(map(lambda num: num!=0, [ticket.points for ticket in tickets]))

    def nbToEstimate(self, tickets):
        """Count the number of tickets in backlog that still need to be estimated with story points"""
        return len(tickets) - self.nbEstimated(tickets)

    def points(self, tickets):
        """Sum the story points of every ticket having estimation in this list"""
        return sum(ticket.points for ticket in tickets)

    def estimationProgress(self):
        """Get the % of estimation progress for tickets in backlog"""
        return round(self.nbEstimated(self.backlogTickets())/len(self.backlogTickets())*100,1)

    def usInBacklogProgress(self):
        """Get the % of US in the backlog"""
        return round(len(self.backlogTickets())/len(self.tickets)*100,1)

    def pointsPerEstimatedTicket(self):
        """Get an average of points per tickets having an estimation"""
        return round(self.points(self.tickets)/self.nbEstimated(self.tickets),1)

    def estimateTotalPoints(self):
        """Calculate the number of story points that the list +would+ contain if every tickets had estimation
        based on an average points per ticket having beeing estimated"""
        return round(self.points(self.tickets)+self.estimateMissingPoints())

    def estimateMissingPoints(self):
        """Estimate the points that would need to be added to complete the estimated points """
        return round(self.averagePointsPerTicket()*self.nbToEstimate(self.backlogTickets()),1)

    def pointsDone(self):
        """Sum the points that are already in sprint"""
        return self.points(self.tickets) - self.points(self.backlogTickets())

    def pointsToBeDone(self):
        """Estimate the points that need to be developed to end the project"""
        return self.estimateTotalPoints() - self.pointsDone()

    def averagePointsPerTicket(self):
        """Get average of points per ticket that have estimation - backlog and sprint"""
        return round(self.points(self.tickets)/self.nbEstimated(self.tickets),1)

    def getStatByList(self):
        """Get array of stats"""

        sortTicketsBySprint = sorted(self.tickets, key=lambda ticket: ticket.sprintName)
        ticketsBySprint = [list(result) for key, result in groupby(
            sortTicketsBySprint, key=lambda ticket: ticket.sprintName
        )]

        stats = []
        for sprint in ticketsBySprint:
            ticketListName = sprint[0].sprintName or "Backlog"
            stats +=  [
                ["Titre de la liste des tickets",ticketListName],
                ["Nombre de tickets",str(len(sprint))],
                ["Nombre de points",str(self.points(sprint))],
            ]
            if ticketListName == "Backlog":
                stats += [
                    ["Tickets estimés",str(self.nbEstimated(self.backlogTickets()))],
                    ["Tickets à estimer",str(self.nbToEstimate(self.backlogTickets()))],
                    ["% estimé du backlog",str(self.estimationProgress())],
                    ["% US restantes dans le backlog",str(self.usInBacklogProgress())],
                ]
            stats += [["",""]]

        return stats

    def getGlobalStats(self):
        return [
            ["Points / US",self.pointsPerEstimatedTicket()],
            ["Points estimés",self.points(self.tickets)],
            ["Projection : points manquants",self.estimateMissingPoints()],
            ["Projection : points totaux",self.estimateTotalPoints()],
            ["Points développés :",self.pointsDone()],
            ["Points à développer :",self.pointsToBeDone()],
        ]

    def __str__(self):
        header = ["Libellé","Valeur"]
        s = tabulate(self.getStatByList(), header, tablefmt="grid")+"\n\n"
        s += "Global\n\n"
        s += tabulate(self.getGlobalStats(), header, tablefmt="grid")+"\n\n"
        return s