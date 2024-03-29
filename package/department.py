from flask_restful import Resource, Api, request
from package.model import conn

class Departments(Resource):
    """This contain APIs to carry out activity with all departments"""

    def get(self):
        """Retrieve all the departments and return in form of json"""

        departments = conn.execute("SELECT * FROM department").fetchall()
        departments_with_doctors = []
        for department in departments:
            department_id = department['department_id']
            doctors = conn.execute("SELECT * FROM doctor WHERE doc_id IN (SELECT doc_id FROM department_doctor WHERE department_id=?)", (department_id,)).fetchall()
            department['doctors'] = doctors
            departments_with_doctors.append(department)
        return departments_with_doctors

    def post(self):
        """API to add department in the database"""

        department_data = request.get_json(force=True)
        department_id = department_data['department_id']
        name = department_data['name']
        head_id = department_data['head_id']
        
        conn.execute("INSERT INTO department(department_id, name, head_id) VALUES(?,?,?)", (department_id, name, head_id))
        conn.commit()

        # Assign doctors to the department if specified
        doctors = department_data.get('doctors', [])
        if doctors:
            for doc_id in doctors:
                conn.execute("INSERT INTO department_doctor(department_id, doc_id) VALUES(?, ?)", (department_id, doc_id))
            conn.commit()

        return department_data


class Department(Resource):
    """This contains all APIs doing activity with single department"""

    def get(self, department_id):
        """Retrieve a single department details by its id"""

        department = conn.execute("SELECT * FROM department WHERE department_id=?", (department_id,)).fetchone()
        if department:
            doctors = conn.execute("SELECT * FROM doctor WHERE doc_id IN (SELECT doc_id FROM department_doctor WHERE department_id=?)", (department_id,)).fetchall()
            department['doctors'] = doctors
            return department
        else:
            return {'message': 'Department not found'}, 404

    def put(self, department_id):
        """Update the department details by the department id"""

        department_data = request.get_json(force=True)
        name = department_data['name']
        head_id = department_data['head_id']
        conn.execute("UPDATE department SET name=?, head_id=? WHERE department_id=?", (name, head_id, department_id))
        conn.commit()
        return department_data

class DepartmentDoctor(Resource):
    """This contains APIs to search, assign, or re-assign doctors to a department"""

    def get(self, department_id):
        """API to retrieve doctors assigned to a department"""

        doctors = conn.execute("SELECT * FROM doctor WHERE doc_id IN (SELECT doc_id FROM department_doctor WHERE department_id=?)", (department_id,)).fetchall()
        return doctors

    def post(self, department_id):
        """API to assign or reassign doctors to a department"""

        data = request.get_json(force=True)
        doctors = data.get('doctors', [])
        
        if not doctors:
            return {'message': 'No doctors specified'}, 400
        
        # Clear existing doctor assignments for the department
        conn.execute("DELETE FROM department_doctor WHERE department_id=?", (department_id,))
        
        # Assign new doctors to the department
        for doc_id in doctors:
            conn.execute("INSERT INTO department_doctor(department_id, doc_id) VALUES(?, ?)", (department_id, doc_id))
        conn.commit()
        return {'message': 'Doctors assigned successfully'}
