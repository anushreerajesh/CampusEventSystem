DESIGN DOCUMENT 
1. Assumptions & Decisions
->Every event will have a unique ID so it can be identified easily.
->One database will handle all colleges, and each event will be linked with its college.
->A student cannot register twice for the same event.
->Attendance will be marked once for each student in an event.
->Feedback it will be stored as a rating (1–5) with a comment.

2. Data to Track
Events → event title, type (workshop/fest/etc.), date & time, created by admin.
Students → student ID, name, email, and college.
Registrations → which student registered for which event.
Attendance → which student attended an event.
Feedback → student’s rating and optional comment.

3. Database Schema (ER Diagram in Words)
->A College has many Students and many Events.
->A Student can register for many Events (through Registrations).
->Attendance links a student and an event with present/absent.
->Feedback links a student and an event with rating and comments.

4. API Design
POST /api/events → Create a new event.
POST /api/students → Add a new student.
POST /api/register → Register a student for an event.
POST /api/attendance → Mark student’s attendance.
POST /api/feedback → Submit feedback for an event.
GET /api/reports/registrations → See registrations for each event.
GET /api/reports/attendance → See attendance percentage for each event.
GET /api/reports/feedback → Get average feedback for each event.
GET /api/reports/student_participation → List all events a student attended.
GET /api/reports/top_active_students → Show top 3 active students.

5. Workflows
Registration-->Student fills registration → API stores in database → confirmation sent.
Attendance-->On event day → student checks in → marked in attendance table.
Feedback-->After event → student submits rating → stored in feedback table.
Reports-->Admin requests report → API collects data → shows event stats.

6. Edge Cases
If a student tries to register twice, the system blocks it.
If an event is canceled, attendance will not be marked.
If feedback is missing, the system will still generate reports with available data.
If a registered student does not attend, they will be marked absent.