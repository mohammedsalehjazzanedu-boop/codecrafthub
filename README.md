# CodeCraftHub
Simple Flask REST API to track learning courses. Data is saved in courses.json.

## Install and run
pip install -r requirements.txt
python3 app.py

## Endpoints
- POST /api/courses - add a course
- GET /api/courses - get all courses
- GET /api/courses/<id> - get one course
- PUT /api/courses/<id> - update a course
- DELETE /api/courses/<id> - delete a course
- GET /api/courses/stats - count of courses by status

Status must be: Not Started, In Progress, Completed. Date format: YYYY-MM-DD.
