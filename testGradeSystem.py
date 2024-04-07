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

    def test_test(self):
        # assert false to check if test is working
        self.assertFalse(False, "Test is working")

    def test_readInput(self):
        data = readInput()
        self.assertIsInstance(data, list, "Return value is not a list")
        if data:  # check if data is not empty
            self.assertIsInstance(data[0], list, "First element in the list is not a list")
            if data[0]:  # check if first element is not empty
                self.assertIsInstance(data[0][0], int, "First element in the sublist is not an integer")

    def test_sanityCheck(self):
        data = readInput()
        try:
            sanityCheck(data)
        except Exception as e:
            self.fail(f"sanityCheck raised exception {e}")

    
class TestStudents(unittest.TestCase):

    def setUp(self):
        self.students = Students()
        self.data = [[SID1, '陳一明', 80, 85, 90, 95, 100],
                     [SID2, '陳二明', 70, 75, 80, 85, 90]]
        self.students.createTable(self.data)

    def test_createTable(self):
        self.assertEqual(len(self.students.studentInfo), 2)
        self.assertEqual(self.students.studentInfo.loc[SID1, 'name'], '陳一明')
        self.assertEqual(self.students.studentInfo.loc[SID1, 'lab1'], 80)
        self.assertEqual(self.students.studentInfo.loc[SID2, 'name'], '陳二明')
        self.assertEqual(self.students.studentInfo.loc[SID2, 'lab2'], 75)

    def test_updateWeight(self):
        newWeight = [0.2, 0.2, 0.2, 0.2, 0.2]
        self.students.updateWeight(newWeight)
        np.testing.assert_array_equal(self.students.weight, np.array(newWeight))

    def test_addStudent(self):
        new_student = [SID3, '陳三明', 60, 65, 70, 75, 80]
        self.students.addStudent(new_student)
        self.assertEqual(len(self.students.studentInfo), 3)
        self.assertEqual(self.students.studentInfo.loc[SID3, 'name'], '陳三明')
        self.assertEqual(self.students.studentInfo.loc[SID3, 'finalExam'], 80)

    def test_updateAverageOfStudent(self):
        self.students.updateAverageOfStudent(0)
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'average']))

    def test_updateAverageFromSid(self):
        self.students.updateAverageFromSid(SID1)
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'average']))

    def test_updateGradeOfStudent(self):
        self.students.updateGradeOfStudent(0)
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'grade']))

    def test_updateGradeFromSid(self):
        self.students.updateGradeFromSid(SID1)
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'grade']))

    def test_updateAverage(self):
        self.students.updateAverage()
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'average']))
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID2, 'average']))

    def test_updateGrade(self):
        self.students.updateGrade()
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID1, 'grade']))
        self.assertFalse(pd.isna(self.students.studentInfo.loc[SID2, 'grade']))

    def test_scoreToGrade(self):
        self.assertEqual(self.students.scoreToGrade(95), 'A+')
        self.assertEqual(self.students.scoreToGrade(85), 'A')
        self.assertEqual(self.students.scoreToGrade(75), 'B')

    def test_updateScoreOfStudent(self):
        self.assertEqual(self.students.updateScoreOfStudent(SID1, 'lab1', 85), 1)
        self.assertEqual(self.students.studentInfo.loc[SID1, 'lab1'], 85)



class TestQuery(unittest.TestCase):
    def setUp(self):
        self.student = Students()
        self.data = [[SID1, '陳一明', 80, 85, 90, 95, 100],
                     [SID2, '陳二明', 70, 75, 80, 85, 90]]
        self.student.createTable(self.data)
        self.query = Query(self.student)

    def test_showScore(self):
        self.assertEqual(self.query.showScore(SID1), 1)

    def test_showGradeLetter(self):
        self.assertEqual(self.query.showGradeLetter(SID1), 1)

    def test_showAverage(self):
        self.assertEqual(self.query.showAverage(SID1), 1)

    def test_showRank(self):
        self.assertEqual(self.query.showRank(SID1), 1)

    def test_showDistribution(self):
        self.assertEqual(self.query.showDistribution(), 1)

    def test_filtering(self):
        self.assertEqual(self.query.filtering(80), 1)

    @patch('builtins.input', side_effect=['12345 John 90 90 90 90 90', 'y'])
    def test_addStudent(self, mock_input):
        self.assertEqual(self.query.addStudent(), 1)

    @patch('builtins.input', side_effect=['90', '90', '90', '90', '90', 'y'])
    def test_updateGrade(self, mock_input):
        self.assertEqual(self.query.updateGrade(SID1), 1)

    def test_printWeight(self):
        self.assertEqual(self.query.printWeight(), 1)

    @patch('builtins.input', side_effect=['0.2 0.2 0.2 0.2 0.2', 'y'])
    def test_updateWeights(self, mock_input):
        # This test may need to be modified based on how the updateWeights method is implemented
        self.assertEqual(self.query.updateWeights(), 1)

    def test_showMenu(self):
        self.assertEqual(self.query.showMenu(), 1)

    def test_printStudentInfo(self):
        # This test may need to be modified based on how the printStudentInfo method is implemented
        self.assertEqual(self.query.printStudentInfo(), 1)

    def test_exit(self):
        # This test may need to be modified based on how the exit method is implemented
        self.assertEqual(self.query.exit(), 1)

class IntegratedTest1(unittest.TestCase):
    """
    test happy flow of each available inqury
    """
    def setUp(self):
        self.student = Students()
        self.data = [[SID1, '陳一明', 80, 80, 80, 80, 80],
                     [SID2, '陳二明', 90, 90, 90, 90, 90]]
        self.student.createTable(self.data)
        self.query = Query(self.student)

    def test_part_1(self):
        self.assertEqual(self.query.showScore(SID1), 1)
        self.assertEqual(self.query.showScore(INVALID_SID), 0)   # assert an invalid SID does not exist
        self.assertEqual(self.query.showGradeLetter(SID1), 1)
        self.assertEqual(self.query.showGradeLetter(INVALID_SID), 0)
        self.assertEqual(self.query.showAverage(SID1), 1)
        self.assertEqual(self.query.showAverage(INVALID_SID), 0)
        self.assertEqual(self.student.studentInfo.at[SID1,"average"], 80)
        self.assertEqual(self.student.studentInfo.at[SID2,"average"], 90)
        sorted_students = self.student.studentInfo.sort_values(by='average', ascending=False)
        student_rank = sorted_students.index.get_loc(SID1)+1
        self.assertEqual(student_rank, 2)
        self.assertEqual(self.query.showRank(SID1), 1)
        self.assertEqual(self.query.showRank(INVALID_SID), 0)
        self.assertEqual(self.query.showDistribution(), 1)
        self.assertEqual(self.query.filtering(80), 1)
        self.assertEqual(self.query.printWeight(), 1)
        #self.assertEqual(self.student.weight, [0.1, 0.1, 0.1, 0.3, 0.4])
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

