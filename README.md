# Take Home Assignment
Run with python app.py, install deps like Flask, pysqilte and the rest

Below are some sample curl commands that demonstrate how to interact with the API endpoints defined in the provided Flask application 
# (Witten in mind with Windows cmd prompt)

# API Usage Guide

## APPOINTMENTS

### Retrieve all appointments
curl -X GET http://localhost:5000/appointment

### Create a new appointment
curl -X POST ^
  http://127.0.0.1:5000/appointment ^
  -H "Content-Type: application/json" ^
  -d "{\"pat_id\": \"2\",\"doc_id\": \"2\",\"appointment_date\": \"2024-04-01\"}"

### Retrieve a single appointment by ID
curl -X GET http://localhost:5000/appointment/2

### Delete an appointment by ID
curl -X DELETE http://localhost:5000/appointment/2

### Update an appointment by ID
curl -X PUT ^  
  http://127.0.0.1:5000/appointment/7 ^  
  -H "Content-Type: application/json" ^  
  -d "{\"pat_id\": \"2\",\"doc_id\": \"4\"}"

## DEPARTMENTS

### Retrieve all departments
curl -X GET http://127.0.0.1:5000/department

### Add a new department
curl -X POST ^
  http://127.0.0.1:5000/department ^
  -H "Content-Type: application/json" ^
  -d "{\"department_id\":1,\"name\":\"Department Name\",\"head_id\":1,\"doctors\":[1,2,3]}"

### Retrieve details of a department by ID
curl -X GET http://127.0.0.1:5000/department/1

### Update details of a department by ID
curl -X PUT ^
  http://127.0.0.1:5000/department/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"New Department Name\",\"head_id\":2}"

### Retrieve doctors assigned to a department
curl -X GET http://127.0.0.1:5000/department/1/doctors

### Assign or reassign doctors to a department
curl -X POST ^
  http://127.0.0.1:5000/department/1/doctors ^
  -H "Content-Type: application/json" ^
  -d "{\"doctors\":[4,5,6]}"

## DOCTORS

### Retrieve all doctors
curl -X GET http://127.0.0.1:5000/doctor

### Add a new doctor
curl -X POST ^
  http://127.0.0.1:5000/doctor ^
  -H "Content-Type: application/json" ^
  -d "{\"doc_first_name\":\"John\",\"doc_last_name\":\"Doe\",\"doc_ph_no\":\"1234567890\",\"doc_address\":\"123 Main St\"}"

### Retrieve details of a doctor by ID
curl -X GET http://127.0.0.1:5000/doctor/1

### Update details of a doctor by ID
curl -X PUT ^
  http://127.0.0.1:5000/doctor/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"doc_first_name\":\"Jane\",\"doc_last_name\":\"Smith\",\"doc_ph_no\":\"9876543210\",\"doc_address\":\"456 Elm St\",\"patients_assigned\":\"1,2,3\"}"

### Assign a patient to a doctor
curl -X PATCH ^
  http://127.0.0.1:5000/doctor/1/patients/assign/1

### Delete a patient from a doctor
curl -X PATCH ^
  http://127.0.0.1:5000/doctor/1/patients/delete/1

### Retrieve list of available doctors
curl -X GET http://127.0.0.1:5000/doctor/availability

### Retrieve list of patients assigned to a doctor
curl -X GET http://127.0.0.1:5000/doctor/1/patients

## PATIENTS

### Retrieve list of all patients
curl -X GET http://127.0.0.1:5000/patient

### Add a new patient
curl -X POST ^
  http://127.0.0.1:5000/patient ^
  -H "Content-Type: application/json" ^
  -d "{\"pat_first_name\":\"John\",\"pat_last_name\":\"Doe\",\"pat_insurance_no\":\"1234567890\",\"pat_ph_no\":\"9876543210\",\"pat_address\":\"123 Main St\"}"

### Retrieve details of a patient by ID
curl -X GET http://127.0.0.1:5000/patient/1

### Delete a patient by ID
curl -X DELETE http://127.0.0.1:5000/patient/1

### Update details of a patient by ID
curl -X PUT ^
  http://127.0.0.1:5000/patient/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"pat_first_name\":\"Jane\",\"pat_last_name\":\"Smith\",\"pat_insurance_no\":\"0987654321\",\"pat_ph_no\":\"1234567890\",\"pat_address\":\"456 Elm St\"}"

### Add medical history
curl -X POST ^
  http://127.0.0.1:5000/patient/2 ^
  -H "Content-Type: application/json" ^
  -d "{\"medical_history\":\"High blood pressure\"}"

### Retrieve medical history of a patient by ID
curl -X GET http://127.0.0.1:5000/patient/1/history

### Retrieve appointments of a patient by ID
curl -X GET http://127.0.0.1:5000/patient/1/appointment

### Set appointments data
curl -X PATCH ^
  http://127.0.0.1:5000/patient/3 ^
  -H "Content-Type: application/json" ^
  -d "{\"appointment\":\"('Dr. White', '2024-04-02')\"}"

## SEARCH

### Search for Patients
curl -X GET "http://127.0.0.1:5000/search/patients?query=John"

### Search for Doctors
curl -X GET "http://127.0.0.1:5000/search/doctors?query=Smith"

### Search for Departments
curl -X GET "http://127.0.0.1:5000/search/departments?query=Cardiology"

## ASSIGNED PATIENTS LIST

### Retrieve assigned patients list for a doctor
curl -X GET "http://127.0.0.1:5000/doctor/1/patients"

There are more features as well, can reference app.py for the same
