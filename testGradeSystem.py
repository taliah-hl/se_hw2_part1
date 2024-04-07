import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch

from gradeSystem import *

SID1 = 1001
SID2 = 1002
SID3 = 1003
INVALID_SID = 9999

class TestGradeSystem(unittest.TestCase):

    # def test_test(self):
    #     # assert false to check if test is working
    #     self.assertFalse(False, "Test is working")

    def test_readInput(self):
        """
        Test function: readInput()
        Test description:
        - run the eadInput() function
        - Check if the return value is a list
        """
        data = readInput()
        self.assertIsInstance(data, list, "Return value is not a list")
        if data:  # check if data is not empty
            self.assertIsInstance(data[0], list, "First element in the list is not a list")
            if data[0]:  # check if first element is not empty
                self.assertIsInstance(data[0][0], int, "First element in the sublist is not an integer")

    def test_sanityCheck(self):
        """
        test function: sanityCheck(data)
        test description:
        - the sanityCheck() checks if the input data is in the correct format, 
        such as number of string in each row.
        - Check if the function runs without raising an exception
        """
        data = readInput()
        try:
            sanityCheck(data)
        except Exception as e:
            self.fail(f"sanityCheck raised exception {e}")

    
class TestStudents(unittest.TestCase):

    def setUp(self):
        """
        description:
        - create an instance of Students class
        - create a data table with 2 students
        """
        self.students = Students()
        self.data = [[SID1, '陳一明', 80, 85, 90, 95, 100],
                     [SID2, '陳二明', 70, 75, 80, 85, 90]]
        self.students.createTable(self.data)

    def test_createTable(self):
        """
        Test function: createTable(data)
        Test description:
        - Check if student added in setUp exist
        - Check if some scores of the students are correct
        """
        self.assertEqual(len(self.students.studentInfo), 2)
        self.assertEqual(self.students.studentInfo.loc[SID1, 'name'], '陳一明')
        self.assertEqual(self.students.studentInfo.loc[SID1, 'lab1'], 80)
        self.assertEqual(self.students.studentInfo.loc[SID2, 'name'], '陳二明')
        self.assertEqual(self.students.studentInfo.loc[SID2, 'lab2'], 75)

    def test_updateWeight(self):
        """
        Test function: updateWeight(newWeight)
        Test description:
        - update the weight of the students to [0.2, 0.2, 0.2, 0.2, 0.2]
        - Check if the weight is updated correctly
        """
        newWeight = [0.2, 0.2, 0.2, 0.2, 0.2]
        self.students.updateWeight(newWeight)
        np.testing.assert_array_equal(self.students.weight, np.array(newWeight))

    def test_addStudent(self):
        """
        Test function: addStudent(new_student)
        Test description:
        - add a student as followed:
            - sid: SID3
            - name: 陳三明
            - lab1: 60
            - lab2: 65
            - lab3: 70
            - midTerm: 75
            - finalExam: 80

        """
        new_student = [SID3, '陳三明', 60, 65, 70, 75, 80]
        self.students.addStudent(new_student)
        self.assertEqual(len(self.students.studentInfo), 3)
        self.assertEqual(self.students.studentInfo.loc[SID3, 'name'], '陳三明')
        self.assertEqual(self.students.studentInfo.loc[SID3, 'finalExam'], 80)

    def test_updateAverageOfStudent(self):
        """
        Test function: updateAverageOfStudent(sid)
        Test description:
        - sid: SID1
        - update the average of the first student
        - assert average is not NA
        """
        self.students.updateAverageOfStudent(0)
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'average']))

    def test_updateAverageFromSid(self):
        """
        Test function: updateAverageFromSid(sid)
        Test description:
        - sid: SID1
        - update the average of the first student
        - assert average is not NA
        """
        self.students.updateAverageFromSid(SID1)
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'average']))

    def test_updateGradeOfStudent(self):
        """
        Test function: updateGradeOfStudent(sid)
        Test description:
        - sid: SID1
        - update the grade of the first student
        - assert grade is not NA
        """
        self.students.updateGradeOfStudent(0)
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'grade']))

    def test_updateGradeFromSid(self):
        """
        Test function: updateGradeFromSid(sid)
        Test description:
        - sid: SID1
        - update the grade of the first student
        - assert grade is not NA
        """
        self.students.updateGradeFromSid(SID1)
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'grade']))

    def test_updateAverage(self):
        """
        Test function: updateAverage()
        Test description:
        - update the average of all students
        - assert avearge of all students are not NaN
        """
        self.students.updateAverage()
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'average']))
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID2, 'average']))

    def test_updateGrade(self):
        """
        Test function: updateGrade()
        Test description:
        - update the grade of all students
        - assert grade of all students are not NaN
        """
        self.students.updateGrade()
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'grade']))
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID2, 'grade']))

    def test_scoreToGrade(self):
        """
        
        Test function: scoreToGrade(score)
        Test description:
        - test the scoreToGrade function with different scores
        """
        self.assertEqual(self.students.scoreToGrade(95), 'A+')
        self.assertEqual(self.students.scoreToGrade(85), 'A')
        self.assertEqual(self.students.scoreToGrade(75), 'B')

    def test_updateScoreOfStudent(self):
        """
        Test function: updateScoreOfStudent(sid, subject, score)
        Test description:
        - update the score of  the first student in lab1 to 85
        - assert the score is updated correctly
        """
        self.assertEqual(self.students.updateScoreOfStudent(SID1, 'lab1', 85), 1)
        self.assertEqual(self.students.studentInfo.loc[SID1, 'lab1'], 85)



class TestQuery(unittest.TestCase):

    def setUp(self):
        """

        description:
        - create an instance of Students class
        - create a data table with 2 students
        - create an instance of Query class with the Students instance
        """
        self.student = Students()
        self.data = [[SID1, '陳一明', 80, 85, 90, 95, 100],
                     [SID2, '陳二明', 70, 75, 80, 85, 90]]
        self.student.createTable(self.data)
        self.query = Query(self.student)

    def test_showScore(self):
        """
        Test function: showScore(sid)
        Test description:
        - sid: SID1
        - assert return value is 1 which denote success

        """
        self.assertEqual(self.query.showScore(SID1), 1)

    def test_showGradeLetter(self):
        """
        Test function: showGradeLetter(sid)
        Test description:
        - sid: SID1
        - assert return value is 1 which denote success

        """
        self.assertEqual(self.query.showGradeLetter(SID1), 1)

    def test_showAverage(self):
        """
        Test function: test_showAverage(sid)
        Test description:
        - sid: SID1
        - assert return value is 1 which denote success

        """
        self.assertEqual(self.query.showAverage(SID1), 1)

    def test_showRank(self):
        """
        Test function: test_showRank()
        Test description:
        - assert return value is 1 which denote success

        """
        self.assertEqual(self.query.showRank(SID1), 1)

    def test_showDistribution(self):
        """
        Test function: test_showDistribution()
        Test description:
        - assert return value is 1 which denote success

        """
        self.assertEqual(self.query.showDistribution(), 1)

    def test_filtering(self):
        """
        Test function: test_filtering()
        Test description:
        - assert return value is 1 which denote success

        """
        self.assertEqual(self.query.filtering(80), 1)

    @patch('builtins.input', side_effect=['12345 John 90 90 90 90 90', 'y'])
    def test_addStudent(self, mock_input):
        """
        Test function: test_addStudent()
        Test description:
        - add a student with the following information:
            - sid: 12345
            - name: John
            - lab1: 90
            - lab2: 90
            - lab3: 90
            - midTerm: 90
            - finalExam: 90
        - assert return value is 1 which denote success
        """

        self.assertEqual(self.query.addStudent(), 1)

    @patch('builtins.input', side_effect=['90', '90', '90', '90', '90', 'y'])
    def test_updateGrade(self, mock_input):
        """
        Test function: test_updateGrade()
        Test description:
        - update the grade of the first student to ['90', '90', '90', '90', '90']
        - check if return value is 1 which denote successd

        """
        self.assertEqual(self.query.updateGrade(SID1), 1)

    def test_printWeight(self):
        self.assertEqual(self.query.printWeight(), 1)

    @patch('builtins.input', side_effect=['0.2 0.2 0.2 0.2 0.2', 'y'])
    def test_updateWeights(self, mock_input):
        """
        test function: updateWeights()
        test description:
        - update the weight of the students to [0.2, 0.2, 0.2, 0.2, 0.2]
        - assert return value is 1 which denote success
        """
        # This test may need to be modified based on how the updateWeights method is implemented
        self.assertEqual(self.query.updateWeights(), 1)

    def test_showMenu(self):
        """
        test function: showMenu()
        test description:
        - assert return value is 1 which denote success
        """
        self.assertEqual(self.query.showMenu(), 1)

    def test_printStudentInfo(self):
        """
        test function: test_printStudentInfo()
        test description:
        - assert return value is 1 which denote success
        """
        # This test may need to be modified based on how the printStudentInfo method is implemented
        self.assertEqual(self.query.printStudentInfo(), 1)

    def test_exit(self):
        """
        test function: test_exit()
        test description:
        - assert return value is 1 which denote success
        """
        # This test may need to be modified based on how the exit method is implemented
        self.assertEqual(self.query.exit(), 1)

class IntegratedTest1(unittest.TestCase):
    """
    test happy flow of each available inqury method in Query class
    
    - test_part_1: test the functionality of the happy flow of all methods in Query class
    - test_addStudent: test is rank, average, is updated correctly after adding student
    - test_updateGrade, test_updateGrade2: test is grade, average, grade letter still correct after update grade
    - test_updateWeights: test is average of student correct after updating weight
    """
    def setUp(self):
        """
        description:
        - create an instance of Students class
        - create a data table with 2 students
        - create an instance of Query class with the Students instance
        """
        self.student = Students()
        self.data = [[SID1, '陳一明', 80, 80, 80, 80, 80],
                     [SID2, '陳二明', 90, 90, 90, 90, 90]]
        self.student.createTable(self.data)
        self.query = Query(self.student)

    def test_part_1(self):
        """
        Test the execution of the following steps:
        - query.showScore() of valid and invalid SID
        - query.showGradeLetter() of valid and invalid SID
        - query.showAverage() of valid and invalid SID
        - assert exsiting student's average is correct
        - assert student rank is correct
        - test query.showRank()
        - test query.showDistribution()
        - test query.filtering()
        - test query.printWeight()
        - check value of weight is same as default (0.1, 0.1, 0.1, 0.3, 0.4)
        - test query.showMenu()
        - test query.printStudentInfo()
        - test query.exit()
        
        """
        self.assertEqual(self.query.showScore(SID1), 1)
        self.assertEqual(self.query.showScore(INVALID_SID), 0)   # assert an invalid SID does not exist
        self.assertEqual(self.query.showGradeLetter(SID1), 1)
        self.assertEqual(self.query.showGradeLetter(INVALID_SID), 0)
        self.assertEqual(self.query.showAverage(SID1), 1)
        self.assertEqual(self.query.showAverage(INVALID_SID), 0)

        # check average of existing students
        self.assertEqual(self.student.studentInfo.at[SID1,"average"], 80)
        self.assertEqual(self.student.studentInfo.at[SID2,"average"], 90)

        # check rank of existing students
        sorted_students = self.student.studentInfo.sort_values(by='average', ascending=False)
        student_rank = sorted_students.index.get_loc(SID1)+1
        self.assertEqual(student_rank, 2)
        self.assertEqual(self.query.showRank(SID1), 1)


        self.assertEqual(self.query.showRank(INVALID_SID), 0)
        self.assertEqual(self.query.showDistribution(), 1)
        self.assertEqual(self.query.filtering(80), 1)
        self.assertEqual(self.query.printWeight(), 1)

        self.assertEqual(self.student.weight[0], 0.1)
        self.assertEqual(self.student.weight[1], 0.1)
        self.assertEqual(self.student.weight[2], 0.1)
        self.assertEqual(self.student.weight[3], 0.3)
        self.assertEqual(self.student.weight[4], 0.4)
        self.assertEqual(self.query.showMenu(), 1)
        self.assertEqual(self.query.printStudentInfo(), 1)
        self.assertEqual(self.query.exit(), 1)


    @patch('builtins.input', side_effect=['12345 John 95 95 95 95 95', 'y'])
    def test_addStudent(self, mock_input):
        """
        Test the execution of the following steps:
        - add John
        - check John is added
        - check John's average is correct
        - check John's and other student's rank is correct
        
        """
        self.assertEqual(self.query.addStudent(), 1)
        self.assertEqual(self.student.studentInfo.at[12345,"name"], "John")
        self.assertEqual(self.student.studentInfo.at[12345,"average"], 95)
        sorted_students = self.student.studentInfo.sort_values(by='average', ascending=False)
        student_rank = sorted_students.index.get_loc(SID1)+1
        self.assertEqual(student_rank, 3)
        student_rank = sorted_students.index.get_loc(12345)+1
        self.assertEqual(student_rank, 1)


    @patch('builtins.input', side_effect=['99', '99', '99', '99', '99', 'y'])
    def test_updateGrade(self, mock_input):
        """
        Test the execution of the following steps:
        - update grade of student 1 to [99, 99, 99, 99, 99]
        - check average of updated and non-updated student
        - check rank of updated student
        - check grade letter of updated student
        
        """
        self.assertEqual(self.query.updateGrade(SID1), 1)

        # check average after update grade
        self.assertEqual(self.student.studentInfo.at[SID1,"average"], 99)
        self.assertEqual(self.student.studentInfo.at[SID2,"average"], 90)


        # check rank after update grade
        sorted_students = self.student.studentInfo.sort_values(by='average', ascending=False)
        student_rank = sorted_students.index.get_loc(SID1)+1
        self.assertEqual(student_rank, 1)


        # check grade letter after update grade
        student_average = self.student.studentInfo.at[SID1,"average"]
        student_grade = self.student.scoreToGrade(student_average)
        self.assertEqual(student_grade, "A+")

    @patch('builtins.input', side_effect=['10', '20', '30', '40', '50', 'y'])
    def test_updateGrade2(self, mock_input):
        """
        
        Test the execution of the following steps:
        - update grade of student 1 to [10, 20, 30, 40, 50]
        - check average of updated and non-updated student
        - check rank of updated student
        - check grade letter of updated student
        """
        self.assertEqual(self.query.updateGrade(SID1), 1)

        # check average after update grade
        expected_avg = (10*0.1 + 20*0.1 + 30*0.1 + 40*0.3 + 50*0.4)# since default weight is [0.1, 0.1, 0.1, 0.3, 0.4]
        # 10*0.1 + 20*0.1 + 30*0.1 + 40*0.3 + 50*0.4 = 38
        self.assertEqual(self.student.studentInfo.at[SID1,"average"], expected_avg)


        # check rank after update grade

        sorted_students = self.student.studentInfo.sort_values(by='average', ascending=False)
        student_rank = sorted_students.index.get_loc(SID1)+1
        self.assertEqual(student_rank, 2)


        # check grade letter after update grade
        # 10*0.1 + 20*0.1 + 30*0.1 + 40*0.3 + 50*0.4 -> E
        student_average = self.student.studentInfo.at[SID1,"average"]
        student_grade = self.student.scoreToGrade(student_average)
        self.assertEqual(student_grade, "E")
        
    @patch('builtins.input', side_effect=['10', '20', '30', '40', '50', 'y','0.2 0.2 0.2 0.2 0.2', 'y'])
    def test_updateWeights(self, mock_input):
        """"
        test the execution of the following steps:
        - update student 1's grade to [10, 20, 30, 40, 50]
        - update weight to [0.2, 0.2, 0.2, 0.2, 0.2]
        - check the new average of student 1
        """
        
        self.assertEqual(self.query.updateGrade(SID1), 1)
        self.assertEqual(self.query.updateWeights(), 1)

        # check new avg of SID1 after update weight
        expected_avg = (10*0.2 + 20*0.2 + 30*0.2 + 40*0.2 + 50*0.2)
        #  (10*0.2 + 20*0.2 + 30*0.2 + 40*0.2 + 50*0.2) = 30
        self.assertEqual(self.student.studentInfo.at[SID1,"average"], expected_avg)


class IntegratedTest2(unittest.TestCase):
    """
    test unhappy flow of add student, update grade, update weight 
    """

    def setUp(self):
        """

        description:
        - create an instance of Students class
        - create a data table with 2 students
        - create an instance of Query class with the Students instance
        """
        self.student = Students()
        self.data = [[SID1, '陳一明', 80, 80, 80, 80, 80],
                     [SID2, '陳二明', 90, 90, 90, 90, 90]]
        self.student.createTable(self.data)
        self.query = Query(self.student)

    @patch('builtins.input', side_effect=['12345'])
    def test_addStudent1(self, mock_input):
        """"
        test input wrong format for add student
        """
        self.assertEqual(self.query.addStudent(), 0)

    @patch('builtins.input', side_effect=['12345 John 90 90 90 90 90', 'n'])
    def test_addStudent2(self, mock_input):
        """
        test the flow for user does not confirm student information
        """
        self.assertEqual(self.query.addStudent(), 0)


    @patch('builtins.input', side_effect=['abc', 'abc', 'abc', 'abc', 'abc'])
    def test_updateGrade2(self, mock_input):
        """
        
        test flow of user input non-numeric grades
        
        """
        self.assertEqual(self.query.updateGrade(SID1), 0)

    @patch('builtins.input', side_effect=['0.2 0.2 0.2', 'y'])
    def test_updateWeights1(self, mock_input):
        """
        Test flow of user inputting an inadequate number in weights.
        """
        self.assertEqual(self.query.updateWeights(), 0)

    @patch('builtins.input', side_effect=['abc abc abc abc abc', 'y'])
    def test_updateWeights2(self, mock_input):
        """
        Test flow of user inputting non-numeric weights.
        """
        self.assertEqual(self.query.updateWeights(), 0)
    
if __name__ == '__main__':
    unittest.main()

