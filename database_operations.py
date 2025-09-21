"""
Database Operations Module
Hostel Management System - Data Access Layer
"""

from database_config import get_database
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class StudentOperations:
    """Operations related to student management"""
    
    @staticmethod
    def add_student(student_data):
        """Add a new student to the database"""
        db = get_database()
        
        # First, get the room_id for the given room number and gender
        room_query = """
        SELECT room_id FROM rooms 
        WHERE room_number = %s AND gender = %s
        """
        room_result = db.execute_query(room_query, (student_data['room_number'], student_data['gender']), fetch=True)
        
        if not room_result:
            return False, "Room not found"
        
        room_id = room_result[0]['room_id']
        
        # Insert student
        student_query = """
        INSERT INTO students (student_id, first_name, last_name, father_name, mother_name, 
                            date_of_birth, email, address, vehicle_number, workplace_college, 
                            gender, room_id, bed_number, registration_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        student_params = (
            student_data['contact'],
            student_data['first_name'],
            student_data['last_name'],
            student_data['father_name'],
            student_data['mother_name'],
            student_data['dob'],
            student_data['email'],
            student_data['address'],
            student_data['vehicle'],
            student_data['workplace'],
            student_data['gender'],
            room_id,
            student_data['bed_number'],
            student_data['registration_date']
        )
        
        if db.execute_query(student_query, student_params):
            # Update room bed allocation
            bed_column = f"bed{student_data['bed_number'][-1]}_occupied"
            bed_student_column = f"bed{student_data['bed_number'][-1]}_student_id"
            bed_date_column = f"bed{student_data['bed_number'][-1]}_allocated_date"
            
            update_room_query = f"""
            UPDATE rooms 
            SET {bed_column} = TRUE, 
                {bed_student_column} = %s, 
                {bed_date_column} = %s
            WHERE room_id = %s
            """
            
            db.execute_query(update_room_query, (
                student_data['contact'],
                student_data['registration_date'],
                room_id
            ))
            
            return True, "Student added successfully"
        else:
            return False, "Failed to add student"
    
    @staticmethod
    def get_all_students():
        """Get all students with room information"""
        db = get_database()
        query = """
        SELECT s.*, r.room_number 
        FROM students s 
        LEFT JOIN rooms r ON s.room_id = r.room_id
        ORDER BY s.registration_date DESC
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_students_by_room(room_number):
        """Get students by room number"""
        db = get_database()
        query = """
        SELECT s.*, r.room_number 
        FROM students s 
        LEFT JOIN rooms r ON s.room_id = r.room_id
        WHERE r.room_number = %s
        ORDER BY s.bed_number
        """
        return db.execute_query(query, (room_number,), fetch=True)
    
    @staticmethod
    def search_student_by_name(name):
        """Search student by name"""
        db = get_database()
        query = """
        SELECT s.*, r.room_number 
        FROM students s 
        LEFT JOIN rooms r ON s.room_id = r.room_id
        WHERE CONCAT(s.first_name, ' ', s.last_name) LIKE %s
        """
        return db.execute_query(query, (f"%{name}%",), fetch=True)

class RoomOperations:
    """Operations related to room management"""
    
    @staticmethod
    def add_room(room_number, gender):
        """Add a new room"""
        db = get_database()
        query = """
        INSERT INTO rooms (room_number, gender)
        VALUES (%s, %s)
        """
        return db.execute_query(query, (room_number, gender))
    
    @staticmethod
    def get_available_rooms(gender):
        """Get available rooms for a specific gender"""
        db = get_database()
        query = """
        SELECT room_id, room_number, 
               bed1_occupied, bed2_occupied, bed3_occupied,
               bed1_student_id, bed2_student_id, bed3_student_id
        FROM rooms 
        WHERE gender = %s
        ORDER BY room_number
        """
        return db.execute_query(query, (gender,), fetch=True)
    
    @staticmethod
    def get_room_availability(room_id):
        """Get room availability details"""
        db = get_database()
        query = """
        SELECT * FROM rooms WHERE room_id = %s
        """
        result = db.execute_query(query, (room_id,), fetch=True)
        return result[0] if result else None

class InOutTimeOperations:
    """Operations related to in/out time logging"""
    
    @staticmethod
    def log_out_time(student_id, purpose):
        """Log student out time"""
        db = get_database()
        query = """
        INSERT INTO inouttime (student_id, purpose, out_time)
        VALUES (%s, %s, %s)
        """
        return db.execute_query(query, (student_id, purpose, datetime.now()))
    
    @staticmethod
    def log_in_time(student_id, remark):
        """Log student in time and update remark"""
        db = get_database()
        query = """
        UPDATE inouttime 
        SET in_time = %s, remark = %s
        WHERE student_id = %s AND in_time IS NULL
        ORDER BY out_time DESC
        LIMIT 1
        """
        return db.execute_query(query, (datetime.now(), remark, student_id))
    
    @staticmethod
    def get_out_time_entry(student_id):
        """Get the latest out time entry for a student"""
        db = get_database()
        query = """
        SELECT * FROM inouttime 
        WHERE student_id = %s AND in_time IS NULL
        ORDER BY out_time DESC
        LIMIT 1
        """
        result = db.execute_query(query, (student_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def get_all_time_logs():
        """Get all time logs"""
        db = get_database()
        query = """
        SELECT i.*, s.first_name, s.last_name, r.room_number
        FROM inouttime i
        LEFT JOIN students s ON i.student_id = s.student_id
        LEFT JOIN rooms r ON s.room_id = r.room_id
        ORDER BY i.out_time DESC
        """
        return db.execute_query(query, fetch=True)

class VisitorOperations:
    """Operations related to visitor management"""
    
    @staticmethod
    def add_visitor(visitor_data):
        """Add visitor information"""
        db = get_database()
        query = """
        INSERT INTO visitors (student_id, visitor_name, visitor_contact, 
                            reason, visitor_address, visit_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            visitor_data['student_id'],
            visitor_data['visitor_name'],
            visitor_data['visitor_contact'],
            visitor_data['reason'],
            visitor_data['visitor_address'],
            visitor_data['visit_date']
        )
        return db.execute_query(query, params)
    
    @staticmethod
    def get_visitors_by_student(student_id):
        """Get visitors for a specific student"""
        db = get_database()
        query = """
        SELECT v.*, s.first_name, s.last_name, r.room_number
        FROM visitors v
        LEFT JOIN students s ON v.student_id = s.student_id
        LEFT JOIN rooms r ON s.room_id = r.room_id
        WHERE v.student_id = %s
        ORDER BY v.visit_date DESC
        """
        return db.execute_query(query, (student_id,), fetch=True)
    
    @staticmethod
    def get_all_visitors():
        """Get all visitors"""
        db = get_database()
        query = """
        SELECT v.*, s.first_name, s.last_name, r.room_number
        FROM visitors v
        LEFT JOIN students s ON v.student_id = s.student_id
        LEFT JOIN rooms r ON s.room_id = r.room_id
        ORDER BY v.visit_date DESC
        """
        return db.execute_query(query, fetch=True)

class LeaveApplicationOperations:
    """Operations related to leave applications"""
    
    @staticmethod
    def submit_leave_application(application_data):
        """Submit a leave application"""
        db = get_database()
        query = """
        INSERT INTO leave_applications (student_id, student_name, room_number, 
                                      mobile_number, reason, application_date, return_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            application_data['student_id'],
            application_data['student_name'],
            application_data['room_number'],
            application_data['mobile_number'],
            application_data['reason'],
            application_data['application_date'],
            application_data['return_date']
        )
        return db.execute_query(query, params)
    
    @staticmethod
    def get_leave_applications():
        """Get all leave applications"""
        db = get_database()
        query = """
        SELECT * FROM leave_applications
        ORDER BY application_date DESC
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def update_leave_status(application_id, status):
        """Update leave application status"""
        db = get_database()
        query = """
        UPDATE leave_applications 
        SET status = %s, updated_at = %s
        WHERE application_id = %s
        """
        return db.execute_query(query, (status, datetime.now(), application_id))

class AdminOperations:
    """Operations related to admin authentication"""
    
    @staticmethod
    def verify_login(username, password):
        """Verify admin login credentials"""
        db = get_database()
        query = """
        SELECT password_hash FROM admin_users WHERE username = %s
        """
        result = db.execute_query(query, (username,), fetch=True)
        
        if result:
            # For now, using simple password comparison
            # In production, use proper password hashing
            return password == "12345670"  # Current hardcoded password
        return False

