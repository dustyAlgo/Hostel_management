-- Hostel Management System Database Schema
-- MySQL Database Design

-- Create database
CREATE DATABASE IF NOT EXISTS hostel_management;
USE hostel_management;

-- 1. Rooms Table
CREATE TABLE rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10) NOT NULL UNIQUE,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    bed1_occupied BOOLEAN DEFAULT FALSE,
    bed2_occupied BOOLEAN DEFAULT FALSE,
    bed3_occupied BOOLEAN DEFAULT FALSE,
    bed1_student_id VARCHAR(15) NULL,
    bed2_student_id VARCHAR(15) NULL,
    bed3_student_id VARCHAR(15) NULL,
    bed1_allocated_date DATETIME NULL,
    bed2_allocated_date DATETIME NULL,
    bed3_allocated_date DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Students Table
CREATE TABLE students (
    student_id VARCHAR(15) PRIMARY KEY, -- Contact number as ID
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    father_name VARCHAR(50) NOT NULL,
    mother_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    vehicle_number VARCHAR(20),
    workplace_college VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    room_id INT,
    bed_number VARCHAR(5), -- B1, B2, B3, G1, G2, G3, O1, O2, O3
    registration_date DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE SET NULL
);

-- 3. InOutTime Table
CREATE TABLE inouttime (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(15) NOT NULL,
    purpose VARCHAR(200) NOT NULL,
    out_time DATETIME NOT NULL,
    in_time DATETIME NULL,
    remark ENUM('Before Time', 'On Time', 'Late') NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- 4. Visitors Table
CREATE TABLE visitors (
    visitor_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(15) NOT NULL,
    visitor_name VARCHAR(100) NOT NULL,
    visitor_contact VARCHAR(15) NOT NULL,
    reason VARCHAR(200) NOT NULL,
    visitor_address TEXT NOT NULL,
    visit_date DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- 5. LeaveApplications Table
CREATE TABLE leave_applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(15) NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    room_number VARCHAR(10) NOT NULL,
    mobile_number VARCHAR(15) NOT NULL,
    reason TEXT NOT NULL,
    application_date DATETIME NOT NULL,
    return_date DATE NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- 6. Admin Users Table (for future authentication improvements)
CREATE TABLE admin_users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert default admin user (password: 12345670)
INSERT INTO admin_users (username, password_hash) VALUES 
('mrityunjay', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8QzQz2C');

-- Create indexes for better performance
CREATE INDEX idx_students_room_id ON students(room_id);
CREATE INDEX idx_students_gender ON students(gender);
CREATE INDEX idx_inouttime_student_id ON inouttime(student_id);
CREATE INDEX idx_inouttime_out_time ON inouttime(out_time);
CREATE INDEX idx_visitors_student_id ON visitors(student_id);
CREATE INDEX idx_leave_applications_student_id ON leave_applications(student_id);
CREATE INDEX idx_leave_applications_status ON leave_applications(status);

