from tkinter.ttk import *
from tkinter import *
from database_config import get_database
from database_operations import (StudentOperations, RoomOperations, 
                               InOutTimeOperations, VisitorOperations, 
                               LeaveApplicationOperations, AdminOperations)
from datetime import datetime

def date():
    # current date time
    now = datetime.now()
    t = now.strftime("%H:%M")
    s1 = now.strftime("%H:%M,%Y-%m-%d")
    s1 = str(s1)
    return s1 #returns Current Date And Time In String

base = Tk()
base.title("HOSTEL MANAGEMENT SYSTEM")
base.geometry(f'{1535}x{790}+{0}+{0}')
heading = Label(base, text="HOSTEL MANAGEMENT SYSTEM", font=("Arial 30 bold"), bg="lightseagreen", fg="white", padx=490, pady=20)
heading.pack()

canvas = Canvas(base, bg='silver', height=575, width=800)
canvas.place(x=330, y=130)

G = 1
def main():
    global G
    canvas = Canvas(base, bg='lightseagreen', height=675, width=310)
    canvas.place(x=-1, y=100)
    can = Canvas(base, bg='silver', height=675, width=1500)
    can.place(x=320, y=105)

    def add_stud():
        canvas = Canvas(base, bg='silver', height=675, width=1210)
        canvas.place(x=320, y=105)
        first_name = Label(base, text="First Name", font=("Arial 15 bold"), bg='silver', fg="black")
        first_name.place(x=400, y=150)
        fir_name_entry = Entry(base, width=15, font=("Arial 15"))
        fir_name_entry.place(x=400, y=180)
        fir_name_entry.focus()

        last_name = Label(base, text="Last Name", font=("Arial 15 bold"), bg="silver", fg="black")
        last_name.place(x=610, y=150)
        last_name_entry = Entry(base, width=15, font=("Arial 15"))
        last_name_entry.place(x=610, y=180)

        father_name = Label(base, text="Father Name", font=("Arial 15 bold"), bg="silver", fg="black")
        father_name.place(x=400, y=220)
        fathr_name_entry = Entry(base, width=15, font=("Arial 15"))
        fathr_name_entry.place(x=400, y=250)

        mother_name = Label(base, text="Mother Name", font=("Arial 15 bold"), bg="silver", fg="black")
        mother_name.place(x=610, y=220)
        mther_name_entry = Entry(base, width=15, font=("Arial 15"))
        mther_name_entry.place(x=610, y=250)

        dob = Label(base, text="DOB", font=("Arial 15 bold"), bg="silver", fg="black")
        dob.place(x=400, y=300)
        dob_entry = Entry(base, width=15, font=("Arial 15 bold"))
        dob_entry.place(x=400, y=330)
        m1 = Label(base, text="(Y-M-D)", font=("Arial 12 bold"), bg="silver", fg="black")
        m1.place(x=450, y=300)

        contact = Label(base, text="Contact", font=("Arial 15 bold"), bg="silver", fg="black")
        contact.place(x=610, y=300)
        cont_entry = Entry(base, width=15, font=("Arial 15 bold"))
        cont_entry.place(x=610, y=330)

        message = Label(base, text="(Contact No. will be your Hostel ID)", font=("Arial 10 bold"), bg="silver",
                        fg="black")
        message.place(x=690, y=300)

        email = Label(base, text="Email", font=("Arial 15 bold"), bg="silver", fg="black")
        email.place(x=400, y=370)
        email_entry = Entry(base, width=15, font=("Arial 15 bold"))
        email_entry.place(x=400, y=410)

        address = Label(base, text="Address", font=("Arial 15 bold"), bg="silver", fg="black")
        address.place(x=610, y=370)
        addrs_entry = Entry(base, width=15, font=("Arial 15 bold"))
        addrs_entry.place(x=610, y=410)

        vehicle = Label(base, text="Vehicle No.", font=("Arial 15 bold"), bg="silver", fg="black")
        vehicle.place(x=400, y=450)
        vehicle_entry = Entry(base, width="15", font=("Arial 15 bold"))
        vehicle_entry.place(x=400, y=490)
        m2 = Label(base, text="(MH20EU9295)", font=("Arial 11 bold"), bg="silver", fg="black")
        m2.place(x=470, y=450)

        work_place = Label(base, text="Work Place/College", font=("Arial 15 bold"), bg="silver", fg="black")
        work_place.place(x=610, y=450)
        place_entry = Entry(base, width="15", font=("Arial 15 bold"))
        place_entry.place(x=610, y=490)


        gender = Label(base, text="Gender", font=("Arial 15 bold"), bg="silver", fg="black")
        gender.place(x=400, y=580)
        G = 1
        def selected():
            global G
            if c1.get() == 1:
                G = 1
            elif c1.get() == 2:
                G = 2
            elif c1.get() == 0:
                G = 0
            else:
                G = 1
        c1 = IntVar()
        a = Radiobutton(base, text="Male", bg="silver", fg="black", font=("Arial 15 bold"), variable=c1, value=1,
                        command=selected)
        b = Radiobutton(base, text="Female", bg="silver", fg="black", font=("Arial 15 bold"), variable=c1, value=2,
                        command=selected)
        c = Radiobutton(base, text="Other", bg="silver", fg="black", font=("Arial 15 bold"), variable=c1, value=0,
                        command=selected)
        a.place(x=490, y=580)
        b.place(x=580, y=580)
        c.place(x=680, y=580)
        def available_roome():
            rooms_availble = Label(base, text="Rooms Available", font=("Arial 20 bold"), bg="lightseagreen",
                                   fg="white", padx=140)
            rooms_availble.place(x=1005, y=110)
            x = "    Room No.                       |                                 Beds"
            room = Label(base, text=x, font=("Arial 15 bold"), bg="dark slate grey", fg="white")
            room.place(x=1005, y=150)
            
            global G
            # Map gender to database values
            gender_map = {1: 'Male', 2: 'Female', 0: 'Other'}
            gender = gender_map.get(G, 'Male')
            
            # Get available rooms from database
            try:
                rooms_data = RoomOperations.get_available_rooms(gender)
                if not rooms_data:
                    y = "No Rooms Available"
                    x = Label(base, text=y, font=("Arial", 40), bg="dark slate grey", fg="white")
                    x.place(x=1020, y=300)
                    return
                
                x1co = 1150
                y1co = 200
                x2co = 1350
                y2co = 200
                flag = 1
                
                for room in rooms_data:
                    if flag > 8:
                        break
                    
                    r_no = Label(base, text=room['room_number'], font=("Arial", 15), bg="silver", fg="black")
                    r_no.place(x=x1co, y=y1co)
                    
                    # Create bed status string
                    bed_status = []
                    if not room['bed1_occupied']:
                        bed_status.append("B1")
                    else:
                        bed_status.append("NA")
                    if not room['bed2_occupied']:
                        bed_status.append("B2")
                    else:
                        bed_status.append("NA")
                    if not room['bed3_occupied']:
                        bed_status.append("B3")
                    else:
                        bed_status.append("NA")
                    
                    y = "   ".join(bed_status)
                    r_bk_no = Label(base, text=y, font=("Arial", 15), bg="silver", fg="black")
                    r_bk_no.place(x=x2co, y=y2co)
                    
                    y1co = y1co + 40
                    y2co = y2co + 40
                    flag = flag + 1
                    
            except Exception as e:
                error_msg = f"Error loading rooms: {str(e)}"
                error_label = Label(base, text=error_msg, font=("Arial", 15), bg="red", fg="white")
                error_label.place(x=1020, y=300)

            c1 = Canvas(base, height=2, width=600)
            c1.place(x=1000, y=550)
            r1 = Label(base, text="Room No.", font=("Arial 15 bold"), bg="silver", fg="black")
            r1.place(x=1040, y=570)
            r2 = Entry(base, width=15, font=("Arial 15 bold"))
            r2.place(x=1150, y=570)
            r3 = Label(base, text="Bed No.", font=("Arial 15 bold"), bg="silver", fg="black")
            r3.place(x=1040, y=610)
            r4 = Entry(base, width=15, font=("Arial 15 bold"))
            r4.place(x=1150, y=610)
            r5 = Label(base, text="(B1 B2 B3)", font=("Arial 10 bold"), bg="silver", fg="black")
            r5.place(x=1040, y=640)
            r6 = Label(base, text="( Girl = G1 )", font=("Arial 15 bold"), bg="silver", fg="black")
            r6.place(x=1350,y=570)
            r7 = Label(base, text="( Other = O1)",font=("Arial 15 bold"), bg="silver", fg="black")
            r7.place(x=1350,y=610)
            def student():
                global G
                try:
                    # Map gender to database values
                    gender_map = {1: 'Male', 2: 'Female', 0: 'Other'}
                    gender = gender_map.get(G, 'Male')
                    
                    # Prepare student data
                    student_data = {
                        'contact': str(cont_entry.get()),
                        'first_name': str(fir_name_entry.get()),
                        'last_name': str(last_name_entry.get()),
                        'father_name': str(fathr_name_entry.get()),
                        'mother_name': str(mther_name_entry.get()),
                        'dob': str(dob_entry.get()),
                        'email': str(email_entry.get()),
                        'address': str(addrs_entry.get()),
                        'vehicle': str(vehicle_entry.get()),
                        'workplace': str(place_entry.get()),
                        'gender': gender,
                        'room_number': str(r2.get()),
                        'bed_number': str(r4.get()).upper(),
                        'registration_date': datetime.now()
                    }
                    
                    # Add student to database
                    success, message = StudentOperations.add_student(student_data)
                    
                    if success:
                        l = Label(base, text="Student Added Successfully....!", font=("Arial 15 bold"), bg='silver',
                                  fg="black")
                        l.place(x=1150, y=650)
                    else:
                        l = Label(base, text=f"Error: {message}", font=("Arial 15 bold"), bg='red',
                                  fg="white")
                        l.place(x=1150, y=650)
                        
                except Exception as e:
                    l = Label(base, text=f"Error: {str(e)}", font=("Arial 15 bold"), bg='red',
                              fg="white")
                    l.place(x=1150, y=650)
            add_student = Button(base, text="Add Student", font=("Arial 20 bold"), bg="white", fg="black" ,command=student)
            add_student.place(x=1040, y=700)

        c1 = IntVar()
        a = Radiobutton(base, text="Male", bg="silver", fg="black", font=("Arial 15 bold"), variable=c1, value=1, command=selected)
        b = Radiobutton(base, text="Female", bg="silver", fg="black", font=("Arial 15 bold"), variable=c1, value=2, command=selected)
        c = Radiobutton(base, text="Other", bg="silver", fg="black", font=("Arial 15 bold"), variable=c1, value=0, command=selected)
        a.place(x=490,y=580)
        b.place(x=580,y=580)
        c.place(x=680,y=580)
        continu = Button(base, text="Continue", font=("Arial 15 bold"), bg="white", command=available_roome)
        continu.place(x=490, y=670)

        line = Canvas(base, height=670, width=2)
        line.place(x=1000, y=105)
    def add_room():
        canvas = Canvas(base, bg='silver', height=675, width=1210)
        canvas.place(x=320, y=105)
        h1 = Label(base, text="Add New Room", bg="dark slate grey", font=("Arial 20 bold"), fg="white", padx=500,
                   pady=10)
        h1.place(x=320, y=105)

        n_rm_n = Label(base, text="New Room No.", font=("Arial 20 bold"), bg="silver", fg="black")
        n_rm_n.place(x=500, y=300)
        rm_n_entry = Entry(base, width=20, font=("Arial 15 bold"))
        rm_n_entry.place(x=750, y=303)
        gender = Label(base,text="Gender", font=("Arial 20 bold"), bg="silver", fg="black")
        gender.place(x=500,y=350)

        global G
        G = 1
        def selected():
            global G
            if c1.get() == 1:
                G = 1
            if c1.get() == 2:
                G = 2
            if c1.get() == 0:
                G = 0
        c1 = IntVar()
        a = Radiobutton(base, text="Male", bg="silver", fg="black", font=("Arial 15 bold"), variable=c1, value=1,
                        command=selected)
        b = Radiobutton(base, text="Female", bg="silver", fg="black", font=("Arial 15 bold"), variable=c1, value=2,
                        command=selected)
        c = Radiobutton(base, text="Other", bg="silver", fg="black", font=("Arial 15 bold"), variable=c1, value=0,
                        command=selected)
        a.place(x=750, y=350)
        b.place(x=840, y=350)
        c.place(x=950, y=350)
        def add():
            try:
                global G
                room_number = str(rm_n_entry.get())
                
                # Map gender to database values
                gender_map = {1: 'Male', 2: 'Female', 0: 'Other'}
                gender = gender_map.get(G, 'Male')
                
                # Add room to database
                success = RoomOperations.add_room(room_number, gender)
                
                if success:
                    l = Label(base, text="ROOM Successfully Added....!", font=("Arial 25 bold"), bg='silver',
                              fg="black")
                    l.place(x=650, y=600)
                else:
                    l = Label(base, text="Room Is Already Added or Error Occurred....!", font=("Arial 25 bold"), bg='red',
                              fg="white")
                    l.place(x=650, y=600)
                    
            except Exception as e:
                l = Label(base, text=f"Error: {str(e)}", font=("Arial 25 bold"), bg='red',
                          fg="white")
                l.place(x=650, y=600)

        ad_rm_btn = Button(base, text="Add Room", font=("Arial 20 bold"), bg="white", fg="black", command=add)
        ad_rm_btn.place(x=550, y=500)

    def in_out_time():
        canvas = Canvas(base, bg='silver', height=675, width=1210)
        canvas.place(x=320, y=105)

        a = "---------------Outtime---------------"
        out_time_h1 = Label(base, text=a, font=("Arial 20 bold"), bg="dark slate grey", fg="white", padx=20,
                            pady=10)
        out_time_h1.place(x=320, y=115)

        out_time = Label(base, text="Enter ID", font=("Arial 20 bold"), bg="silver", fg="black")
        out_time.place(x=470, y=200)
        out_time_entry = Entry(base, width=20, font=("Arial 20 bold"))
        out_time_entry.place(x=620, y=200)
        out_time_entry.focus()

        purpose = Label(base, text="Purpose", font=("Arial 20 bold"), bg="silver", fg="black")
        purpose.place(x=470, y=270)
        purpose_entry = Entry(base, width=20, font=("Arial 20 bold"))
        purpose_entry.place(x=620, y=270)

        def save1():
            try:
                student_id = str(out_time_entry.get())
                purpose = str(purpose_entry.get())
                
                # Log out time to database
                success = InOutTimeOperations.log_out_time(student_id, purpose)
                
                if success:
                    done = Label(base, text="Successfull...!", font=("Arial 20 bold"), bg="silver", fg="black")
                    done.place(x=1200, y=220)
                else:
                    done = Label(base, text="Error logging out time...!", font=("Arial 20 bold"), bg="red", fg="white")
                    done.place(x=1200, y=220)
                    
            except Exception as e:
                done = Label(base, text=f"Error: {str(e)}", font=("Arial 20 bold"), bg="red", fg="white")
                done.place(x=1200, y=220)

        save1 = Button(base, text="Save", font=("Arial 20 bold"), bg="white", fg="black", command=save1)
        save1.place(x=1050, y=220)

        a1 = "---------------Inttime---------------"
        in_time_h1 = Label(base, text=a1, font=("Arial 20 bold"), bg="dark slate grey", fg="white", padx=20,
                           pady=10)
        in_time_h1.place(x=320, y=400)

        in_time = Label(base, text="Enter ID", font=("Arial 20 bold"), bg="silver", fg="black")
        in_time.place(x=470, y=500)
        in_time_entry = Entry(base, width=20, font=("Arial 20 bold"))
        in_time_entry.place(x=680, y=500)
        in_time_entry.focus()

        ot_entry = Label(base, text="Outtime Entry", font=("Arial 20 bold"), bg="silver", fg="black")
        ot_entry.place(x=470, y=550)
        ot_entry_entry = Entry(base, width=20, font=("Arial 20 bold"))
        ot_entry_entry.place(x=680, y=550)

        def search_outtime():
            try:
                student_id = str(in_time_entry.get())
                
                # Get out time entry from database
                out_time_entry = InOutTimeOperations.get_out_time_entry(student_id)
                
                tv = StringVar()
                if out_time_entry:
                    # Format the out time for display
                    out_time_str = out_time_entry['out_time'].strftime("%H:%M,%Y-%m-%d")
                    tv.set(out_time_str + "     OUTTIME")
                else:
                    tv.set("Invalid Id")
                
                ot = Entry(base, width=20, textvariable=tv, font=("Arial 20 bold"))
                ot.place(x=680, y=550)
                
            except Exception as e:
                tv = StringVar()
                tv.set(f"Error: {str(e)}")
                ot = Entry(base, width=20, textvariable=tv, font=("Arial 20 bold"))
                ot.place(x=680, y=550)

        def save2():
            try:
                remark = str(r_sel.get())
                student_id = str(in_time_entry.get())
                
                # Log in time to database
                success = InOutTimeOperations.log_in_time(student_id, remark)
                
                if success:
                    done = Label(base, text="Successful...!", font=("Arial 20 bold"), bg="silver", fg="black")
                    done.place(x=700, y=720)
                else:
                    done = Label(base, text="Please Give Correct Information", font=("Arial 20 bold"), bg="red",
                                 fg="white")
                    done.place(x=600, y=720)
                    
            except Exception as e:
                done = Label(base, text=f"Error: {str(e)}", font=("Arial 20 bold"), bg="red", fg="white")
                done.place(x=600, y=720)

        sear_ot = Button(base, text="Search Outtime", font=("Arial 18 bold"), bg="white", command=search_outtime)
        sear_ot.place(x=1050, y=520)
        save2 = Button(base, text="Save", font=("Arial 20 bold"), bg="white", fg="black", command=save2)
        save2.place(x=1050, y=700)

        r_sel = StringVar(base)
        ls = ['Before Time', 'On Time', 'Late']
        r_sel.set(ls[0])
        remark = OptionMenu(base, r_sel, *ls)
        remark.config(width=20, font=("Arial 15 bold"), fg="black")
        remark.place(x=680, y=610)

    def visitor():
        canvas = Canvas(base, bg='silver', height=675, width=1210)
        canvas.place(x=320, y=105)

        h1 = Label(base, text="Visitor's   Information", bg="dark slate grey", font=("Arial 20 bold"), fg="white",
                   padx=480, pady=10)
        h1.place(x=320, y=105)
        v_name = Label(base, text="Name", font=("Arial 20 bold"), bg="silver", fg="black")
        v_name.place(x=500, y=200)
        v_name_entry = Entry(base, width=20, font=("Arial 20 bold"))
        v_name_entry.place(x=650, y=200)

        v_contact = Label(base, text="Contact", font=("Arial 20 bold"), bg="silver", fg="black")
        v_contact.place(x=500, y=300)
        v_contact_entry = Entry(base, width=20, font=("Arial 20 bold"))
        v_contact_entry.place(x=650, y=300)

        v_reason = Label(base, text="Reason", font=("Arial 20 bold"), bg="silver", fg="black")
        v_reason.place(x=500, y=400)
        v_reason_entry = Entry(base, width=20, font=("Arial 20 bold"))
        v_reason_entry.place(x=650, y=400)

        v_address = Label(base, text="Address", font=("Arial 20 bold"), bg="silver", fg="black")
        v_address.place(x=500, y=500)
        v_address_entry = Entry(base, width=20, font=("Arial 20 bold"))
        v_address_entry.place(x=650, y=500)

        st_name = Label(base, text="Student Name", font=("Arial 20 bold"), bg="silver", fg="black")
        st_name.place(x=1020, y=200)
        st_name_entry = Entry(base, width=15, font=("Arial 20 "))
        st_name_entry.place(x=1250, y=200)

        def search():
            def reset():
                ot.destroy()
                st_name_entry.delete(0, END)
                st_name_entry.place(x=1250, y=200)

            def add_visitor():
                try:
                    visitor_data = {
                        'student_id': student_id,
                        'visitor_name': str(v_name_entry.get()),
                        'visitor_contact': str(v_contact_entry.get()),
                        'reason': str(v_reason_entry.get()),
                        'visitor_address': str(v_address_entry.get()),
                        'visit_date': datetime.now()
                    }
                    
                    success = VisitorOperations.add_visitor(visitor_data)
                    
                    if success:
                        s = Label(base, text="Successfull...!", font=("Arial 20 bold"), bg="dark slate grey", fg="white",
                                  padx=100)
                        s.place(x=1100, y=700)
                    else:
                        s = Label(base, text="Error adding visitor...!", font=("Arial 20 bold"), bg="red", fg="white",
                                  padx=100)
                        s.place(x=1100, y=700)
                        
                except Exception as e:
                    s = Label(base, text=f"Error: {str(e)}", font=("Arial 20 bold"), bg="red", fg="white",
                              padx=100)
                    s.place(x=1100, y=700)

            reset_btn = Button(base, text="Reset", font=("Arial 20 bold"), command=reset)
            reset_btn.place(x=1340, y=280)
            
            try:
                student_name = str(st_name_entry.get())
                
                # Search student by name in database
                students = StudentOperations.search_student_by_name(student_name)
                
                if students:
                    student = students[0]  # Take first match
                    student_id = student['student_id']
                    room_number = student.get('room_number', 'N/A')
                    
                    tv = StringVar()
                    tv.set(room_number)
                    ot_name = Label(base, text="Room No.", font=("Arial 20 bold"), bg="silver")
                    ot_name.place(x=1020, y=400)
                    ot = Entry(base, width=15, textvariable=tv, font=("Arial 20 bold"), justify=CENTER)
                    ot.place(x=1250, y=400)
                    add_btn = Button(base, text="Add Visitor", font=("Arial 20 bold"), command=add_visitor)
                    add_btn.place(x=1100, y=500)
                else:
                    tv = StringVar()
                    tv.set("Invalid Name")
                    ot = Entry(base, width=15, textvariable=tv, font=("Arial 20 bold"), fg="red")
                    ot.place(x=1250, y=200)
                    
            except Exception as e:
                tv = StringVar()
                tv.set(f"Error: {str(e)}")
                ot = Entry(base, width=15, textvariable=tv, font=("Arial 20 bold"), fg="red")
                ot.place(x=1250, y=200)

        line = Canvas(base, height=650, width=5)
        line.place(x=1000, y=162)

        ser_btn = Button(base, text="Search", font=("Arial 20 bold"), command=search)
        ser_btn.place(x=1180, y=280)


    def view_info():
        canvas = Canvas(base, bg='silver', height=675, width=1215)
        canvas.place(x=320, y=105)

        def all_girl_info():
            canvas = Canvas(base, bg='silver', height=675, width=810)
            canvas.place(x=715, y=105)
            h1 = Label(base, text="Information Of Students", font=("Arial 20 bold"), bg="dark slate grey", fg="white",
                       padx=270, pady=5)
            h1.place(x=720, y=105)

            h = "Room NO.           Name             Contact             Workplace"
            h2 = Label(base, text=h, font=("Arial 20 bold"), bg="dark orange", fg="white")
            h2.place(x=723, y=150)

            try:
                # Get all students from database
                students = StudentOperations.get_all_students()
                
                x1co = 800
                y1co = 200
                x2co = 900
                x3co = 1160
                x4co = 1380
                flag = 1

                for student in students:
                    if flag > 8:
                        break
                    
                    # Display student information
                    label = Label(base, text=student.get('room_number', 'N/A'), font=("Arial 15 bold"), bg="silver", fg="black")
                    label.place(x=x1co, y=y1co)
                    label2 = Label(base, text=f"{student['first_name']} {student['last_name']}", font=("Arial 15 bold"), bg="silver", fg='black')
                    label2.place(x=x2co, y=y1co)
                    label3 = Label(base, text=student['student_id'], font=('Arial 15 bold'), bg="silver", fg='black')
                    label3.place(x=x3co, y=y1co)
                    label4 = Label(base, text=student['workplace_college'], font=("Arial 15 bold"), bg="silver", fg="black")
                    label4.place(x=x4co, y=y1co)
                    
                    y1co = y1co + 50
                    flag = flag + 1
                    
            except Exception as e:
                error_label = Label(base, text=f"Error loading students: {str(e)}", font=("Arial 15 bold"), bg="red", fg="white")
                error_label.place(x=800, y=200)

        def room_wise():
            canvas = Canvas(base, bg='silver', height=675, width=810)
            canvas.place(x=715, y=105)
            l1 = Label(base, text="Enter Room No.", font=("Arial 20 bold"), bg="silver", fg="black")
            l1.place(x=750, y=150)
            l1_entry = Entry(base, width=10, font=("Arial 20 bold"))
            l1_entry.place(x=1000, y=150)
            l1_entry.focus()

            def search():
                try:
                    room_number = str(l1_entry.get())
                    
                    # Get students by room number from database
                    students = StudentOperations.get_students_by_room(room_number)
                    
                    h1 = Label(base, text="Information Of Students", font=("Arial 20 bold"), bg="dark slate grey",
                               fg="white", padx=270, pady=5)
                    h1.place(x=720, y=250)

                    h = "Bed No.              Name                 Contact                Workplace"
                    h2 = Label(base, text=h, font=("Arial 20 bold"), bg="dark orange", fg="white")
                    h2.place(x=723, y=300)
                    
                    if not students:
                        no_students = Label(base, text="No students found in this room", font=("Arial 15 bold"), bg="silver", fg="black")
                        no_students.place(x=800, y=400)
                        return
                    
                    x1co = 780
                    y1co = 400
                    x2co = 900
                    x3co = 1160
                    x4co = 1380
                    flag = 1

                    for student in students:
                        if flag > 2:
                            break
                        
                        # Display student information
                        label = Label(base, text=student['bed_number'], font=("Arial 15 bold"), bg="silver", fg="black")
                        label.place(x=x1co, y=y1co)
                        label2 = Label(base, text=f"{student['first_name']} {student['last_name']}", font=("Arial 15 bold"), bg="silver", fg='black')
                        label2.place(x=x2co, y=y1co)
                        label3 = Label(base, text=student['student_id'], font=('Arial 15 bold'), bg="silver", fg='black')
                        label3.place(x=x3co, y=y1co)
                        label4 = Label(base, text=student['workplace_college'], font=("Arial 15 bold"), bg="silver", fg="black")
                        label4.place(x=x4co, y=y1co)
                        
                        y1co = y1co + 100
                        flag = flag + 1
                        
                except Exception as e:
                    error_label = Label(base, text=f"Error loading room info: {str(e)}", font=("Arial 15 bold"), bg="red", fg="white")
                    error_label.place(x=800, y=400)

            search_btn = Button(base, text="Search", font=("Arial 20 bold"), command=search)
            search_btn.place(x=1200, y=140)

        stud_info = Button(base, text="Information Of All Students", wraplength=180, justify=CENTER,
                            font=("Arial 20 bold"), padx=50, pady=1, command=all_girl_info)
        stud_info.place(x=400, y=200)

        stud_room_wise = Button(base, text="Room Info", font=("Arial 20 bold"), padx=60, pady=5, command=room_wise)
        stud_room_wise.place(x=400, y=400)

        line = Canvas(base, height=680, width=5)
        line.place(x=710, y=105)

    def leave_application():
        canvas = Canvas(base, bg='silver', height=675, width=1210)
        canvas.place(x=320, y=105)
        h1 = Label(base, text="Leave Application", bg="dark slate grey", font=("Arial 20 bold"), fg="white",
                   padx=485, pady=10)
        h1.place(x=320, y=105)

        h_id = Label(base, text="Hostel ID", bg="silver", font=("Arial 20 bold"), fg="black")
        h_id.place(x=400, y=200)
        id_entry = Entry(base, width=15, font=("Arial 20"))
        id_entry.place(x=550, y=200)

        n_label = Label(base, text="Name", bg="silver", font=("Arial 20 bold"), fg="black")
        n_label.place(x=800, y=200)
        n_entry = Entry(base, width=20, font=("Arial 20"))
        n_entry.place(x=900, y=200)

        r_label = Label(base, text="Room No.", bg="silver", font=("Arial 20 bold"), fg="black")
        r_label.place(x=400, y=300)
        r_entry = Entry(base, width=15, font=("Arial 20"))
        r_entry.place(x=550, y=300)

        m_no = Label(base, text="Mobile No.", bg="silver", font=("Arial 20 bold"), fg="black")
        m_no.place(x=800, y=300)
        m_entry = Entry(base, width=15, font=("Arial 20"))
        m_entry.place(x=950, y=300)

        reason = Label(base, text="Reason For Leave", bg="silver", font=("Arial 20 bold"), fg="black")
        reason.place(x=400, y=400)

        reason_entry = Entry(base, width=20, font=("Arial 20"))
        reason_entry.place(x=700, y=400)

        return_date = Label(base, text="Return Date", bg="silver", font=("Arial 20 bold"), fg="black")
        return_date.place(x=400, y=500)
        x = Label(base, text="(YEAR-DD-MM)", font=("Arial 15 bold"), bg="silver", fg="black")
        x.place(x=1000, y=500)
        date_entry = Entry(base, width=18, font=("Arial 20"))
        date_entry.place(x=700, y=500)

        def leave_info():
            try:
                application_data = {
                    'student_id': str(id_entry.get()),
                    'student_name': str(n_entry.get()),
                    'room_number': str(r_entry.get()),
                    'mobile_number': str(m_entry.get()),
                    'reason': str(reason_entry.get()),
                    'application_date': datetime.now(),
                    'return_date': str(date_entry.get())
                }
                
                success = LeaveApplicationOperations.submit_leave_application(application_data)
                
                if success:
                    success_label = Label(base, text="Submit Successfully..!", font=("Arial 20 bold"), fg="green", bg="white")
                    success_label.place(x=700, y=700)
                else:
                    error_label = Label(base, text="Error submitting application..!", font=("Arial 20 bold"), fg="red", bg="white")
                    error_label.place(x=700, y=700)
                    
            except Exception as e:
                error_label = Label(base, text=f"Error: {str(e)}", font=("Arial 20 bold"), fg="red", bg="white")
                error_label.place(x=700, y=700)

        submit = Button(base, text="Submit", font=("Arial 20 bold"), fg="black", command=leave_info)
        submit.place(x=700, y=600)

    add_std_btn = Button(base, text="Add Student", font=("Arial 20 bold"), padx=15, bg="white", command=add_stud)
    add_std_btn.place(x=50, y=150)

    add_new_room = Button(base, text="Add New Room", font=("Arial 20 bold"), bg="white", command=add_room)
    add_new_room.place(x=50, y=250)

    in_ot_time = Button(base, text="In And Outtime", font=("Arial 20 bold"), bg="white", command=in_out_time)
    in_ot_time.place(x=50, y=350)

    visitor = Button(base, text="Visitor", font=("Arial 20 bold"), bg="white", padx=55, command=visitor)
    visitor.place(x=50, y=450)

    view_info = Button(base, text="View Information", font=("Arial 18 bold"), bg="white", command=view_info)
    view_info.place(x=50, y=535)

    leave_application = Button(base, text="Leave Application", font=("Arial 18 bold"), bg="white", command=leave_application)
    leave_application.place(x=50, y=620)

    exit = Button(base, text="EXIT", font=("Arial 18 bold"), bg="white", padx=70, command=quit)
    exit.place(x=50, y=700)

username = Label(base, text="Username", font=("Arial 25 bold"), bg="silver", fg="black")
username.place(x=470, y=240)
user_entry = Entry(base, width=17, font=("Arial 20"))
user_entry.place(x=650, y=245)
user_entry.focus()

password = Label(base, text="Password", font=("Arial 25 bold"), bg="silver", fg="black")
password.place(x=470, y=350)
pass_entry = Entry(base, width=17, font="Arial 20")
pass_entry.place(x=650, y=355)

def login():
    try:
        username = str(user_entry.get())
        password = str(pass_entry.get())
        
        # Verify login using database
        if AdminOperations.verify_login(username, password):
            main()
        else:
            user_entry.focus()
            user_entry.delete(0, END)
            pass_entry.delete(0, END)
            fail = Label(base, text="Wrong Username Or Password...!", font=("Arial 30 bold"), bg="silver", fg="red")
            fail.place(x=450, y=540)
            
    except Exception as e:
        user_entry.focus()
        user_entry.delete(0, END)
        pass_entry.delete(0, END)
        fail = Label(base, text=f"Login Error: {str(e)}", font=("Arial 30 bold"), bg="silver", fg="red")
        fail.place(x=450, y=540)


login_btn = Button(base, text="Login", font=("Arial 25 bold"), bg="lightseagreen", fg="white", command=login)
login_btn.place(x=650, y=440)

base.mainloop()
