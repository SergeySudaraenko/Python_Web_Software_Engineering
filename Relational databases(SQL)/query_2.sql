SELECT s.name, AVG(g.grade) AS avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.subject_id = :subject_id
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 1;
