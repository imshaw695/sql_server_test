-- This report can be used in the report builder as a plain text query

SELECT s.student_name, sts.test_subject, sts.test_score, sch.school_name
FROM students s
JOIN student_test_scores sts ON s.student_id = sts.student_id
JOIN schools sch ON s.school_id = sch.school_id
WHERE sts.test_score < 50;