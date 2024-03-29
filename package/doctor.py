from flask_restful import Resource, Api, request
from package.model import conn
class Doctors(Resource):
    """This contain apis to carry out activity with all doctors"""

    def get(self):
        """Retrive list of all the doctor"""

        doctors = conn.execute("SELECT * FROM doctor ORDER BY doc_date DESC").fetchall()
        return doctors



    def post(self):
        """Add the new doctor"""

        doctorInput = request.get_json(force=True)
        doc_first_name=doctorInput['doc_first_name']
        doc_last_name = doctorInput['doc_last_name']
        doc_ph_no = doctorInput['doc_ph_no']
        doc_address = doctorInput['doc_address']
        doctorInput['doc_id']=conn.execute('''INSERT INTO doctor(doc_first_name,doc_last_name,doc_ph_no,doc_address)
            VALUES(?,?,?,?)''', (doc_first_name, doc_last_name,doc_ph_no,doc_address)).lastrowid
        conn.commit()
        return doctorInput

class Doctor(Resource):
    """This includes all the APIs carrying out the activity with a single doctor"""

    def get(self, id):
        """Get the details of the doctor by the doctor id"""

        doctor = conn.execute("SELECT * FROM doctor WHERE doc_id=?", (id,)).fetchall()
        return doctor

    def delete(self, id):
        """Delete the doctor by its id"""

        conn.execute("DELETE FROM doctor WHERE doc_id=?", (id,))
        conn.commit()
        return {'msg': 'Successfully deleted'}

    def put(self, id):
        """Update the doctor by its id"""

        doctor_input = request.get_json(force=True)
        doc_first_name = doctor_input['doc_first_name']
        doc_last_name = doctor_input['doc_last_name']
        doc_ph_no = doctor_input['doc_ph_no']
        doc_address = doctor_input['doc_address']
        conn.execute(
            "UPDATE doctor SET doc_first_name=?,doc_last_name=?,doc_ph_no=?,doc_address=? WHERE doc_id=?",
            (doc_first_name, doc_last_name, doc_ph_no, doc_address, id))
        conn.commit()
        return doctor_input


class DoctorAssignPatients(Resource):
    """Assign patients to a doctor"""

    def patch(self, doc_id, patient_id):
        """Assign a patient to a doctor"""

        # Check if doctor exists
        doctor_exists = conn.execute("SELECT doc_id FROM doctor WHERE doc_id=?", (doc_id,)).fetchone()
        if not doctor_exists:
            return {'message': 'Doctor not found'}, 404

        # Check if patient exists
        patient_exists = conn.execute("SELECT pat_id FROM patient WHERE pat_id=?", (patient_id,)).fetchone()
        if not patient_exists:
            return {'message': 'Patient not found'}, 404

        # Fetch currently assigned patients for the doctor
        assigned_patients_record = conn.execute("SELECT patients_assigned FROM doctor WHERE doc_id=?", (doc_id,)).fetchone()
        if assigned_patients_record:
            assigned_patients = assigned_patients_record['patients_assigned']
            assigned_patients_list = assigned_patients.split(',')
            if str(patient_id) in assigned_patients_list:
                return {'message': 'Patient already assigned to this doctor'}, 400

        else:
            # If no patients are assigned yet, initialize the list with the new patient
            assigned_patients_updated = str(patient_id)

        # Update doctor's assigned patients
        conn.execute("UPDATE doctor SET patients_assigned=? WHERE doc_id=?", (assigned_patients_updated, doc_id))
        conn.commit()
        return {'message': 'Patient assigned successfully'}


class DoctorDeletePatients(Resource):
    """Delete assigned patients from a doctor"""

    def patch(self, doc_id, patient_id):
        """Delete a patient from a doctor"""

        # Check if doctor exists
        doctor_exists = conn.execute("SELECT doc_id FROM doctor WHERE doc_id=?", (doc_id,)).fetchone()
        if not doctor_exists:
            return {'message': 'Doctor not found'}, 404

        # Check if patient exists in the list of assigned patients
        assigned_patients_record = conn.execute("SELECT patients_assigned FROM doctor WHERE doc_id=?", (doc_id,)).fetchone()
        
        # Check if assigned_patients_record is not empty
        if not assigned_patients_record or not assigned_patients_record['patients_assigned']:
            return {'message': 'No patients assigned to this doctor'}, 404

        assigned_patients = assigned_patients_record['patients_assigned']
        assigned_patients_list = list(map(int, assigned_patients.split(',')))

        # Check if patient_id exists in assigned_patients_list
        if patient_id in assigned_patients_list:
            assigned_patients_list.remove(patient_id)
            assigned_patients_updated = ','.join(map(str, assigned_patients_list))
            conn.execute("UPDATE doctor SET patients_assigned=? WHERE doc_id=?", (assigned_patients_updated, doc_id))
            conn.commit()
            return {'message': 'Patient deleted successfully'}
        else:
            return {'message': 'Patient not assigned to this doctor'}, 404




        

class AvailableDoctors(Resource):
    """This contains API to return doctors as available if no patients are assigned"""

    def get(self):
        """Retrieve list of available doctors"""

        available_doctors = conn.execute("SELECT * FROM doctor WHERE patients_assigned=''").fetchall()
        if not available_doctors:
            return {'message': 'No available doctors'}
        else:
            return available_doctors
        
class AssignedPatients(Resource):
    """Retrieve list of patients assigned to a doctor"""

    def get(self, doc_id):
        """Retrieve list of patients assigned to the specified doctor"""

        # Check if doctor exists
        doctor_exists = conn.execute("SELECT doc_id FROM doctor WHERE doc_id=?", (doc_id,)).fetchone()
        if not doctor_exists:
            return {'message': 'Doctor not found'}, 404

        # Retrieve list of patients assigned to the doctor
        assigned_patients_record = conn.execute("SELECT patients_assigned FROM doctor WHERE doc_id=?", (doc_id,)).fetchone()
        if not assigned_patients_record or not assigned_patients_record['patients_assigned']:
            return {'message': 'No patients assigned to this doctor'}, 404

        assigned_patients = assigned_patients_record['patients_assigned']
        assigned_patients_list = assigned_patients.split(',')

        return {'assigned_patients': assigned_patients_list}
