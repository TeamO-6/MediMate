import json
import sqlite3
import os
from werkzeug.security import generate_password_hash
from PIL import Image

import shutil

def create_demo_file(profile_id, filename, file_type):
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', str(profile_id))
    demo_assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'demo_assets')
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    
    # Check if real file exists in demo_assets (try with exact name or replacing _ with space)
    real_file_path = os.path.join(demo_assets_dir, filename)
    alt_file_path = os.path.join(demo_assets_dir, filename.replace('_', ' '))
    
    if os.path.exists(real_file_path):
        shutil.copy2(real_file_path, filepath)
    elif os.path.exists(alt_file_path):
        shutil.copy2(alt_file_path, filepath)
    elif not os.path.exists(filepath):
        if file_type == 'image':
            img = Image.new('RGB', (200, 200), color=(73, 109, 137))
            img.save(filepath)
        elif file_type == 'pdf':
            with open(filepath, 'w') as f:
                f.write('This is a dummy medical report for the demo.')

def seed_demo_data():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'healthcare.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    email = 'rahul@gmail.com'
    cur.execute('SELECT id FROM users WHERE email = ?', (email,))
    existing_user = cur.fetchone()
    if existing_user:
        print('Demo user already exists. Deleting to recreate...')
        user_id = existing_user[0]
        cur.execute('DELETE FROM users WHERE id = ?', (user_id,))
        cur.execute('DELETE FROM profiles WHERE manager_user_id = ?', (user_id,))

    password_hash = generate_password_hash('123456')
    cur.execute('INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)', 
                ('Rahul Sharma', email, password_hash))
    user_id = cur.lastrowid

    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'demo_data.json')
    with open(json_path, 'r') as f:
        data = json.load(f)

    profile_id_map = {}
    medicine_id_map = {}

    for profile_key, profile_data in data.items():
        pd = profile_data['profile_details']
        cur.execute('INSERT INTO profiles (manager_user_id, profile_name, date_of_birth, gender, is_manager, profile_picture) VALUES (?, ?, ?, ?, ?, ?)',
                    (user_id, pd['profile_name'], pd['date_of_birth'], pd['gender'], pd['is_manager'], pd.get('profile_picture')))
        new_prof_id = cur.lastrowid
        
        # Map old profile ID if possible
        old_prof_id = None
        if len(profile_data.get('medicines', [])) > 0:
            old_prof_id = profile_data['medicines'][0]['profile_id']
        elif len(profile_data.get('medical_history', [])) > 0:
            old_prof_id = profile_data['medical_history'][0]['profile_id']
            
        if old_prof_id is not None:
            profile_id_map[old_prof_id] = new_prof_id

        if pd.get('profile_picture'):
            create_demo_file(new_prof_id, pd['profile_picture'], 'image')

        for med in profile_data.get('medicines', []):
            cur.execute('INSERT INTO medicines (profile_id, name, current_stock, meal_timing, meal_type, days_to_take, reason, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        (new_prof_id, med['name'], med['current_stock'], med['meal_timing'], med['meal_type'], med['days_to_take'], med['reason'], med['created_at']))
            medicine_id_map[med['id']] = cur.lastrowid

        for rem in profile_data.get('reminders', []):
            new_med_id = medicine_id_map.get(rem['medicine_id'])
            cur.execute('INSERT INTO reminders (profile_id, medicine_id, time, days, note) VALUES (?, ?, ?, ?, ?)',
                        (new_prof_id, new_med_id, rem['time'], rem['days'], rem['note']))

        for mh in profile_data.get('medical_history', []):
            cur.execute('INSERT INTO medical_history (profile_id, condition, description, report_file, created_at) VALUES (?, ?, ?, ?, ?)',
                        (new_prof_id, mh['condition'], mh['description'], mh.get('report_file'), mh['created_at']))
            if mh.get('report_file'):
                ftype = 'pdf' if mh['report_file'].endswith('.pdf') else 'image'
                create_demo_file(new_prof_id, mh['report_file'], ftype)

        for appt in profile_data.get('appointments', []):
            cur.execute('INSERT INTO appointments (profile_id, doctor_name, hospital, date_time, purpose, notes, reminder_minutes_before, reminder_sent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        (new_prof_id, appt['doctor_name'], appt['hospital'], appt['date_time'], appt['purpose'], appt['notes'], appt['reminder_minutes_before'], appt['reminder_sent']))

        for ec in profile_data.get('emergency_contacts', []):
            cur.execute('INSERT INTO emergency_contacts (profile_id, name, relationship, phone) VALUES (?, ?, ?, ?)',
                        (new_prof_id, ec['name'], ec['relationship'], ec['phone']))

        for mi in profile_data.get('medicine_intake', []):
            new_med_id = medicine_id_map.get(mi['medicine_id'])
            cur.execute('INSERT INTO medicine_intake (profile_id, medicine_id, taken_at) VALUES (?, ?, ?)',
                        (new_prof_id, new_med_id, mi['taken_at']))
                        
        for su in profile_data.get('stock_updates', []):
            new_med_id = medicine_id_map.get(su['medicine_id'])
            cur.execute('INSERT INTO stock_updates (profile_id, medicine_id, change, updated_at) VALUES (?, ?, ?, ?)',
                        (new_prof_id, new_med_id, su['change'], su['updated_at']))

        for ra in profile_data.get('recent_activities', []):
            cur.execute('INSERT INTO recent_activities (profile_id, activity_type, description, timestamp) VALUES (?, ?, ?, ?)',
                        (new_prof_id, ra['activity_type'], ra['description'], ra['timestamp']))

        for ad in profile_data.get('adherence', []):
            cur.execute('INSERT INTO adherence (profile_id, date, percentage) VALUES (?, ?, ?)',
                        (new_prof_id, ad['date'], ad['percentage']))

    conn.commit()
    conn.close()
    print('Successfully seeded demo user from JSON')

if __name__ == '__main__':
    seed_demo_data()
