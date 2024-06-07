SELECT s.name AS student_name, g.grade
FROM students s
JOIN groups gr ON s.group_id = gr.id
JOIN grades g ON s.id = g.student_id
WHERE gr.name = :group_name AND g.subject_id = :subject_id;
