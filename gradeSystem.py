"""
Grade systempyth
"""

import pandas as pd
import tabulate


class Student:
    
    def __init__(self):
        self.studentInfo: pd.DataFrame = None
        # 每個student一個row
        # col 為lab1, lab2,.... ,weighted average, grade

        
        

    def addStudent(self):
        pass

    def updateAverage(self):
        pass
        # 重算average 的Column
    
    def updateGrade(self):
        pass
        # 重算grade 的column

    def updateScoreOfStudent(sid, subject, newScore):
        pass


class Subjects:
    def __init__(self) -> None:
        self.name = ["lab1", "lab2", "lab3", "midTerm", "finalExam"]
        self.weight=[0.1, 0.1, 0.1, 0.3, 0.4]
    
    def updateWeight(self):
        pass

class Query:
    def __init__(self) -> None:
        pass
    
    def ShowScore(self, sid):
        pass
    def showGradeLetter(self, sid):
        pass
    def showAverage(self, sid):
        pass
    def showRank(self, sid):
        pass
    def showDistribution(self):
        pass
    def filtering(self, scoreLargerThan):
        pass
    def addStudent(self, sid, name, listOfScore):
        pass
    def updateGrade(self, sid, subject):
        pass
    def updateWeights(self, listOfWeight):
        pass
    def showMenu(self):
        pass
    def exit(self):
        pass
    
def readInput():
    """
    Read txt input of student data
    """
    pass

if __name__ == "__main__":
    # 1. read input
    # 2. show interface
    # inifinte loop for waiting command

