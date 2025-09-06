-- 📊 Event Popularity Report (sorted by registrations)
SELECT e.title, COUNT(r.id) AS total_registrations
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
GROUP BY e.id
ORDER BY total_registrations DESC;

-- 📊 Attendance Percentage per Event
SELECT e.title,
       ROUND((CAST(COUNT(a.id) AS FLOAT) / COUNT(r.id)) * 100, 2) AS attendance_percentage
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
LEFT JOIN attendance a ON e.id = a.event_id AND r.student_id = a.student_id AND a.status = 'present'
GROUP BY e.id;

-- 📊 Average Feedback Score per Event
SELECT e.title, ROUND(AVG(f.rating), 2) AS avg_feedback
FROM events e
LEFT JOIN feedback f ON e.id = f.event_id
GROUP BY e.id;

-- 📊 Student Participation Report (how many events a student attended)
SELECT s.name, COUNT(a.id) AS events_attended
FROM students s
LEFT JOIN attendance a ON s.id = a.student_id AND a.status = 'present'
GROUP BY s.id
ORDER BY events_attended DESC;

-- ⭐ Top 3 Most Active Students
SELECT s.name, COUNT(a.id) AS events_attended
FROM students s
JOIN attendance a ON s.id = a.student_id AND a.status = 'present'
GROUP BY s.id
ORDER BY events_attended DESC
LIMIT 3;

-- 🔍 Flexible Report: Filter by Event Type (example: Workshop)
SELECT e.title, e.event_type, COUNT(r.id) AS registrations
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
WHERE e.event_type = 'Workshop'
GROUP BY e.id;
