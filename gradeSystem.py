"""
Grade system
--- [這裡給我們自己看] ----
TO DO
1. 刻好query的各method
2. 最外層for loop, 讀input -> call query的相應method
3. 在可能出錯地方加 try...except... block 
4. 現在的try...except... block 只有打印error, 需加上code 接回去讓使用者重新輸入

[新to do]
所有method + 回傳值
e.g. return False = error -> 傳到main -> 使main 知道收到Fasle = 要prompt user 重新輸入
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
        newWeight: list of float
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


def testFunc(student, query):
    # for index, row in self.studentInfo.iterrows():
    #     print(row)
    print("showScore")
    query.showScore(955002056)
    print("showGradeLetter")
    query.showGradeLetter(955002056)
    print("showAverage")
    query.showAverage(955002056)
    print("showRank")
    query.showRank(955002056)
    print("showDistribution")
    query.showDistribution()
    print("filtering")
    query.filtering(90)
    print("addStudent")
    query.addStudent()
    print("updateGrade")
    query.updateGrade(955002056)
    print("updateWeights")
    query.updateWeights()
    print("showMenu")
    query.showMenu()



class Query:
    def __init__(self, student) -> None:
        self.student=student
    
    def showScore(self, sid):
        #[update]:要判斷輸入的id是否真實存在，加上輸出學生的ID和姓名
        print((self.student.studentInfo.loc[sid]))
    def showGradeLetter(self, sid):
        #[todo]:印出學生等第的那一排
        try:
            student_average = self.student.studentInfo.at[sid,"average"]
            student_grade = self.student.scoreToGrade(student_average)
            student_name = self.student.studentInfo.at[sid,"name"]
            print("Student ID:",sid)
            print("Student Name:",student_name)
            print("Student Grade letter:",student_grade)
        except KeyError:
            print("Student ID:",sid,"not found")
        
    def showAverage(self, sid):
        #[todo]:印出學生平均成績的那一排
        try:
            student_average = self.student.studentInfo.at[sid,"average"]
            student_name = self.student.studentInfo.at[sid,"name"]
            print("Student ID:",sid)
            print("Student Name:",student_name)
            print("Student Average:",student_average)
        except KeyError:
            print("Student ID:",sid,"not found")
        
    def showRank(self, sid):
        #[todo]:計算排名+印出排名
        try:
            sorted_students = self.student.studentInfo.sort_values(by='average', ascending=False)
            student_rank = sorted_students.index.get_loc(sid)+1
            student_name = self.student.studentInfo.at[sid,"name"]
            print("Student ID:",sid)
            print("Student Name:",student_name)
            print("Student Rank:", student_rank)
        except KeyError:
            print("Student ID:",sid,"not found")

    def showDistribution(self):
        #[todo]:迴圈統計人數+印出排名
        try:
            grade_distribution = self.student.studentInfo.groupby('grade').size().reset_index(name='count')
            print("Grade Distribution:")
            print(tabulate(grade_distribution, headers='keys', tablefmt='psql'))
        except Exception as e:
            print("Error occurred while printing grade distribution:", e)

    def filtering(self, scoreLargerThan):
        #[todo]:迴圈跑一次所有學生，符合標準的印出來
        try:
            self.updateAverage()
            above_scoreLargeThan = self.student.studentInfo[self.student.studentInfo['average'] > scoreLargerThan]
            if above_scoreLargeThan.empty:
                print("No student")
            else:
                print(tabulate(above_scoreLargeThan[['ID', 'name', 'lab1', 'lab2', 'lab3', 'midTerm', 'finalExam', 'average', 'grade']], headers='keys', tablefmt='psql'))
        except Exception as e:
            print("Error occurred while printing grade distribution:", e)

    def addStudent(self):
        #[todo]:開一個新的row放新學生的資料
        try:
            input_str = input("請依格式輸入新增的學生資訊(格式: ID Name lab1 lab2 lab3 midTerm finalExam): ")
            student_info_list = input_str.split()
            if len(student_info_list) != 7:
                print("未依格式輸入資訊，請重新確認您的資訊~")
                return

            student_id = student_info_list[0]
            student_name = student_info_list[1]
            lab1 = float(student_info_list[2])
            lab2 = float(student_info_list[3])
            lab3 = float(student_info_list[4])
            mid_term = float(student_info_list[5])
            final_exam = float(student_info_list[6])

            new_student_info = [student_id, student_name, lab1, lab2, lab3, mid_term, final_exam]

            print("新增資訊為: ",new_student_info)
            Y_N = input("請確認您輸入的資訊是否正確?(Y/N) ")
            YES = Y_N.split()
            if YES == "N":
                return

            self.student.addStudent(new_student_info)
            #[to fix] column mis match problem

            print("New student added successfully.")
        except Exception as e:
            print("Error occurred while adding new student:", e)
        
    def updateGrade(self, sid):
        #[todo]:更新指定學生的成績+重新計算該學生的成績平均&等第
        try:

            if sid not in self.student.studentInfo.index:
                print(sid, "not found")
                return

            lab1 = float(input("Enter new lab1 score: "))
            lab2 = float(input("Enter new lab2 score: "))
            lab3 = float(input("Enter new lab3 score: "))
            mid_term = float(input("Enter new midterm score: "))
            final_exam = float(input("Enter new final exam score: "))
            student_name = self.student.studentInfo.at[sid,"name"]

            # 更新學生的成績
            self.student.updateScoreOfStudent(sid, 'lab1', lab1)
            self.student.updateScoreOfStudent(sid, 'lab2', lab2)
            self.student.updateScoreOfStudent(sid, 'lab3', lab3)
            self.student.updateScoreOfStudent(sid, 'midTerm', mid_term)
            self.student.updateScoreOfStudent(sid, 'finalExam', final_exam)

            print("新增資訊為: ", sid, " ", student_name, " ", lab1, " ", lab2, " ", lab3, " ", mid_term, " ", final_exam, " ",)
            Y_N = input("請確認您輸入的資訊是否正確?(Y/N) ")
            YES = Y_N.split()
            if YES == "N":
                return

            print("Student scores updated successfully.")

        except ValueError:
            print("輸入無效")
        except Exception as e:
            print("Error occurred while updating student scores:", e)
        
    def updateWeights(self):
        #[todo]:更新加權+重新計算所有學生的平均&等第
        try:
            new_weight = [float(x) for x in input("請依照順序輸入加權(順序: lab1 lab2 lab3 midTerm finalExam): ").split()]

            if len(new_weight) != 5 :
                print("無效輸入，請重新輸入")
                return

            print("新增資訊為: ",new_weight)
            Y_N = input("請確認您輸入的資訊是否正確?(Y/N) ")
            YES = Y_N.split()
            if YES == "N":
                return
            
            self.student.updateWeight(new_weight)
            self.student.updateAverage()
            self.student.updateGrade()

            print("Weights updated and grades recalculated successfully.")

        except ValueError:
            print("輸入無效")
        except Exception as e:
            print("Error occurred while updating weights and recalculating grades:", e)

    def showMenu(self):
        #[todo]:印出menu
        print("Welcome to the Grade System.")
        print("0) Show menu")
        print("1) Show grade")
        print("2) Show grade letter")
        print("3) Show average")
        print("4) Show rank")
        print("5) Show distribution")
        print("6) Filtering")
        print("7) Add student")
        print("8) Update grade")
        print("9) Update weights")
        print("10) Exit")
        print("請輸入指令(0~10)開始使用: ")
    
    def exit(self):
        #[todo]:離開
        print("~歡迎下次再使用該系統，祝您有美好的一天~")
    
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
    query.showScore(995002901)
    


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

    # ----- UAT  --------------#
    #testFunc(student, query)

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
    

    # ===============================================
    print(UI)
    while(True):
        cmd = input("請輸入指令(0~10)開始使用: ")
        #[todo]:補齊剩下的10個功能
        #0.輸出UI
        if cmd == "0":
            query.showMenu()
        elif cmd =="1":
            sid = input("請輸入ID: ")
            sid = int(sid)
            query.showScore(sid)
        #2.獲得學生ID+輸出學生等第
        elif cmd == "2":
            sid = input("請輸入ID: ")
            sid = int(sid)
            query.showGradeLetter(sid)
        #3.獲得學生ID+輸出學生平均
        elif cmd == "3":
            sucess = False
            sid = input("請輸入ID: ")
            sid = int(sid)
            query.showAverage(sid)
            
        #4.獲得學生ID+輸出學生名次
        elif cmd == "4":
            sid = input("請輸入ID: ")
            sid = int(sid)
            query.showRank(sid)
        #5.輸出統計人數
        elif cmd == "5":
            query.showDistribution()
        #6.獲得分數+輸出符合學生
        elif cmd == "6":
            scoreLargerThan = input("請輸入指定分數: ")
            scoreLargerThan = int(scoreLargerThan)
            query.filtering(scoreLargerThan)
        #7.獲得要新增的學生資訊+放進去
        elif cmd == "7":
            query.addStudent()
        #8.獲得要更新的學生和資訊+放進去
        elif cmd == "8":
            sid = input("請輸入ID: ")
            sid = int(sid)
            query.updateGrade(sid)
        #9.獲得要新加權+更新
        elif cmd == "9":
            query.updateWeights()
        #10.離開
        elif cmd == "10":
            query.exit()
            break
        else:  
            print("輸入錯誤!")
    
    

    
    

# python gradeSystem.py