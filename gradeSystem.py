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

[3.25]
1.加權更新後爆掉(猜測可能平均計算的問題)
2.新增學生
3.多加一句話 (已完成)
4.回傳10 (已完成)
"""

import pandas as pd
from tabulate import tabulate
import numpy as np
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

class Students:
    
    def __init__(self):
        self.studentInfo: pd.DataFrame = None
        self.subjectNames = ["id", "name", "lab1", "lab2", "lab3", "midTerm", "finalExam"]
        self.weight= np.array([0.1, 0.1, 0.1, 0.3, 0.4])
        # 每個student一個row
        # col 為lab1, lab2,.... ,weighted average, grade

    def createTable(self, data)->None:
        """
        Create table for student info

        Parameters
        -------
        :param data: student info data table
        :type data: list of list 

        Return
        ------
        :returns: None
        :rtype: None

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
        :param newWeight: list of float
        :type newWeight: list of float
        Return
        ------
        :returns: None
        :rtype: None
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
        print self.studentInfo for debugging

        Parameters
        ------
        :param None

        Return
        ------
        :returns: None
        :rtype: None
        """
        assert self.studentInfo is not None
        print(tabulate(self.studentInfo, headers='keys', tablefmt='psql'))

    def addStudent(self, data):
        """
        add a student into self.studentInfo

        Parameters
        ------
        :param data: student info to be added, list in order align with self.subjectNames
        :type data: list

        Return
        ------
        :returns: None
        :rtype: None
        """
        assert(len(data)==7)
        data.append(np.nan)
        data.append(np.nan)
        # new_row = pd.DataFrame([data[1:]], columns=self.studentInfo.columns, index=[data[0]])
        # self.studentInfo.loc[len(self.studentInfo)] = data

        self.studentInfo.loc[data[0]] = data[1:]
        self.updateAverageOfStudent(len(self.studentInfo)-1)
        self.updateGradeOfStudent(len(self.studentInfo)-1)

    def updateAverageOfStudent(self, row):
        """
        update average score of a student by calculating weighted average from self.weight

        Parameters
        ------
        :param row: row index of the student
        :type row: int

        Return
        ------
        :returns: None
        :rtype: None
        """
        first_col = self.studentInfo.columns.get_loc("lab1")
        last_col = self.studentInfo.columns.get_loc("finalExam")
        self.studentInfo.iloc[row, self.studentInfo.columns.get_loc("average")] = np.sum(
                        self.studentInfo.iloc[row, first_col:last_col+1] * self.weight)
    def updateGradeOfStudent(self, row):
        """
        update letter grade of a student by calculating from average score

        Parameters
        ------
        :param row: row index of the student
        :type row: int

        Return
        ------
        :returns: None
        :rtype: None

        """
        self.studentInfo.iloc[row, self.studentInfo.columns.get_loc("grade")] = self.scoreToGrade(self.studentInfo.iloc[row, self.studentInfo.columns.get_loc("average")])

    def updateAverage(self):
        """
        update average score of all students by calculating weighted average from self.weight
        
        Parameters
        ------
        :param None

        Return
        ------
        :returns: None
        :rtype: None        
        """
        
        # 重算average 的Column
        first_col = self.studentInfo.columns.get_loc("lab1")
        last_col = self.studentInfo.columns.get_loc("finalExam")
        for row in range(len(self.studentInfo)):
            self.studentInfo.iloc[row, self.studentInfo.columns.get_loc("average")] = np.sum(self.studentInfo.iloc[row, first_col:last_col+1] * self.weight)

    def updateGrade(self):
        """
        update letter grade of all students by calculating from average score
        
        Parameters
        ------
        :param None

        Return
        ------
        :returns: None
        :rtype: None        
        """
        
        # 重算grade 的column
        for row in range(len(self.studentInfo)):
            self.studentInfo.iloc[row, self.studentInfo.columns.get_loc("grade")] = self.scoreToGrade(self.studentInfo.iloc[row, self.studentInfo.columns.get_loc("average")])
            
    def scoreToGrade(self, score)->str:
        """
        Convert score to letter grade

        Parameters
        ------
        :param score: average score of a student
        :type score: float

        Return
        ------
        :return: letter grade
        :rtype: str
        
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





class Query:
    def __init__(self, student) -> None:
        """
        Initialize the Query class with a student object.

        Parameters
        -------
        :param student: The student object
        :type student: Student

        Return
        ------
        :returns: None
        :rtype: None
        """
        self.student=student
    
    def showScore(self, sid)->int:
        """
        Show the score of a student with a given student ID.

        Parameters
        -------
        :param sid: The student ID
        :type sid: int

        Return
        ------
        :returns: 1 if successful, 0 otherwise
        :rtype: int
        """
        #[update]:要判斷輸入的id是否真實存在，加上輸出學生的ID和姓名
        try:
            print(tabulate(self.student.studentInfo.loc[[sid]], headers='keys', tablefmt='psql'))
            return 1
        except Exception as e:
            print("Error occurred while printing student score:", e)
            return 0
    def showGradeLetter(self, sid)->int:
        """
        Show the grade letter of a student with a given student ID.

        Parameters
        -------
        :param sid: The student ID
        :type sid: int

        Return
        ------
        :returns: 1 if successful, 0 otherwise
        :rtype: int
        """
        #[todo]:印出學生等第的那一排
        try:
            student_average = self.student.studentInfo.at[sid,"average"]
            student_grade = self.student.scoreToGrade(student_average)
            student_name = self.student.studentInfo.at[sid,"name"]
            print("Student ID:",sid)
            print("Student Name:",student_name)
            print("Student Grade letter:",student_grade)
            return 1
        except KeyError:
            print("找不到Student ID:",sid,",請重新輸入")
            return 0

        
    def showAverage(self, sid):
        """
        Show the average score of a student with a given student ID.

        Parameters
        -------
        :param sid: The student ID
        :type sid: int

        Return
        ------
        :returns: 1 if successful, 0 otherwise
        :rtype: int
        """
        #[todo]:印出學生平均成績的那一排
        try:
            student_average = self.student.studentInfo.at[sid,"average"]
            student_name = self.student.studentInfo.at[sid,"name"]
            print("Student ID:",sid)
            print("Student Name:",student_name)
            print("Student Average:",student_average)
            return 1
        except KeyError:
            print("Student ID:",sid,"not found")
            return 0

        
    def showRank(self, sid):
        """
        Show the rank of a student with a given student ID.

        Parameters
        -------
        :param sid: The student ID
        :type sid: int

        Return
        ------
        :returns: 1 if successful, 0 otherwise
        :rtype: int
        """
        #[todo]:計算排名+印出排名
        try:
            sorted_students = self.student.studentInfo.sort_values(by='average', ascending=False)
            student_rank = sorted_students.index.get_loc(sid)+1
            student_name = self.student.studentInfo.at[sid,"name"]
            print("Student ID:",sid)
            print("Student Name:",student_name)
            print("Student Rank:", student_rank)
            return 1
        except KeyError:
            print("Student ID:",sid,"not found")
            return 0


    def showDistribution(self):
        """
        Show the distribution of grades of all students.

        Parameters
        -------
        :param None

        Return
        ------
        :returns: 1 if successful, 0 otherwise
        :rtype: int
        """
        #[todo]:迴圈統計人數+印出排名
        try:
            grade_distribution = self.student.studentInfo.groupby('grade').size().reset_index(name='count')
            print("Grade Distribution:")
            print(tabulate(grade_distribution, headers='keys', tablefmt='psql'))
            return 1
        except Exception as e:
            print("Error occurred while printing grade distribution:", e)
            return 0

    def filtering(self, scoreLargerThan):
        """
        Show students with an average score larger than a given value.

        Parameters
        -------
        :param scoreLargerThan: The score threshold
        :type scoreLargerThan: float

        Return
        ------
        :returns: 1 if successful, 0 otherwise
        :rtype: int
        """
        #[todo]:迴圈跑一次所有學生，符合標準的印出來
        try:
            assert(isinstance(scoreLargerThan, int) or isinstance(scoreLargerThan, float))
        except AssertionError:
            print("輸入無效")
            return 0
        try:
            above_scoreLargeThan = self.student.studentInfo[self.student.studentInfo['average'] > scoreLargerThan]
            if above_scoreLargeThan.empty:
                print("No student")
            else:
                print(tabulate(above_scoreLargeThan, headers='keys', tablefmt='psql'))
            return 1
        except Exception as e:
            print("打印成績分佈時出現錯誤:", e)
            return 0

    def addStudent(self):
        """
        Add a new student.

        Parameters
        -------
        :param None

        Return
        ------
        :returns: 1 if successful, 0 otherwise
        :rtype: int
        """
        try:
            student_info_list = input("請依格式輸入新增的學生資訊(格式: ID Name lab1 lab2 lab3 midTerm finalExam): ").split()
            if len(student_info_list) != 7:
                print("未依格式輸入資訊，請重新確認您的資訊~")
                return 0
            new_student_info = [student_info_list[0], student_info_list[1]] + list(map(float, student_info_list[2:]))
            print("新增資訊為: ", new_student_info)
            if input("請確認您輸入的資訊是否正確?(Y/N) ").lower().strip() == "y":
                self.student.addStudent(new_student_info)
                print("Student added successfully.")
                return 1
            else:
                print("輸入未獲確認,請重新輸入")
                return 0
        except Exception as e:
            print("新增學生時出現錯誤: ", e)
            return 0

        
    def updateGrade(self, sid):
        """
        Update the grade of a student with a given student ID.

        Parameters
        -------
        :param sid: The student ID
        :type sid: int

        Return
        ------
        :returns: 1 if successful, 0 otherwise
        :rtype: int
        """
        while True:
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

                print("新增資訊為: ", sid, " ", student_name, " ", lab1, " ", lab2, " ", lab3, " ", mid_term, " ", final_exam, " ",)
                Y_N = input("請確認您輸入的資訊是否正確?(Y/N) ")
                YES = Y_N.lower()
                if YES == "n":
                    print("輸入未獲確認,請重新輸入")
                    continue
                else:
                    # 更新學生的成績
                    self.student.updateScoreOfStudent(sid, 'lab1', lab1)
                    self.student.updateScoreOfStudent(sid, 'lab2', lab2)
                    self.student.updateScoreOfStudent(sid, 'lab3', lab3)
                    self.student.updateScoreOfStudent(sid, 'midTerm', mid_term)
                    self.student.updateScoreOfStudent(sid, 'finalExam', final_exam)
                    print("Student scores updated successfully.")
                    return 1

            except ValueError:
                print("輸入無效")
                return 0
            except Exception as e:
                print("更新成績時出現錯誤:", e)
                return 0
        
    def updateWeights(self):
        """
        Update the weights for calculating the average score.

        Parameters
        -------
        :param None

        Return
        ------
        :returns: 1 if successful, 0 otherwise
        :rtype: int
        """
        #[todo]:更新加權+重新計算所有學生的平均&等第
        while(True):
            try:
                new_weight = [float(x) for x in input("請依照順序輸入加權(註: 加權總和必須等於1)(順序: lab1 lab2 lab3 midTerm finalExam): ").split()]

                if len(new_weight) != 5 or sum(new_weight) != 1:
                    print("無效輸入，請重新輸入")
                    return

                print("新增資訊為: ",new_weight)
                Y_N = input("請確認您輸入的資訊是否正確?(Y/N) ")
                YES = Y_N.lower().split()
                if YES == "n":
                    print("輸入未獲確認,請重新輸入")
                    continue
                else:
                    self.student.updateWeight(new_weight)
                    self.student.updateAverage()
                    self.student.updateGrade()
                    print("Weights updated and grades recalculated successfully.")
                    return 1

            except ValueError:
                print("輸入無效")
                return 0
            except Exception as e:
                print("更新加權時出現錯誤:", e)
                return 0

    def showMenu(self):
        """
        Show the menu.

        Parameters
        -------
        :param None

        Return
        ------
        :returns: 1 if successful, 0 otherwise
        :rtype: int
        """
        #[todo]:印出menu
        print(UI)

        return 1
    
    def exit(self):
        """
        Exit the system.

        Parameters
        -------
        :param None

        Return
        ------
        :returns: None
        :rtype: None
        """
        #[todo]:離開
        print("現在正在執行 10.Exit")
        print("~歡迎下次再使用該系統，祝您有美好的一天~")

    
def readInput()->list:
    """
    Read student data from text file "input.txt".

    Parameters
    -------
    :param None

    Return
    ------
    :returns: A list of lists containing student data
    :rtype: list
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
    """
    Check the sanity of the data.

    Parameters
    -------
    :param data: The data to be checked, expected to be student info
    :type data: list of list of strings
    :param toPrint: Whether to print the first 5 rows of the data
    :type toPrint: bool

    Return
    ------
    :returns: None
    :rtype: None
    """

    assert isinstance(data, list)
    assert isinstance(data[0], list)
    for i in range(7):
        assert isinstance(data[i], list)
            
    # print first 5 rows if toPrint==true for sanity check
    if toPrint:
        for i in range(5):
            print(f"row {i}", sep="\t")
            print(data[i])
    


def uat(student, query):
    """
    內部測試用
    
    """
    ### test case 1
    # [to do] move this to unit test
    print("===================\n====================")
    print("no. of col")
    print(len(student.studentInfo.columns))
    print(student.studentInfo.columns)
    student.updateScoreOfStudent(955002056, "lab1", 1)
    new_student = [10, "陳小明", 10.0, 10.0, 10.0, 10.0, 10.0]
    student.addStudent(new_student)
    student.printTable()

    ## testing query
    #query.showScore(10)
    


if __name__ == "__main__":
    """
    This is the main entry point of the program. It performs the following steps:
    
    1. Reads input data and performs a sanity check on it.
    2. Initializes the Students and Query objects, and creates a table with the input data.
    3. Prints the user interface and enters an infinite loop waiting for user commands.
    Depending on the command entered, it performs various operations such as showing the score, grade letter, average, rank, distribution, filtering students, adding a student, updating grade, updating weights, or exiting the program.
    """


    #------ Read Input --------#

    data = readInput()
    sanityCheck(data, False)

    # ------ Initialization  ---------#
    student = Students()
    query = Query(student)
    student.createTable(data)

    # ----- UAT  --------------#
    # uat(student, query)

    # ------ mian function  -------#

    
    

    # ===============================================
    print(UI)
    while(True):
        cmd = input("請輸入指令(0~10)開始使用: ")
        #[todo]:補齊剩下的10個功能
        #0.輸出UI
        if cmd == "0":
            success = 0
            while(success==0):
                success = query.showMenu()
        elif cmd =="1":
            print("現在正在執行 1.Show score")
            success = 0
            while(success==0):
                sid = input("請輸入ID: ")
                try:
                    sid = int(sid)
                except ValueError:
                    print("輸入無效, 請重新輸入")
                    continue
                success = query.showScore(sid)
        #2.獲得學生ID+輸出學生等第
        elif cmd == "2":
            print("現在正在執行 2.Show grade letter")
            success = 0
            while(success==0):
                sid = input("請輸入ID: ")
                try:
                    sid = int(sid)
                except ValueError:
                    print("輸入無效, 請重新輸入")
                    continue
                success = query.showGradeLetter(sid)
        #3.獲得學生ID+輸出學生平均
        elif cmd == "3":
            print("現在正在執行 3.Show average")
            success = 0
            while(success==0):
                sucess = False
                sid = input("請輸入ID: ")
                try:
                    sid = int(sid)
                except ValueError:
                    print("輸入無效, 請重新輸入")
                    continue
                success = query.showAverage(sid)     
        #4.獲得學生ID+輸出學生名次
        elif cmd == "4":
            print("現在正在執行 4.Show rank")
            success = 0
            while(success==0):
                sid = input("請輸入ID: ")
                try:
                    sid = int(sid)
                except ValueError:
                    print("輸入無效, 請重新輸入")
                    continue
                success = query.showRank(sid)
        #5.輸出統計人數
        elif cmd == "5":
            print("現在正在執行 5.Show distribution")
            success = 0
            while(success==0):
                success = query.showDistribution()
        #6.獲得分數+輸出符合學生
        elif cmd == "6":
            print("現在正在執行 6.Filtering")
            success = 0
            while(success==0):
                scoreLargerThan = input("請輸入指定分數: ")
                try:
                    scoreLargerThan = int(scoreLargerThan)
                except ValueError:
                    print("輸入無效, 請重新輸入")
                    continue
                success = query.filtering(scoreLargerThan)
        #7.獲得要新增的學生資訊+放進去
        elif cmd == "7":
            print("現在正在執行 7.Add student")
            success = 0
            while(success==0):
                success = query.addStudent()
        #8.獲得要更新的學生和資訊+放進去
        elif cmd == "8":
            print("現在正在執行 8.Update grade")
            success = 0
            while(success==0):
                sid = input("請輸入ID: ")
                try:
                    sid = int(sid)
                except ValueError:
                    print("輸入無效, 請重新輸入")
                    continue
                success = query.updateGrade(sid)
        #9.獲得要新加權+更新
        elif cmd == "9":
            print("現在正在執行 9.Update weights")
            success = 0
            while(success==0):
                success = query.updateWeights()
        #10.離開
        elif cmd == "10":
            query.exit()
            break
        else:  
            print("輸入錯誤!")
    
    

    
    

# python gradeSystem.py