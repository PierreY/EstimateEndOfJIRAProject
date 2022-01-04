from tabulate import tabulate
import datetime
import csv
import configparser
from TicketList import TicketList
from Ticket import Ticket
from tkinter import Tk, filedialog

# HYPOTHESIS 1 : a ticket with 0 points is a ticket that has not been estimated
# HYPOTHESIS 2 : a ticket having an empty sprint name is a ticket in the backlog

class Project():

    def __init__(self, confFile):
        # Set variables according to conf file
        config = configparser.ConfigParser()
        config.read(confFile,encoding='utf-8')
        self.name = config['DEFAULT']['ProjectName']
        self.ticketList = TicketList(self.setTicketsFromCSV(self.askCsv(), config['CSV']))
        self.sprintSpeed =  config['DEFAULT']['SprintDefaultSpeed']
        self.sprintDone = config['DEFAULT']['SprintDone']
        self.initialNbOfSprints = config['DEFAULT']['InitialNbOfSprints']
        self.sprintDurationInWeeks = config['DEFAULT']['SprintDurationInWeeks']
        self.beginningNextSprint = datetime.datetime.strptime(config['DEFAULT']['NewSprintBegins'], '%d/%m/%y')
        self.wishDate = datetime.datetime.strptime(config['DEFAULT']['WishDate'], '%d/%m/%y')

    def remainingSprints(self):
        """Calculate the number of sprints that should be done to end the project"""
        return round(self.ticketList.pointsToBeDone()/float(self.sprintSpeed),0)

    def neededSprints(self):
        """Calculate the total of sprint needed"""
        return int(float(self.sprintDone) + self.remainingSprints())

    def additionalSprints(self):
        """Calculate the number of sprints needed in addition to the intial ones"""
        return self.neededSprints() - int(self.initialNbOfSprints)

    def weeksRemaining(self):
        """Calculate the number of weeks that remain to ends the project"""
        return self.remainingSprints() * int(self.sprintDurationInWeeks)

    def endOfProject(self):
        """Estimate the end date of the project"""
        return self.beginningNextSprint + datetime.timedelta(weeks=self.weeksRemaining())

    def wishedSprintSpeed(self):
        """Get the sprint speed that would be needed to keep the wish end date"""
        weeksWished = (self.wishDate - self.beginningNextSprint).days / 7
        return round(self.ticketList.pointsToBeDone() / (weeksWished/float(self.sprintDurationInWeeks)),1)

    def setTicketsFromCSV(self, csvFilename, confCsv):
        """Set ticket list of this project based on a CSV file gotten from JIRA filter"""

        tickets = []

        with open(csvFilename, encoding='utf8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            for row in csv_reader:

                tickets.append(Ticket(
                    row[confCsv["TicketNameField"]],
                    0 if row[confCsv["TicketPointsField"]]=="" else int(float(row[confCsv["TicketPointsField"]])),
                    row[confCsv["TicketSprintField"]]
                    )
                )
        return tickets

    def askCsv(self):
        """Open a dialog asking to choose a .csv file"""
        root = Tk()
        root.withdraw()
        root.update()
        return filedialog.askopenfilename(title = "Please select a .csv file from JIRA filter",filetypes = (("CSV Files","*.csv"),))

    def getInitialParams(self):
        """Get array of initial project parameters"""
        return [
            ["Date de début du prochain sprint",self.beginningNextSprint],
            ["Durée d'un sprint en semaines",self.sprintDurationInWeeks],
            ["Vélocité",self.sprintSpeed]
        ]

    def getSprintData(self):
        """Get array of sprint data"""
        return [
            ["Nombre de sprints initiaux",self.initialNbOfSprints],
            ["Nombre de sprints réalisés",self.sprintDone],
            ["Nombre de sprints restants",self.remainingSprints()],
            ["Nombre de sprints à ajouter aux sprints initiaux",self.additionalSprints()],
            ["Nombre de sprints au total pour finir le projet",self.neededSprints()],
        ]

    def getProjectDate(self):
        """Get project dates data"""
        return [
            ["Nombre de semaines restantes",self.weeksRemaining()],
            ["Estimation fin de projet",self.endOfProject()],
            ["Vélocité nécessaire pour tenir la date du "+str(self.wishDate),self.wishedSprintSpeed()]
        ]

    def __str__(self):
        header = ["Libellé","Valeur"]
        #s = "##############   "+self.name+"   #################\n\n"
        s = "PARAMETRES GENERAUX\n\n"
        s += tabulate(self.getInitialParams(), header, tablefmt="grid")+"\n\n"
        s += "NOMBRE DE SPRINTS\n\n"
        s += tabulate(self.getSprintData(), header, tablefmt="grid")+"\n\n"
        s += "DATE DE FIN ESTIMEE\n\n"
        s += tabulate(self.getProjectDate(), header, tablefmt="grid")+"\n\n"
        return s
