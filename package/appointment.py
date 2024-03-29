from flask_restful import Resource, Api, request
from package.model import conn



class Appointments(Resource):
    """This contain apis to carry out activity with all appiontments"""

    def get(self):
        """Retrive all the appointment and return in form of json"""

        appointment = conn.execute("SELECT p.*,d.*,a.* from appointment a LEFT JOIN patient p ON a.pat_id = p.pat_id LEFT JOIN doctor d ON a.doc_id = d.doc_id ORDER BY appointment_date DESC").fetchall()
        return appointment

    def post(self):
        """Create the appoitment by assiciating patient and docter with appointment date"""

        appointment = request.get_json(force=True)
        pat_id = appointment['pat_id']
        doc_id = appointment['doc_id']
        appointment_date = appointment['appointment_date']
        appointment['app_id'] = conn.execute('''INSERT INTO appointment(pat_id,doc_id,appointment_date)
            VALUES(?,?,?)''', (pat_id, doc_id,appointment_date)).lastrowid
        conn.commit()
        return appointment



class Appointment(Resource):
    """This contain all api doing activity with single appointment"""

    def get(self,id):
        """retrive a singe appointment details by its id"""

        appointment = conn.execute("SELECT * FROM appointment WHERE app_id=?",(id,)).fetchall()
        return appointment


    def delete(self,id):
        """Delete teh appointment by its id"""

        conn.execute("DELETE FROM appointment WHERE app_id=?",(id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):
        """Update the appointment details by the appointment id"""

        appointment = request.get_json(force=True)
        pat_id = appointment['pat_id']
        doc_id = appointment['doc_id']
        conn.execute("UPDATE appointment SET pat_id=?,doc_id=? WHERE app_id=?",
                     (pat_id, doc_id, id))
        conn.commit()
        return appointment
    


class DoctorAvailability(Resource):
    """This contains API to check doctor availability"""

    def get(self):
        """Check if any doctor has appointments and update availability"""

        all_doctors = conn.execute("SELECT doc_id FROM doctor").fetchall()
        print(all_doctors)
        available_doctors = []

        for doctor_id in all_doctors:
            appointments = conn.execute("SELECT * FROM appointment WHERE doc_id=?", doctor_id).fetchall()
            if not appointments:
                available_doctors.append(doctor_id[0])

        if available_doctors:
            return {'msg': 'Available doctors', 'available_doctors': available_doctors}
        else:
            return {'msg': 'All doctors have appointments'}



