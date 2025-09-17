#!/usr/bin/env python3
"""
Setup script for Hostel Management System
Creates all required data files and directories
"""

import os

def create_required_files():
    """Create all required data files for the Hostel Management System"""
    
    # List of required files
    required_files = [
        "room_info_boys.txt",
        "room_info_girls.txt", 
        "room_info_others.txt",
        "student_info.txt",
        "inouttime.txt",
        "visitor_info.txt",
        "leave_applications.txt"
    ]
    
    # Create each file if it doesn't exist
    for filename in required_files:
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("")  # Create empty file
            print(f"✓ Created: {filename}")
        else:
            print(f"✓ Already exists: {filename}")
    
    # Create Images directory if it doesn't exist
    if not os.path.exists("Images"):
        os.makedirs("Images")
        print("✓ Created: Images/ directory")
    else:
        print("✓ Images/ directory already exists")
    
    print("\n🎉 Setup complete! All required files have been created.")
    print("You can now run 'Hostel Management.py' without errors.")

if __name__ == "__main__":
    print("Setting up Hostel Management System...")
    print("=" * 40)
    create_required_files()
