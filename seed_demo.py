import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone

def seed_demo_data():
    db_path = 'c:/Users/laksh/OneDrive - Shiv Nadar University - Chennai/Others/Hackathons/SIH/FamilyHealthManager-main/healthcare.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. Create Demo User
    email = 'john@gmail.com'
    # Check if user already exists
    cur.execute("SELECT id FROM users WHERE email = ?", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        print("Demo user already exists. Deleting to recreate...")
        user_id = existing_user[0]
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        # Foreign key constraints (if ON DELETE CASCADE is properly set up in DB) might handle this, but let's be safe:
        # Actually SQLite doesn't enforce PRAGMA foreign_keys = ON by default in standard connect unless specified, 
        # so let's delete manually or assume it's okay.
        # Actually, let's just let it be and use a clean insert.
        cur.execute("DELETE FROM profiles WHERE manager_user_id = ?", (user_id,))

    password_hash = generate_password_hash('123456')
    cur.execute("INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)", 
                ("John Doe", email, password_hash))
    user_id = cur.lastrowid

    # 2. Create Profiles
    # Manager Profile (Self)
    cur.execute("INSERT INTO profiles (manager_user_id, profile_name, date_of_birth, gender, is_manager) VALUES (?, ?, ?, ?, ?)",
                (user_id, "John Doe", "1985-05-15", "Male", 1))
    profile_id_self = cur.lastrowid

    # Dependent Profile (Parent)
    cur.execute("INSERT INTO profiles (manager_user_id, profile_name, date_of_birth, gender, is_manager) VALUES (?, ?, ?, ?, ?)",
                (user_id, "Jane Doe (Mother)", "1955-10-22", "Female", 0))
    profile_id_parent = cur.lastrowid

    # 3. Add Medicines & Reminders for Self
    cur.execute("INSERT INTO medicines (profile_id, name, current_stock, meal_timing, meal_type, days_to_take, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (profile_id_self, "Vitamin D3", 30, "After Meal", "Breakfast", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "Supplement"))
    med_self_1 = cur.lastrowid
    cur.execute("INSERT INTO reminders (profile_id, medicine_id, time, days, note) VALUES (?, ?, ?, ?, ?)",
                (profile_id_self, med_self_1, "09:00", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "Take with milk"))

    now_ist = datetime.now()
    
    # Medicine 2 (To Take Now)
    cur.execute("INSERT INTO medicines (profile_id, name, current_stock, meal_timing, meal_type, days_to_take, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (profile_id_self, "Omega-3 Fish Oil", 60, "With Meal", "Lunch", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "Heart Health"))
    med_self_2 = cur.lastrowid
    past_due_time = (now_ist - timedelta(minutes=10)).strftime('%H:%M')
    cur.execute("INSERT INTO reminders (profile_id, medicine_id, time, days, note) VALUES (?, ?, ?, ?, ?)",
                (profile_id_self, med_self_2, past_due_time, "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "Swallow whole"))

    # Medicine 3 (To Take Later)
    cur.execute("INSERT INTO medicines (profile_id, name, current_stock, meal_timing, meal_type, days_to_take, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (profile_id_self, "Melatonin", 15, "Before Sleep", "Dinner", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "Sleep Aid"))
    med_self_3 = cur.lastrowid
    later_time = (now_ist + timedelta(hours=2)).strftime('%H:%M')
    cur.execute("INSERT INTO reminders (profile_id, medicine_id, time, days, note) VALUES (?, ?, ?, ?, ?)",
                (profile_id_self, med_self_3, later_time, "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "30 mins before bed"))

    # Add Intake Log for Vitamin D3 (Already Taken Today)
    taken_time = now_ist.replace(hour=9, minute=5, second=0).strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("INSERT INTO medicine_intake (profile_id, medicine_id, taken_at) VALUES (?, ?, ?)",
                (profile_id_self, med_self_1, taken_time))

    # 4. Add Medicines & Reminders for Parent
    cur.execute("INSERT INTO medicines (profile_id, name, current_stock, meal_timing, meal_type, days_to_take, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (profile_id_parent, "Lisinopril", 15, "Before Meal", "Breakfast", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "Blood Pressure"))
    med_parent_1 = cur.lastrowid
    cur.execute("INSERT INTO reminders (profile_id, medicine_id, time, days, note) VALUES (?, ?, ?, ?, ?)",
                (profile_id_parent, med_parent_1, "08:00", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "Important"))

    cur.execute("INSERT INTO medicines (profile_id, name, current_stock, meal_timing, meal_type, days_to_take, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (profile_id_parent, "Metformin", 50, "After Meal", "Dinner", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "Diabetes"))
    med_parent_2 = cur.lastrowid
    cur.execute("INSERT INTO reminders (profile_id, medicine_id, time, days, note) VALUES (?, ?, ?, ?, ?)",
                (profile_id_parent, med_parent_2, "20:00", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "Take with water"))

    # 5. Add Medical History
    cur.execute("INSERT INTO medical_history (profile_id, condition, description) VALUES (?, ?, ?)",
                (profile_id_parent, "Hypertension", "Diagnosed in 2015. Controlled with Lisinopril."))
    cur.execute("INSERT INTO medical_history (profile_id, condition, description) VALUES (?, ?, ?)",
                (profile_id_parent, "Type 2 Diabetes", "Diagnosed in 2018. Monitored regularly."))

    # 6. Add Emergency Contacts
    cur.execute("INSERT INTO emergency_contacts (profile_id, name, relationship, phone) VALUES (?, ?, ?, ?)",
                (profile_id_parent, "Dr. Smith", "Primary Care Physician", "555-0198"))
    cur.execute("INSERT INTO emergency_contacts (profile_id, name, relationship, phone) VALUES (?, ?, ?, ?)",
                (profile_id_self, "Mary Doe", "Spouse", "555-0123"))

    # 7. Add Some Fake Adherence/Intake Data
    today = datetime.now()
    for i in range(7):
        past_date = today - timedelta(days=i)
        date_str = past_date.strftime('%Y-%m-%d')
        # Parent Adherence
        percent = 100 if i % 3 != 0 else 50
        cur.execute("INSERT INTO adherence (profile_id, date, percentage) VALUES (?, ?, ?)",
                    (profile_id_parent, date_str, percent))
        
        # Self Adherence (100%)
        cur.execute("INSERT INTO adherence (profile_id, date, percentage) VALUES (?, ?, ?)",
                    (profile_id_self, date_str, 100))

    # 8. Add Appointments
    # Appointment for self later today
    appt_dt_1 = (now_ist + timedelta(hours=4)).replace(tzinfo=timezone(timedelta(hours=5, minutes=30))).astimezone(timezone.utc).replace(tzinfo=None)
    cur.execute("INSERT INTO appointments (profile_id, doctor_name, hospital, date_time, purpose, reminder_minutes_before) VALUES (?, ?, ?, ?, ?, ?)",
                (profile_id_self, "Dr. John Watson", "St. Mary's Clinic", appt_dt_1, "General Checkup", 60))

    # Appointment for parent tomorrow
    appt_dt_2 = (now_ist + timedelta(days=1, hours=2)).replace(tzinfo=timezone(timedelta(hours=5, minutes=30))).astimezone(timezone.utc).replace(tzinfo=None)
    cur.execute("INSERT INTO appointments (profile_id, doctor_name, hospital, date_time, purpose, reminder_minutes_before) VALUES (?, ?, ?, ?, ?, ?)",
                (profile_id_parent, "Dr. Sarah Connor", "City General Hospital", appt_dt_2, "Cardiology Follow-up", 120))

    conn.commit()
    conn.close()
    print("Successfully seeded demo user John Doe with john@gmail.com")

if __name__ == '__main__':
    seed_demo_data()
