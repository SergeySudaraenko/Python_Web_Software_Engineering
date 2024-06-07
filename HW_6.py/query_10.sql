SELECT s.name AS subject_name
FROM subjects s
JOIN grades g ON s.id = g.subject_id
JOIN students st ON g.student_id = st.id
JOIN teachers t ON s.teacher_id = t.id
WHERE st.name = :student_name AND t.name = :teacher_name;
