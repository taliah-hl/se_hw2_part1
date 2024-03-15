"""
Grade systempyth
"""

import pandas as pd
from tabulate import tabulate
import numpy as np


class Students:
    
    def __init__(self):
        self.studentInfo: pd.DataFrame = None
        self.subjectNames = ["id", "name", "lab1", "lab2", "lab3", "midTerm", "finalExam"]
        self.weight= np.array([0.1, 0.1, 0.1, 0.3, 0.4])
        # 每個student一個row
        # col 為lab1, lab2,.... ,weighted average, grade

    def createTable(self, data):
        """
        Parameters
        -------
        data: list of list 
        """
        self.studentInfo = pd.DataFrame(data, columns= [ele for ele in self.subjectNames])
        self.studentInfo["average"] = pd.NA
        self.studentInfo["grade"] = pd.NA
        self.studentInfo.set_index("id", inplace=True)

        self.updateAverage()
        self.updateGrade()

    def updateWeight(self, newWeight):
        """
        Parameters
        ------
        nreWeight: list of float
        """
        try:
            assert isinstance(newWeight, list)
            assert len(newWeight) == 5
        except:
            print("wrong format of weight, weight must be a list of 5 float")
        try:
            self.weight = np.array(newWeight)
        except:
            print("wrong format of weight, weight must be a list of 5 float")

    
    def printTable(self):
        """
        for debug only
        """
        assert self.studentInfo is not None
        print(tabulate(self.studentInfo, headers='keys', tablefmt='psql'))

    def addStudent(self, data):
        self.studentInfo.loc[data[0]] = data[1:]
    def updateAverage(self):
        
        # 重算average 的Column
        first_col = self.studentInfo.columns.get_loc("lab1")
        last_col = self.studentInfo.columns.get_loc("finalExam")
        for row in range(len(self.studentInfo)):
            self.studentInfo.iloc[row, self.studentInfo.columns.get_loc("average")] = np.sum(self.studentInfo.iloc[row, first_col:last_col+1] * self.weight)

    def updateGrade(self):
        
        # 重算grade 的column
        for row in range(len(self.studentInfo)):
            self.studentInfo.iloc[row, self.studentInfo.columns.get_loc("grade")] = self.scoreToGrade(self.studentInfo.iloc[row, self.studentInfo.columns.get_loc("average")])
            
    def scoreToGrade(self, score)->str:
        """
        Parameters
        ------
        score: float

        Return
        ------
        letter: str
        
        """
        try:
            if score >=90:
                return "A+"
            elif score >=85 and score <90:
                return "A"
            elif score >=80 and score <85:
                return "A-"
            elif score >=77 and score <80:
                return "B+"
            elif score >=73 and score <77:
                return "B"
            elif score >=70 and score <73:
                return "B-"
            elif score >=67 and score <69:
                return "C+"
            elif score >=63 and score <67:
                return "C"
            elif score >=60 and score <63:
                return "C-"
            elif score >=50 and score <60:
                return "D"
            else:
                return "E"
        except Exception as err:
            print(err)

    
    def updateScoreOfStudent(self, sid, subject, newScore):

        try:
            self.studentInfo.at[sid, subject] = newScore
        except Exception as err:
            print(err)  # subject name does not match any subject
        
        # update average of this student
        first_col = self.studentInfo.columns.get_loc("lab1")
        last_col = self.studentInfo.columns.get_loc("finalExam")
        self.studentInfo.at[sid, "average"] = np.sum(self.studentInfo.iloc[self.studentInfo.index.get_loc(sid), first_col:last_col+1] * self.weight)

        # update grade of this student
        self.studentInfo.at[sid, "grade"] = self.scoreToGrade(self.studentInfo.at[sid, "average"])


    def testFunc(self):
        # for index, row in self.studentInfo.iterrows():
        #     print(row)
        print("index")
        print(self.studentInfo.index.values)


class Query:
    def __init__(self, student) -> None:
        self.student=student
    
    def ShowScore(self, sid):
        print((self.student.studentInfo.loc[sid]))
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
    
def readInput()->list:
    """
    Read txt input of student data
    Return
    -----
    data: list
    - list of list describing student data
    """
    with open ('input.txt', 'r', encoding='utf-8') as fio:
        data = fio.readlines()

    # data cleaning
    for i in range(len(data)):
        data[i] = data[i].strip("\n").split(" ")
        try:
            assert(len(data[i])==7)
        except:
            print("Wrong input file format. Input file must contain 7 columns")
        for j in range(7):
            if j != 1:
                data[i][j] = int(data[i][j])

    return data
    

def sanityCheck(data, toPrint=False):

    # [to do] change all assert to try...except...
    assert isinstance(data, list)
    assert isinstance(data[0], list)
    for i in range(7):
        assert isinstance(data[i], list)
            
    # print first 5 rows if toPrint==true for sanity check
    if toPrint:
        for i in range(5):
            print(f"row {i}", sep="\t")
            print(data[i])
    


def uat():
    """
    內部測試用
    
    """
    ### test case 1
    # [to do] move this to unit test
    print("===================\n====================")
    student.updateScoreOfStudent(955002056, "lab1", 1)
    new_student = [985111111, "陳小明", 100, 100, 100, 100, 100, 100, "hi"]
    student.addStudent(new_student)
    #student.printTable()

    ## testing query
    query.ShowScore(995002901)


if __name__ == "__main__":
    # 1. read input
    # 2. show interface
    # inifinte loop for waiting command


    #------ Read Input --------#

    data = readInput()
    sanityCheck(data, False)

    # ------ Initialization  ---------#
    student = Students()
    query = Query(student)

    student.createTable(data)


    # ------ mian function  -------#

    UI = """Welcome to the Grade System.
    0) Show menu
    1) Show grade
    2) Show grade letter
    3) Show average
    4) Show rank
    5) Show distribution
    6) Filtering
    7) Add student
    8) Update grade
    9) Update weights
    10) Exit
    """
    print(UI)
    while(True):
        cmd = input("請輸入指令(0~10)開始使用: ")
        if cmd =="1":
            sid = input("請輸入ID: ")
            sid = int(sid)
            query.ShowScore(sid)
    
    

    
    

# python gradeSystem.py