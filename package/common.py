from flask_restful import Resource, Api, request
from package.model import conn


class Common(Resource):
    """This contain common api ie noe related to the specific module"""

    def get(self):
        """Retrive the patient, doctor, appointment, medication count for the dashboard page"""

        getPatientCount=conn.execute("SELECT COUNT(*) AS patient FROM patient").fetchone()
        getDoctorCount = conn.execute("SELECT COUNT(*) AS doctor FROM doctor").fetchone()
        getAppointmentCount = conn.execute("SELECT COUNT(*) AS appointment FROM appointment").fetchone()
        getDepartmentCount = conn.execute("SELECT COUNT(*) AS department FROM department").fetchone()


        getPatientCount.update(getDoctorCount)
        getPatientCount.update(getAppointmentCount)
        getPatientCount.update(getDepartmentCount)


        return getPatientCount