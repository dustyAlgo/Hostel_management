import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration and connection management"""
    
    def __init__(self):
        # Database configuration - Update these values as needed
        self.config = {
            'host': 'localhost',
            'database': 'hostel_management',
            'user': 'root',  # Change to your MySQL username
            'password': 'pass@1234',  # Change to your MySQL password
            'port': 3306,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True
        }
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                logger.info("Successfully connected to MySQL database")
                return True
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            return False
        return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed")
    
    def get_connection(self):
        """Get current database connection"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute SQL query and return results if needed"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                connection.commit()
                cursor.close()
                return True
                
        except Error as e:
            logger.error(f"Error executing query: {e}")
            return False
    
    def execute_many(self, query, params_list):
        """Execute query with multiple parameter sets"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.executemany(query, params_list)
            connection.commit()
            cursor.close()
            return True
        except Error as e:
            logger.error(f"Error executing batch query: {e}")
            return False

# Global database instance
db = DatabaseConfig()

def get_database():
    """Get database instance"""
    return db

def test_connection():
    """Test database connection"""
    if db.connect():
        print("✓ Database connection successful!")
        db.disconnect()
        return True
    else:
        print("✗ Database connection failed!")
        print("Please check your MySQL configuration in database_config.py")
        return False

if __name__ == "__main__":
    # Test the database connection
    test_connection()

