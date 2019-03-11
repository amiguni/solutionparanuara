import unittest
from Sys_Paranuara import Welcome
from Sys_Paranuara import AllEmployees
from Sys_Paranuara import MutualFriends
from Sys_Paranuara import Likes


class TestSysParanuara(unittest.TestCase):

    def test_Welcome(self):
        result = Welcome.get(self)
        self.assertEqual(result, {
        "From": "Paranuara",
        "Message": "Welcome to class-m planet..",
        "End_Point_01": "/all_employees/<string:company_name>",
        "End_Point_02": "/mutual_friends/<name1,name2>",
        "End_Point_03": "/likes/<string:employee_name>"
        })

    def test_AllEmployees(self):
        result = AllEmployees.get(self,'ZILODYNE')
        self.assertEqual(result, ['ZILODYNE Employees:', 'Oneill Wood', 'Rosalind Edwards', 'Hoover Acevedo',
                                  'Alexander Valencia','Carr Bender', 'Mcknight Everett','Anastasia Alston',
                                  'Ashley Stark'])

    def test_MutualFriends(self):
            result = MutualFriends.get(self, 'Duncan Michael, Trisha Molina')
            self.assertEqual(result, [{'Name': 'Duncan Michael', 'Age': 29, 'Address': '790 Perry Terrace, Downsville,'
                                    ' Maine, 5869', 'Phone': '+1 (920) 423-2980'}, {'Name': 'Trisha Molina', 'Age': 24,
                                    'Address': '497 Holt Court, Connerton, Hawaii, 2162', 'Phone': '+1 (915) 412-2760'},
                                    {'Mutual friend': '---', 'index': 1, 'name': 'Decker Mckenzie', 'age': 60,
                                     'eyeColor': 'brown', 'has_died': False, 'address': '492 Stockton Street, Lawrence,'
                                    ' Guam, 4854', 'phone': '+1 (893) 587-3311'}, {'Mutual friend': '---', 'index': 4,
                                    'name': 'Mindy Beasley', 'age': 62, 'eyeColor': 'brown', 'has_died': False,
                                    'address': '628 Brevoort Place, Bellamy, Kansas, 2696',
                                    'phone': '+1 (862) 503-2197'}])

    def test_Likes(self):
        result = Likes.get(self, 'Lena Lucas')
        self.assertEqual(result, {'username': 'Lena Lucas', 'age': 29, 'fruits': ['banana', 'orange'],
                                  'vegetables': ['beetroot', 'celery']})


if __name__ == '__main__':
    unittest.main()


