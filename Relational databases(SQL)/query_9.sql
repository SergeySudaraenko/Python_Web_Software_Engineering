SELECT DISTINCT s.name AS subject_name
FROM subjects s
JOIN grades g ON s.id = g.subject_id
JOIN students st ON g.student_id = st.id
WHERE st.name = :student_name;
