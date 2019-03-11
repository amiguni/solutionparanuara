from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)


class MyExceptions(Exception):
    pass


class RecordNotFoundError(MyExceptions):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class CompanyNotFoundError(MyExceptions):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class EmployeeNotFoundError(MyExceptions):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


# end_point 01
class Welcome(Resource):
    def get(self):
        return {'From': 'Paranuara',
                'Message': 'Welcome to class-m planet..',
                'End_Point_01': '/all_employees/<string:company_name>',
                'End_Point_02': '/mutual_friends/<name1,name2>',
                'End_Point_03': '/likes/<string:employee_name>'
        }


# end_point 02
class AllEmployees(Resource):
    @staticmethod
    def search_all_employees(company_name):
        try:
            comp_idx = None
            col_employees = []

            # find company index value
            with open('companies.json', 'r') as data_comp:
                dt_c = data_comp.read()
            companies = json.loads(dt_c)
            for company in companies:
                if company_name == company['company']:
                    comp_idx = company['index']
                    break
            if comp_idx is None:
                raise CompanyNotFoundError('Error_345:', "Company doesn\'t exists.")

            # find people working in that company
            with open('people.json', 'r') as data_ppl:
                dt_p = data_ppl.read()
            people = json.loads(dt_p)
            col_employees.append(company_name + ' Employees:')
            for each in people:
                if each['company_id'] == comp_idx:
                    col_employees.append(each['name'])
            if len(col_employees) > 0:
                return col_employees
            else:
                raise EmployeeNotFoundError('Error_785:', 'This company doesn\'t have any employees.')

        except FileNotFoundError:
            return 'File not found'
        except CompanyNotFoundError as e1:
            return e1.expression + '  ' + e1.message
        except EmployeeNotFoundError as e2:
            return e2.expression + '  ' + e2.message

    def get(self, comp_name):
        try:
            employees = AllEmployees.search_all_employees(comp_name)
            if employees is None:
                raise CompanyNotFoundError('Error465:', 'Company doesn\'t exist')
            else:
                return employees
        except CompanyNotFoundError as e:
            return e.expression + ' ' + e.message


# end_point 03
class MutualFriends(Resource):
    @staticmethod
    def search_alive_brown(eye_c, died):
        ab_data = []  # alive brown storage
        try:
            with open('people.json', 'r') as ppl:
                dt = ppl.read()
            data = json.loads(dt)
            for rec in data:
                if rec['eyeColor'] == eye_c and rec['has_died'] == died:
                    ab_data.append(rec)
            return ab_data
        except FileNotFoundError:
            return 'People file is not found'

    @staticmethod
    def detail_lookup(comm_idx, data, peoples):
        output = []
        for e in peoples:
            people = {}
            people.update({'Name': e['name']})
            people.update({'Age': e['age']})
            people.update({'Address': e['address']})
            people.update({'Phone': e['phone']})
            output.append(people)

        for i in comm_idx:
            for each_person in data:
                if i == each_person['index']:
                    rs = {}
                    rs.update({'Mutual friend': '---'})
                    rs.update({'index': each_person['index']})
                    rs.update({'name': each_person['name']})
                    rs.update({'age': each_person['age']})
                    rs.update({'eyeColor': each_person['eyeColor']})
                    rs.update({'has_died': each_person['has_died']})
                    rs.update({'address': each_person['address']})
                    rs.update({'phone': each_person['phone']})
                    output.append(rs)
        return output

    def get(self, names):
        eye_color = 'brown'
        has_died = False
        _lst_a = []  # friend list a
        _lst_b = []  # friend list b
        _col_persons = []  # persons to be searched

        try:
            # get required data
            data_ab = list(MutualFriends.search_alive_brown(eye_color, has_died))
            # find their [names] friend lists
            nms = [e.strip() for e in names.split(',')]
            for person in data_ab:
                if person['name'] == nms[0] or person['name'] == nms[1]:
                    _col_persons.append(person)
                    if len(_col_persons) == 2:
                        break
            if len(_col_persons) == 2:
                for p1 in _col_persons[0]['friends']:
                    _lst_a.append(p1['index'])
                for p2 in _col_persons[1]['friends']:
                    _lst_b.append(p2['index'])
                # find mutual/common friends from both lists
                a_set = set(_lst_a)
                b_set = set(_lst_b)
                if a_set & b_set:
                    common_idx_values = a_set & b_set
                    res = MutualFriends.detail_lookup(common_idx_values, data_ab, _col_persons)
                    return res
            else:
                raise EmployeeNotFoundError('Error505:', 'Record(s) not found.')

        except IndexError:
                return 'Error885: Please provide names for 2 people to get mutual friends list.'
        except EmployeeNotFoundError as e:
                return e.expression + ' ' + e.message


# end_point 04
class Likes(Resource):
    def get(self, name ):
        fruits = ['apple', 'banana', 'orange', 'strawberry']
        veges = ['beetroot', 'cucumber', 'carrot', 'celery']
        with open('people.json', 'r') as data_ppl:
            dt_p = data_ppl.read()
        people = json.loads(dt_p)
        for each in people:
            if each['name'] == name:
                result = {}
                ff = list(set(fruits) & set(each['favouriteFood']))
                fv = list(set(veges) & set(each['favouriteFood']))
                result.update({'username': each['name']})
                result.update({'age': each['age']})
                result.update({'fruits': sorted(ff)})
                result.update({'vegetables': sorted(fv)})
                return result


api.add_resource(Welcome, '/')
api.add_resource(AllEmployees, '/all_employees/<string:comp_name>')
api.add_resource(MutualFriends, '/mutual_friends/<string:names>')
api.add_resource(Likes, '/likes/<string:name>')


if __name__ == '__main__':
    app.run(debug=True)


