"""
Database Setup Script
Sets up MySQL database for Hostel Management System
"""

import mysql.connector
from mysql.connector import Error
import os
import sys

def create_database():
    """Create the database and tables"""
    
    # Database configuration
    config = {
        'host': 'localhost',
        'user': 'root',  # Change to your MySQL username
        'password': '',  # Change to your MySQL password
        'port': 3306
    }
    
    try:
        # Connect to MySQL server
        print("Connecting to MySQL server...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Create database
        print("Creating database 'hostel_management'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS hostel_management")
        cursor.execute("USE hostel_management")
        
        # Read and execute schema file
        print("Creating tables...")
        with open('database_schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Split by semicolon and execute each statement
        statements = schema_sql.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Error as e:
                    if "already exists" not in str(e).lower():
                        print(f"Warning: {e}")
        
        connection.commit()
        print("✓ Database and tables created successfully!")
        
        # Test connection with the new database
        cursor.close()
        connection.close()
        
        # Test with our database config
        from database_config import test_connection
        if test_connection():
            print("✓ Database connection test successful!")
            return True
        else:
            print("✗ Database connection test failed!")
            return False
            
    except Error as e:
        print(f"Error: {e}")
        print("\nPlease check your MySQL configuration:")
        print("1. Make sure MySQL server is running")
        print("2. Update the database configuration in this script")
        print("3. Ensure you have the correct username and password")
        return False

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Required packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install packages: {e}")
        return False

def main():
    """Main setup function"""
    print("Hostel Management System - Database Setup")
    print("=" * 50)
    
    # Check if MySQL is available
    try:
        import mysql.connector
    except ImportError:
        print("MySQL connector not found. Installing requirements...")
        if not install_requirements():
            print("Failed to install requirements. Please install manually:")
            print("pip install mysql-connector-python")
            return
    
    # Create database
    if create_database():
        print("\n🎉 Database setup completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python migrate_data.py' to migrate existing data")
        print("2. Run 'python Hostel Management Database.py' to start the application")
    else:
        print("\n❌ Database setup failed!")
        print("Please check your MySQL configuration and try again.")

if __name__ == "__main__":
    main()

