from flask_restful import Resource, Api, request
from package.model import conn

class Patients(Resource):
    """It contain all the api carryign the activity with aand specific patient"""

    def get(self):
        """Api to retive all the patient from the database"""

        patients = conn.execute("SELECT * FROM patient  ORDER BY pat_date DESC").fetchall()
        return patients



    def post(self):
        """api to add the patient in the database"""

        patientInput = request.get_json(force=True)
        pat_first_name=patientInput['pat_first_name']
        pat_last_name = patientInput['pat_last_name']
        pat_insurance_no = patientInput['pat_insurance_no']
        pat_ph_no = patientInput['pat_ph_no']
        pat_address = patientInput['pat_address']
        patientInput['pat_id']=conn.execute('''INSERT INTO patient(pat_first_name,pat_last_name,pat_insurance_no,pat_ph_no,pat_address)
            VALUES(?,?,?,?,?)''', (pat_first_name, pat_last_name, pat_insurance_no,pat_ph_no,pat_address)).lastrowid
        conn.commit()
        return patientInput

class Patient(Resource):
    """It contains all apis doing activity with the single patient entity"""

    def get(self,id):
        """api to retrive details of the patient by it id"""

        patient = conn.execute("SELECT * FROM patient WHERE pat_id=?",(id,)).fetchall()
        return patient

    def delete(self,id):
        """api to delete the patiend by its id"""

        conn.execute("DELETE FROM patient WHERE pat_id=?",(id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):
        """api to update the patient by it id"""

        patientInput = request.get_json(force=True)
        pat_first_name = patientInput['pat_first_name']
        pat_last_name = patientInput['pat_last_name']
        pat_insurance_no = patientInput['pat_insurance_no']
        pat_ph_no = patientInput['pat_ph_no']
        pat_address = patientInput['pat_address']
        conn.execute("UPDATE patient SET pat_first_name=?,pat_last_name=?,pat_insurance_no=?,pat_ph_no=?,pat_address=? WHERE pat_id=?",
                     (pat_first_name, pat_last_name, pat_insurance_no,pat_ph_no,pat_address,id))
        conn.commit()
        return patientInput
    
    def post(self, id):
        """API to add medical history to a patient"""

        medical_history_input = request.get_json(force=True)
        medical_history = medical_history_input['medical_history']
        conn.execute("UPDATE patient SET medical_history=? WHERE pat_id=?", (medical_history, id))
        conn.commit()
        return {'msg': 'Medical history added successfully'}

    def patch(self, id):
        """API to add appointment to a patient"""

        appointment_input = request.get_json(force=True)
        appointment = appointment_input['appointment']
        
        # Fetch existing appointment record
        existing_record = conn.execute("SELECT appointment_record FROM patient WHERE pat_id=?", (id,)).fetchone()
        if existing_record:
            existing_appointments = existing_record['appointment_record']
            if existing_appointments:
                existing_appointments = eval(existing_appointments)
                existing_appointments.append(appointment)
            else:
                existing_appointments = [appointment]
        else:
            existing_appointments = [appointment]

        # Update patient's appointment record
        conn.execute("UPDATE patient SET appointment_record=? WHERE pat_id=?", (str(existing_appointments), id))
        conn.commit()
        return {'msg': 'Appointment added successfully'}
    
class PatientMedicalHistory(Resource):
    """API to handle medical history of a patient"""

    def get(self, id):
        """API to retrieve medical history of a patient by its id"""

        medical_history = conn.execute("SELECT medical_history FROM patient WHERE pat_id=?", (id,)).fetchone()
        return medical_history

class PatientAppointments(Resource):
    """API to handle appointments of a patient"""

    def get(self, id):
        """API to retrieve appointments of a patient by its id"""

        appointments = conn.execute("SELECT appointment_record FROM patient WHERE pat_id=?", (id,)).fetchone()
        return appointments
    
