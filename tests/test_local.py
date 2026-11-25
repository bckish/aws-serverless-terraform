import unittest
from Backend.GETmethod import get_students
from Backend.POSTmethod import add_student
from local_server import LocalTable


class StudentTests(unittest.TestCase):
    def test_add_and_read(self):
        table = LocalTable()
        self.assertEqual(add_student({"roll_number": "1", "student_name": "Demo", "student_class": "Class 1"}, table)["statusCode"], 200)
        self.assertEqual(get_students(table)[0]["student_name"], "Demo")
        self.assertEqual(add_student({}, table)["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()
