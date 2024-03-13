-- Drop tables if they exist, in reverse order due to dependencies
DROP TABLE IF EXISTS student_test_scores;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS schools;

-- Create the schools table
CREATE TABLE schools (
    school_id INT PRIMARY KEY,
    school_name VARCHAR(255) NOT NULL,
    school_address VARCHAR(255),
    school_city VARCHAR(100),
    school_state VARCHAR(50),
    school_zip VARCHAR(10)
);

-- Create the students table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    school_id INT,
    FOREIGN KEY (school_id) REFERENCES schools(school_id) ON DELETE SET NULL
);

-- Create the student_test_scores table
CREATE TABLE student_test_scores (
    test_id INT PRIMARY KEY,
    student_id INT,
    test_date DATE,
    test_subject VARCHAR(50),
    test_score DECIMAL(5,2),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);
