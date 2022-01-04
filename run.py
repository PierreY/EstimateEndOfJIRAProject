from Project import Project
from tabulate import tabulate

# SET PROJECT
project = Project('conf.ini')

# PRINT DATA - in terminal or in file
#print(project.ticketList)
#print(project)
#input()
with open('résultat.txt', 'w', encoding='utf-8') as outputfile:
    print(project.ticketList, file=outputfile)
    print(project, file=outputfile)