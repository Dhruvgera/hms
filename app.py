from flask import Flask,send_from_directory,render_template
from flask import send_from_directory

from flask_restful import Resource, Api
from package.patient import Patients, Patient, PatientAppointments, PatientMedicalHistory
from package.doctor import AssignedPatients, AvailableDoctors, DoctorAssignPatients, DoctorDeletePatients, Doctors, Doctor
from package.appointment import Appointments, Appointment
from package.common import Common
from package.department import DepartmentDoctor, Departments, Department


import json
import os

from package.search import SearchDepartments, SearchDoctors, SearchPatients

with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')
api = Api(app)

api.add_resource(Patients, '/patient')
api.add_resource(Patient, '/patient/<int:id>')
api.add_resource(PatientAppointments, '/patient/<int:id>/appointment')
api.add_resource(PatientMedicalHistory, '/patient/<int:id>/history')
api.add_resource(Doctors, '/doctor')
api.add_resource(Doctor, '/doctor/<int:id>')
api.add_resource(DoctorAssignPatients, '/doctor/<int:doc_id>/patients/assign/<int:patient_id>')
api.add_resource(DoctorDeletePatients, '/doctor/<int:doc_id>/patients/delete/<int:patient_id>')
api.add_resource(Appointments, '/appointment')
api.add_resource(Appointment, '/appointment/<int:id>')
api.add_resource(AvailableDoctors, '/doctor/availability')
api.add_resource(Common, '/common')
api.add_resource(Departments, '/department')
api.add_resource(Department, '/department/<int:department_id>')
api.add_resource(DepartmentDoctor, '/department/<int:department_id>/doctors', '/department/<int:department_id>/doctors/search')
api.add_resource(AssignedPatients, '/doctor/<int:doc_id>/patients')
api.add_resource(SearchPatients, '/search/patients')
api.add_resource(SearchDoctors, '/search/doctors')
api.add_resource(SearchDepartments, '/search/departments')



if __name__ == '__main__':
    app.run(debug=True,host=config['host'],port=config['port'])