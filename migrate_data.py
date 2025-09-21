"""
Data Migration Script
Migrates existing text file data to MySQL database
"""

import os
from datetime import datetime
from database_config import get_database
from database_operations import *
import logging

logger = logging.getLogger(__name__)

class DataMigrator:
    """Handles migration of text file data to database"""
    
    def __init__(self):
        self.db = get_database()
        self.migration_log = []
    
    def log_migration(self, message):
        """Log migration progress"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        self.migration_log.append(log_message)
        print(log_message)
    
    def migrate_rooms(self):
        """Migrate room data from text files"""
        self.log_migration("Starting room migration...")
        
        room_files = {
            'Male': 'room_info_boys.txt',
            'Female': 'room_info_girls.txt',
            'Other': 'room_info_others.txt'
        }
        
        for gender, filename in room_files.items():
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip empty lines and comments
                        parts = line.split(',')
                        if len(parts) >= 5:
                            room_number = parts[0]
                            if room_number and room_number != '--':
                                try:
                                    RoomOperations.add_room(room_number, gender)
                                    self.log_migration(f"Migrated room {room_number} for {gender}")
                                except Exception as e:
                                    self.log_migration(f"Error migrating room {room_number}: {e}")
            else:
                self.log_migration(f"File {filename} not found, skipping...")
    
    def migrate_students(self):
        """Migrate student data from text files"""
        self.log_migration("Starting student migration...")
        
        if not os.path.exists('student_info.txt'):
            self.log_migration("student_info.txt not found, skipping student migration")
            return
        
        with open('student_info.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split(',')
                if len(parts) >= 12:
                    try:
                        # Parse student data
                        student_data = {
                            'contact': parts[0],
                            'first_name': parts[1].split()[0] if parts[1] else '',
                            'last_name': ' '.join(parts[1].split()[1:]) if len(parts[1].split()) > 1 else '',
                            'father_name': parts[2],
                            'mother_name': parts[3],
                            'dob': parts[4],
                            'email': parts[5],
                            'workplace': parts[6],
                            'vehicle': parts[7],
                            'registration_date': parts[8] + ' ' + parts[9] if len(parts) > 9 else datetime.now(),
                            'bed_number': parts[10],
                            'room_number': parts[11],
                            'address': 'Not specified',  # Not in original data
                            'gender': 'Male'  # Default, will be updated based on room
                        }
                        
                        # Determine gender based on room file
                        gender = self.determine_gender_from_room(student_data['room_number'])
                        student_data['gender'] = gender
                        
                        # Add student
                        success, message = StudentOperations.add_student(student_data)
                        if success:
                            self.log_migration(f"Migrated student {student_data['first_name']} {student_data['last_name']}")
                        else:
                            self.log_migration(f"Error migrating student {student_data['first_name']}: {message}")
                            
                    except Exception as e:
                        self.log_migration(f"Error parsing student data: {e}")
    
    def determine_gender_from_room(self, room_number):
        """Determine gender based on which room file contains the room"""
        room_files = {
            'Male': 'room_info_boys.txt',
            'Female': 'room_info_girls.txt',
            'Other': 'room_info_others.txt'
        }
        
        for gender, filename in room_files.items():
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if room_number in content:
                        return gender
        
        return 'Male'  # Default fallback
    
    def migrate_inouttime(self):
        """Migrate in/out time data"""
        self.log_migration("Starting in/out time migration...")
        
        if not os.path.exists('inouttime.txt'):
            self.log_migration("inouttime.txt not found, skipping in/out time migration")
            return
        
        with open('inouttime.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split(',')
                if len(parts) >= 5:
                    try:
                        student_id = parts[0]
                        purpose = parts[1]
                        out_time_str = parts[2]
                        in_time_str = parts[3] if parts[3] != 'OUTTIME' else None
                        remark = parts[4] if parts[4] != 'REMARK' else None
                        
                        # Parse datetime
                        out_time = datetime.strptime(out_time_str, "%H:%M,%Y-%m-%d")
                        
                        if in_time_str and in_time_str != 'OUTTIME':
                            in_time = datetime.strptime(in_time_str, "%H:%M,%Y-%m-%d")
                        else:
                            in_time = None
                        
                        # Add to database
                        if in_time:
                            # Complete entry
                            InOutTimeOperations.log_out_time(student_id, purpose)
                            InOutTimeOperations.log_in_time(student_id, remark)
                        else:
                            # Out time only
                            InOutTimeOperations.log_out_time(student_id, purpose)
                        
                        self.log_migration(f"Migrated time log for student {student_id}")
                        
                    except Exception as e:
                        self.log_migration(f"Error parsing time log: {e}")
    
    def migrate_visitors(self):
        """Migrate visitor data"""
        self.log_migration("Starting visitor migration...")
        
        if not os.path.exists('visitor_info.txt'):
            self.log_migration("visitor_info.txt not found, skipping visitor migration")
            return
        
        with open('visitor_info.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split(',')
                if len(parts) >= 6:
                    try:
                        visitor_data = {
                            'student_id': self.find_student_id_by_name(parts[0]),
                            'visitor_name': parts[1],
                            'visitor_contact': parts[2],
                            'reason': parts[3],
                            'visitor_address': parts[4],
                            'visit_date': parts[5]
                        }
                        
                        if visitor_data['student_id']:
                            VisitorOperations.add_visitor(visitor_data)
                            self.log_migration(f"Migrated visitor {visitor_data['visitor_name']}")
                        else:
                            self.log_migration(f"Could not find student for visitor {visitor_data['visitor_name']}")
                            
                    except Exception as e:
                        self.log_migration(f"Error parsing visitor data: {e}")
    
    def find_student_id_by_name(self, student_name):
        """Find student ID by name"""
        students = StudentOperations.get_all_students()
        for student in students:
            full_name = f"{student['first_name']} {student['last_name']}".lower()
            if student_name.lower() in full_name:
                return student['student_id']
        return None
    
    def migrate_leave_applications(self):
        """Migrate leave application data"""
        self.log_migration("Starting leave application migration...")
        
        if not os.path.exists('leave_applications.txt'):
            self.log_migration("leave_applications.txt not found, skipping leave application migration")
            return
        
        with open('leave_applications.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split(',')
                if len(parts) >= 7:
                    try:
                        application_data = {
                            'student_id': parts[0],
                            'student_name': parts[1],
                            'room_number': parts[2],
                            'mobile_number': parts[3],
                            'reason': parts[4],
                            'application_date': parts[5],
                            'return_date': parts[6]
                        }
                        
                        LeaveApplicationOperations.submit_leave_application(application_data)
                        self.log_migration(f"Migrated leave application for {application_data['student_name']}")
                        
                    except Exception as e:
                        self.log_migration(f"Error parsing leave application: {e}")
    
    def run_migration(self):
        """Run complete migration process"""
        self.log_migration("Starting data migration process...")
        
        # Test database connection
        if not self.db.connect():
            self.log_migration("Failed to connect to database. Migration aborted.")
            return False
        
        try:
            # Run migrations in order
            self.migrate_rooms()
            self.migrate_students()
            self.migrate_inouttime()
            self.migrate_visitors()
            self.migrate_leave_applications()
            
            self.log_migration("Migration completed successfully!")
            return True
            
        except Exception as e:
            self.log_migration(f"Migration failed with error: {e}")
            return False
        finally:
            self.db.disconnect()
    
    def save_migration_log(self):
        """Save migration log to file"""
        with open('migration_log.txt', 'w', encoding='utf-8') as f:
            for log_entry in self.migration_log:
                f.write(log_entry + '\n')
        self.log_migration("Migration log saved to migration_log.txt")

def main():
    """Main migration function"""
    print("Hostel Management System - Data Migration Tool")
    print("=" * 50)
    
    migrator = DataMigrator()
    
    # Run migration
    success = migrator.run_migration()
    
    # Save log
    migrator.save_migration_log()
    
    if success:
        print("\n✓ Migration completed successfully!")
        print("You can now use the database-enabled version of the application.")
    else:
        print("\n✗ Migration failed. Check migration_log.txt for details.")

if __name__ == "__main__":
    main()

