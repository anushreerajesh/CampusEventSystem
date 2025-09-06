# Campus Event Management System

This is a small Flask + SQLite project I built for managing college events.  
It allows adding colleges, students, events, and keeping track of registrations, attendance, and feedback.


## Features

- Add students and link them to colleges
- Create events (seminars, workshops, etc.)
- Register students for events
- Mark attendance for events
- Collect feedback (rating + comment)
- Reports:
  - Registrations per event
  - Student participation
  - Top active students


## Tech Used

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Testing**: Postman for API requests

## To run
1. Clone or download the project folder.  
2. Install dependencies:
   ```bash
   pip install flask

## To run the server
python app.py

## Server 
Server will start at http://127.0.0.1:5000

## API Endpoints 
Some sample endpoints which can be tested on Postman 
1. Create Event (POST) http://127.0.0.1:5000/events
{
  "title": "AI Workshop",
  "event_type": "Seminar",
  "date": "2025-09-10",
  "college_id": 1
}
2. Get All Events (GET) http://127.0.0.1:5000/events
3. Add Students (POST) http://127.0.0.1:5000/students
{
  "name": "John Doe",
  "email": "john@example.com",
  "college_id": 1
}
4. Register Student (POST) http://127.0.0.1:5000/register
5. Mark Attendance (POST) http://127.0.0.1:5000/attendance
6. Submit Feedback (POST) http://127.0.0.1:5000/feedback
7. Reports
http://127.0.0.1:5000/reports/registrations
http://127.0.0.1:5000/reports/student_participation/<student_id>
http://127.0.0.1:5000/reports/top_active_students

## Screenshots
I’ve attached a few screenshots inside the Screenshots/ folder that show:
1. Creating an event
2. Adding a student
3. Registering a student
4. Attendance and feedback flow

## Future advancements
In the future this can be implemented on web applications and mobile applications as well!
