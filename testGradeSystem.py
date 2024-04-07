import unittest
import pandas as pd
import numpy as np

from gradeSystem import *
SID1 = 1001
SID2 = 1002
SID3 = 1003

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
        self.assertNotEqual(self.students.studentInfo.loc[SID1, 'average'], pd.NA)

    def test_updateAverageFromSid(self):
        self.students.updateAverageFromSid(1)
        self.assertNotEqual(self.students.studentInfo.loc[SID1, 'average'], pd.NA)

    def test_updateGradeOfStudent(self):
        self.students.updateGradeOfStudent(0)
        self.assertNotEqual(self.students.studentInfo.loc[SID1, 'grade'], pd.NA)

    def test_updateGradeFromSid(self):
        self.students.updateGradeFromSid(SID1)
        self.assertNotEqual(self.students.studentInfo.loc[SID1, 'grade'], pd.NA)

    def test_updateAverage(self):
        self.students.updateAverage()
        self.assertNotEqual(self.students.studentInfo.loc[SID1, 'average'], pd.NA)
        self.assertNotEqual(self.students.studentInfo.loc[SID1, 'average'], pd.NA)

    def test_updateGrade(self):
        self.students.updateGrade()
        self.assertNotEqual(self.students.studentInfo.loc[SID1, 'grade'], pd.NA)
        self.assertNotEqual(self.students.studentInfo.loc[SID1, 'grade'], pd.NA)

    def test_scoreToGrade(self):
        self.assertEqual(self.students.scoreToGrade(95), 'A+')
        self.assertEqual(self.students.scoreToGrade(85), 'A')
        self.assertEqual(self.students.scoreToGrade(75), 'B')

    def test_updateScoreOfStudent(self):
        self.assertEqual(self.students.updateScoreOfStudent(SID1, 'lab1', 85), 1)
        self.assertEqual(self.students.studentInfo.loc[SID1, 'lab1'], 85)

if __name__ == '__main__':
    unittest.main()