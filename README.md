## Hostel Management System
A simple Hostel Management System built with Python Tkinter and plain text file storage (no database). It manages students, rooms, visitors, in/out time logs, and leave applications.

### Requirements
- Python 3.8+
- Tkinter (bundled with standard Python on Windows/macOS; on some Linux distros install via your package manager)

### Project Structure
- `Hostel Management.py`: Main GUI application
- `Images/`: Screenshots used in this README
- Text data files created at runtime (see below)

### Run
1. Ensure you have Python 3 installed.
2. Create the following empty text files in the project root before first run (the app expects them to exist):
   - `room_info_boys.txt`
   - `room_info_girls.txt`
   - `room_info_others.txt`
   - `student_info.txt`
   - `inouttime.txt`
   - `visitor_info.txt`
   - `leave_applications.txt`
3. Start the app:
   - Windows: Right‑click `Hostel Management.py` → Open with Python
   - Or from terminal: `python "Hostel Management.py"`

### Default Login
- Username: `mrityunjay`
- Password: `312345670`

These values are hardcoded in `Hostel Management.py` inside the `login()` function.

### Change the Login Credentials
1. Open `Hostel Management.py`.
2. Find the `login()` function near the bottom.
3. Replace the two string literals in the condition with your desired username and password, e.g.:

```python
if id == "YourUsername" and key == "YourPassword":
    main()
```

Optional (slightly safer): move them to module‑level constants or read from an environment file to avoid editing code for future changes.

### Core Features
- Add Student: Register student details and assign a specific bed in a room
- Add New Room: Create rooms for Boys/Girls/Others with three beds each (e.g., B1/B2/B3)
- In/Out Time: Log outtime and subsequently record the corresponding intime with a remark (Before Time/On Time/Late)
- Visitor: Record visitor details for a student
- View Information: List all students or search by room number
- Leave Application: Submit and store leave requests

### Data Storage (Text Files)
- Rooms per gender: `room_info_boys.txt`, `room_info_girls.txt`, `room_info_others.txt`
  - Format per line (after adding rooms): `roomNo,B1,B2,B3,NOT,`
  - When a bed is allocated, the placeholder (e.g., `B1`) is replaced with the student contact/ID and the trailing `NOT` is updated with the date
- Students: `student_info.txt`
- In/Out logs: `inouttime.txt`
- Visitors: `visitor_info.txt`
- Leave applications: `leave_applications.txt`

Note: The app opens room files in read mode in several places; ensure the files exist before running. Empty files are fine.

### Tips
- Create rooms first so that beds are available to assign when adding students
- The contact number acts as the Hostel ID during student registration
- If you see “No Rooms Available,” add rooms for the selected gender

### Screenshots
![Login](https://raw.githubusercontent.com/ShaileshGodghase/Hostel-Management-System-/main/Images/Login.png)

![Add Student](https://raw.githubusercontent.com/ShaileshGodghase/Hostel-Management-System-/main/Images/addStudents.png)

![Add New Room](https://raw.githubusercontent.com/ShaileshGodghase/Hostel-Management-System-/main/Images/AddNewRoom.png)

![All Information](https://raw.githubusercontent.com/ShaileshGodghase/Hostel-Management-System-/main/Images/allInfo.png)

![Room Information](https://raw.githubusercontent.com/ShaileshGodghase/Hostel-Management-System-/main/Images/RoomInfo.png)

![In and Out Time](https://raw.githubusercontent.com/ShaileshGodghase/Hostel-Management-System-/main/Images/inOutTime.png)

![Visitor](https://raw.githubusercontent.com/ShaileshGodghase/Hostel-Management-System-/main/Images/visitor.png)

![Leave Application](https://raw.githubusercontent.com/ShaileshGodghase/Hostel-Management-System-/main/Images/Leave-Application.png)
