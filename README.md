# Take Home Assignment

Below are some sample curl commands that demonstrate how to interact with the API endpoints defined in the provided Flask application (Witten in mind with Windows cmd prompt):

APPOINTMENTS

Retrieve all appointments

curl -X GET http://localhost:5000/appointment
Create a new appointment

curl -X POST ^
  http://127.0.0.1:5000/appointment ^
  -H "Content-Type: application/json" ^
  -d "{\"pat_id\": \"2\",\"doc_id\": \"2\",\"appointment_date\": \"2024-04-01\"}"

Retrieve a single appointment by ID

curl -X GET http://localhost:5000/appointment/2
Delete an appointment by ID

curl -X DELETE http://localhost:5000/appointment/2
Update an appointment by ID

curl -X PUT ^  http://127.0.0.1:5000/appointment/7 ^  -H "Content-Type: application/json" ^  -d "{\"pat_id\": \"2\",\"doc_id\": \"4\"}"

DEPARTMENTS

For Departments Resource:
GET /department - Retrieve all departments


curl -X GET http://127.0.0.1:5000/department POST /department - Add a new department


curl -X POST \
  http://127.0.0.1:5000/department \
  -H 'Content-Type: application/json' \
  -d '{
    "department_id": 1,
    "name": "Department Name",
    "head_id": 1,
    "doctors": [1, 2, 3]  // Optional
  }'


GET /department/{department_id} - Retrieve details of a department by ID


curl -X GET http://127.0.0.1:5000/department/1
PUT /department/{department_id} - Update details of a department by ID


curl -X PUT \
  http://127.0.0.1:5000/department/1 \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "New Department Name",
    "head_id": 2
  }'


GET /department/{department_id}/doctors - Retrieve doctors assigned to a department


curl -X GET http://127.0.0.1:5000/department/1/doctors
POST /department/{department_id}/doctors - Assign or reassign doctors to a department


curl -X POST \
  http://127.0.0.1:5000/department/1/doctors \
  -H 'Content-Type: application/json' \
  -d '{
    "doctors": [4, 5, 6]
  }'



