from flask import jsonify
from flask_restful import Resource, Api, request
from package.model import conn

from flask_restful import Resource, request
from package.model import conn

class SearchPatients(Resource):
    def get(self):
        search_query = request.args.get('query', '')  # Get search query parameter

        # Execute SQL query to search for patients with matching first names
        patients = conn.execute("SELECT * FROM patient WHERE pat_first_name LIKE ?", ('%' + search_query + '%',)).fetchall()

        return jsonify({'patients': patients})

class SearchDoctors(Resource):
    def get(self):
        search_query = request.args.get('query', '')  # Get search query parameter

        # Execute SQL query to search for doctors with matching first names
        doctors = conn.execute("SELECT * FROM doctor WHERE doc_first_name LIKE ?", ('%' + search_query + '%',)).fetchall()

        return jsonify({'doctors': doctors})

class SearchDepartments(Resource):
    def get(self):
        search_query = request.args.get('query', '')  # Get search query parameter

        # Execute SQL query to search for departments with matching names
        departments = conn.execute("SELECT * FROM department WHERE name LIKE ?", ('%' + search_query + '%',)).fetchall()

        return jsonify({'departments': departments})
