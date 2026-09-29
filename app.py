from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import json
import functools
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'medtrack_cloud_secret_key_2026_super_secure!')

# ==========================================
# TEMPORARY IN-MEMORY STORAGE (EPIC 1)
# Ready for AWS DynamoDB Migration in Phase 2
# ==========================================

users = [
    {
        'id': 'U101',
        'name': 'Sarah Jenkins',
        'email': 'dr.jenkins@medtrack.com',
        'password': generate_password_hash('doctor123'),
        'role': 'Doctor',
        'phone': '+1 (555) 234-5678'
    },
    {
        'id': 'U102',
        'name': 'Robert Chen',
        'email': 'dr.chen@medtrack.com',
        'password': generate_password_hash('doctor123'),
        'role': 'Doctor',
        'phone': '+1 (555) 345-6789'
    },
    {
        'id': 'U103',
        'name': 'Emily Vance',
        'email': 'dr.vance@medtrack.com',
        'password': generate_password_hash('doctor123'),
        'role': 'Doctor',
        'phone': '+1 (555) 456-7890'
    },
    {
        'id': 'U201',
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': generate_password_hash('patient123'),
        'role': 'Patient',
        'phone': '+1 (555) 876-5432'
    },
    {
        'id': 'U202',
        'name': 'Kusuma Sharma',
        'email': 'xyz@gmail.com',
        'password': generate_password_hash('patient123'),
        'role': 'Patient',
        'phone': '+1 (555) 987-6543'
    },
    {
        'id': 'U301',
        'name': 'System Administrator',
        'email': 'admin@medtrack.com',
        'password': generate_password_hash('admin123'),
        'role': 'Admin',
        'phone': '+1 (555) 000-1111'
    }
]

doctors = [
    {
        'doctor_id': 'D101',
        'user_id': 'U101',
        'name': 'Dr. Sarah Jenkins',
        'specialization': 'Cardiology',
        'experience': '12 Years',
        'bio': 'Specialist in cardiovascular diseases and preventive heart health care.',
        'availability': 'Mon - Fri (09:00 AM - 04:00 PM)'
    },
    {
        'doctor_id': 'D102',
        'user_id': 'U102',
        'name': 'Dr. Robert Chen',
        'specialization': 'Neurology',
        'experience': '9 Years',
        'bio': 'Expert in nervous system disorders, migraines, and spinal care.',
        'availability': 'Mon - Thu (10:00 AM - 05:00 PM)'
    },
    {
        'doctor_id': 'D103',
        'user_id': 'U103',
        'name': 'Dr. Emily Vance',
        'specialization': 'Pediatrics & Internal Medicine',
        'experience': '15 Years',
        'bio': 'Comprehensive family healthcare, adolescent care, and diagnostic medicine.',
        'availability': 'Tue - Sat (08:00 AM - 03:00 PM)'
    }
]

patients = [
    {
        'patient_id': 'P101',
        'user_id': 'U201',
        'name': 'John Doe',
        'age': 34,
        'gender': 'Male',
        'blood_group': 'O+',
        'medical_history': 'Seasonal allergies, Mild Hypertension (managed with diet).'
    },
    {
        'patient_id': 'P102',
        'user_id': 'U202',
        'name': 'Kusuma Sharma',
        'age': 28,
        'gender': 'Female',
        'blood_group': 'A+',
        'medical_history': 'No prior major surgeries or chronic illnesses.'
    }
]

appointments = [
    {
        'booking_id': 1,
        'appointment_id': 'APP-1001',
        'patient_id': 'P101',
        'patient_name': 'John Doe',
        'doctor_id': 'D101',
        'doctor_name': 'Dr. Sarah Jenkins',
        'specialization': 'Cardiology',
        'date': '2026-10-02',
        'time': '10:30 AM',
        'status': 'Confirmed',
        'reason': 'Annual Cardiac Checkup & ECG Review',
        'booking_time': '2026-09-25 14:30:00'
    },
    {
        'booking_id': 2,
        'appointment_id': 'APP-1002',
        'patient_id': 'P102',
        'patient_name': 'Kusuma Sharma',
        'doctor_id': 'D102',
        'doctor_name': 'Dr. Robert Chen',
        'specialization': 'Neurology',
        'date': '2026-10-05',
        'time': '02:00 PM',
        'status': 'Pending',
        'reason': 'Frequent headache consultation',
        'booking_time': '2026-09-26 09:15:00'
    }
]

diagnoses = [
    {
        'diagnosis_id': 'DIAG-5001',
        'appointment_id': 'APP-1001',
        'patient_id': 'P101',
        'patient_name': 'John Doe',
        'doctor_id': 'D101',
        'doctor_name': 'Dr. Sarah Jenkins',
        'report_title': 'ECG Normal - Baseline Healthy',
        'symptoms': 'Mild chest muscle strain following workout.',
        'findings': 'Heart rhythm within normal limits. Blood pressure 122/80 mmHg.',
        'prescription': 'Lisinopril 5mg daily if BP exceeds 130/85. Hydration and rest.',
        'date': '2026-09-25'
    }
]

notifications = [
    {
        'notification_id': 'NOTIF-9001',
        'user_id': 'U201',
        'user_name': 'John Doe',
        'message': 'Your appointment with Dr. Sarah Jenkins on 2026-10-02 is Confirmed.',
        'type': 'Appointment Confirmation',
        'timestamp': '2026-09-25 14:31:00',
        'read': False
    },
    {
        'notification_id': 'NOTIF-9002',
        'user_id': 'U202',
        'user_name': 'Kusuma Sharma',
        'message': 'Appointment request submitted for Dr. Robert Chen. Awaiting review.',
        'type': 'Booking Request',
        'timestamp': '2026-09-26 09:15:00',
        'read': False
    }
]

user_counter = len(users) + 1
booking_counter = len(appointments) + 1

# ==========================================
# HELPER FUNCTIONS & DECORATORS
# ==========================================

def add_notification(user_id, user_name, message, notif_type='System Alert'):
    notif_id = f"NOTIF-{1000 + len(notifications) + 1}"
    notif = {
        'notification_id': notif_id,
        'user_id': user_id,
        'user_name': user_name,
        'message': message,
        'type': notif_type,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'read': False
    }
    notifications.append(notif)
    print(f"[NOTIFICATION] Real-Time Alert [AWS SNS Simulation]: {notif}")

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                flash('Please log in to continue.', 'warning')
                return redirect(url_for('login'))
            user_role = session['user'].get('role')
            if user_role not in roles:
                flash('Unauthorized access: You do not have permission to view this resource.', 'danger')
                return redirect(url_for('home1'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ==========================================
# CORE ROUTES
# ==========================================

@app.route('/')
def index():
    return render_template('index.html', doctors=doctors, total_doctors=len(doctors), total_patients=len(patients), total_appointments=len(appointments))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        flash(f'Thank you, {name}! Your message regarding "{subject}" has been received. Our support team will get back to you shortly.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# ------------------------------------------
# AUTHENTICATION ROUTES
# ------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = next((u for u in users if u['email'].lower() == email.lower()), None)

        if user and check_password_hash(user['password'], password):
            session['user'] = {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'phone': user.get('phone', '')
            }
            # Mandatory Server Logging from PDF specifications
            print(f"Logged In User Session: {session['user']}")
            print(f"Current Session User Info: {{'email': '{user['email']}', 'id': '{user['id']}', 'name': '{user['name']}'}}")
            
            flash(f"Welcome back, {user['name']}! Logged in as {user['role']}.", 'success')
            return redirect(url_for('home1'))
        else:
            flash('Invalid email address or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global user_counter
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'Patient')
        phone = request.form.get('phone', '').strip()

        if any(u['email'].lower() == email.lower() for u in users):
            flash('Email address is already registered! Please log in.', 'danger')
            return redirect(url_for('signup'))

        hashed_pw = generate_password_hash(password)
        new_user_id = f"U{100 + user_counter}"
        user_counter += 1

        new_user = {
            'id': new_user_id,
            'name': name,
            'email': email,
            'password': hashed_pw,
            'role': role,
            'phone': phone
        }
        users.append(new_user)

        # Create role-specific record
        if role == 'Doctor':
            specialization = request.form.get('specialization', 'General Medicine')
            experience = request.form.get('experience', '1 Year')
            bio = request.form.get('bio', 'Healthcare practitioner dedicated to patient wellbeing.')
            doc_id = f"D{100 + len(doctors) + 1}"
            doctors.append({
                'doctor_id': doc_id,
                'user_id': new_user_id,
                'name': f"Dr. {name}",
                'specialization': specialization,
                'experience': experience,
                'bio': bio,
                'availability': 'Mon - Fri (09:00 AM - 05:00 PM)'
            })
        elif role == 'Patient':
            age = request.form.get('age', 30)
            gender = request.form.get('gender', 'Other')
            blood_group = request.form.get('blood_group', 'Unknown')
            medical_history = request.form.get('medical_history', 'No prior medical history provided.')
            pat_id = f"P{100 + len(patients) + 1}"
            patients.append({
                'patient_id': pat_id,
                'user_id': new_user_id,
                'name': name,
                'age': int(age) if str(age).isdigit() else 30,
                'gender': gender,
                'blood_group': blood_group,
                'medical_history': medical_history
            })

        # Mandatory PDF Proof Logging
        print(f"Current Users List: {users}")
        
        # Trigger welcome notification
        add_notification(new_user_id, name, f"Welcome to MedTrack! Your {role} account has been successfully created.", "Registration")

        flash('Registration successful! Please log in to continue.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    user = session.pop('user', None)
    if user:
        print(f"User {user['name']} logged out.")
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('index'))

# ------------------------------------------
# MAIN DASHBOARD / HOME1 ROUTE
# ------------------------------------------

@app.route('/home1')
@login_required
def home1():
    user = session.get('user')
    print(f"Current Session User Info: {user}")

    role = user.get('role')
    if role == 'Patient':
        return redirect(url_for('patient_dashboard'))
    elif role == 'Doctor':
        return redirect(url_for('doctor_dashboard'))
    elif role == 'Admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('home1.html', user=user)

# ------------------------------------------
# PATIENT PORTAL & BOOKING ROUTES
# ------------------------------------------

@app.route('/patient/dashboard')
@login_required
@role_required(['Patient'])
def patient_dashboard():
    user = session.get('user')
    patient = next((p for p in patients if p['user_id'] == user['id']), None)
    patient_id = patient['patient_id'] if patient else None

    my_appointments = [a for a in appointments if a['patient_id'] == patient_id] if patient_id else []
    my_diagnoses = [d for d in diagnoses if d['patient_id'] == patient_id] if patient_id else []
    my_notifications = [n for n in notifications if n['user_id'] == user['id']]

    return render_template('patient_dashboard.html',
                           user=user,
                           patient=patient,
                           appointments=my_appointments,
                           diagnoses=my_diagnoses,
                           notifications=my_notifications,
                           doctors=doctors)

@app.route('/b1', methods=['GET'])
@app.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def booking_page():
    user = session.get('user')
    
    if request.method == 'GET':
        selected_doc = request.args.get('doctor_id') or request.args.get('movie') # handle b1 fallback args
        selected_doctor_obj = next((d for d in doctors if d['doctor_id'] == selected_doc), None)
        return render_template('book_appointment.html',
                               user=user,
                               doctors=doctors,
                               selected_doctor=selected_doctor_obj)
    
    # POST Request - Processing Booking
    global booking_counter
    try:
        doctor_id = request.form.get('doctor_id')
        doctor_obj = next((d for d in doctors if d['doctor_id'] == doctor_id), None)
        if not doctor_obj:
            flash('Invalid doctor selected.', 'danger')
            return redirect(url_for('booking_page'))

        patient_obj = next((p for p in patients if p['user_id'] == user['id']), None)
        patient_id = patient_obj['patient_id'] if patient_obj else f"P-GUEST-{user['id']}"
        patient_name = user['name']

        app_date = request.form.get('date')
        app_time = request.form.get('time')
        reason = request.form.get('reason', 'General Health Consultation')

        app_id_str = f"APP-{1000 + booking_counter}"

        new_booking = {
            'booking_id': booking_counter,
            'appointment_id': app_id_str,
            'patient_id': patient_id,
            'patient_name': patient_name,
            'doctor_id': doctor_id,
            'doctor_name': doctor_obj['name'],
            'specialization': doctor_obj['specialization'],
            'date': app_date,
            'time': app_time,
            'status': 'Pending',
            'reason': reason,
            'booking_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        appointments.append(new_booking)
        booking_counter += 1

        # PDF Mandatory Server Logs
        print(f"Booking Added: {new_booking}")
        print(f"All Bookings: {appointments}")

        # Real-time SNS Notification trigger
        add_notification(user['id'], user['name'], f"Appointment request {app_id_str} sent to {doctor_obj['name']} for {app_date} at {app_time}.", "Booking Request")
        add_notification(doctor_obj['user_id'], doctor_obj['name'], f"New appointment request from {patient_name} on {app_date}.", "Doctor Alert")

        flash(f'Appointment request submitted successfully! Booking ID: {app_id_str}', 'success')
        return redirect(url_for('view_appointments'))

    except Exception as e:
        print(f"Error processing booking: {e}")
        flash(f'Error processing booking: {e}', 'danger')
        return redirect(url_for('home1'))

@app.route('/tickets')
@app.route('/appointments')
@login_required
def view_appointments():
    user = session.get('user')
    role = user.get('role')

    if role == 'Patient':
        patient_obj = next((p for p in patients if p['user_id'] == user['id']), None)
        patient_id = patient_obj['patient_id'] if patient_obj else None
        user_appointments = [a for a in appointments if a['patient_id'] == patient_id]
    elif role == 'Doctor':
        doctor_obj = next((d for d in doctors if d['user_id'] == user['id']), None)
        doctor_id = doctor_obj['doctor_id'] if doctor_obj else None
        user_appointments = [a for a in appointments if a['doctor_id'] == doctor_id]
    else: # Admin sees all
        user_appointments = appointments

    return render_template('appointments.html', appointments=user_appointments, user=user)

@app.route('/appointment/update_status/<int:booking_id>', methods=['POST'])
@login_required
@role_required(['Doctor', 'Admin'])
def update_appointment_status(booking_id):
    new_status = request.form.get('status')
    booking = next((a for a in appointments if a['booking_id'] == booking_id), None)
    
    if booking:
        booking['status'] = new_status
        flash(f"Appointment {booking['appointment_id']} status updated to {new_status}.", 'success')
        
        # Find patient user_id
        patient_obj = next((p for p in patients if p['patient_id'] == booking['patient_id']), None)
        if patient_obj:
            add_notification(patient_obj['user_id'], patient_obj['name'],
                             f"Your appointment ({booking['appointment_id']}) with {booking['doctor_name']} is now {new_status}.",
                             "Status Update")

        print(f"Status Updated: Appointment {booking['appointment_id']} -> {new_status}")
    else:
        flash("Appointment record not found.", "danger")

    return redirect(url_for('view_appointments'))

# ------------------------------------------
# DOCTOR PORTAL & DIAGNOSIS ROUTES
# ------------------------------------------

@app.route('/doctor/dashboard')
@login_required
@role_required(['Doctor', 'Admin'])
def doctor_dashboard():
    user = session.get('user')
    doctor_obj = next((d for d in doctors if d['user_id'] == user['id']), None)
    doc_id = doctor_obj['doctor_id'] if doctor_obj else None

    doc_appointments = [a for a in appointments if a['doctor_id'] == doc_id] if doc_id else appointments
    doc_diagnoses = [dg for dg in diagnoses if dg['doctor_id'] == doc_id] if doc_id else diagnoses
    doc_notifications = [n for n in notifications if n['user_id'] == user['id']]

    return render_template('doctor_dashboard.html',
                           user=user,
                           doctor=doctor_obj,
                           appointments=doc_appointments,
                           diagnoses=doc_diagnoses,
                           notifications=doc_notifications,
                           patients=patients)

@app.route('/submit_diagnosis', methods=['GET', 'POST'])
@login_required
@role_required(['Doctor', 'Admin'])
def submit_diagnosis():
    user = session.get('user')
    doctor_obj = next((d for d in doctors if d['user_id'] == user['id']), None)

    if request.method == 'POST':
        appointment_id = request.form.get('appointment_id')
        app_obj = next((a for a in appointments if a['appointment_id'] == appointment_id), None)

        if not app_obj:
            flash("Appointment record not found.", "danger")
            return redirect(url_for('submit_diagnosis'))

        report_title = request.form.get('report_title', 'Clinical Diagnosis Report')
        symptoms = request.form.get('symptoms', '')
        findings = request.form.get('findings', '')
        prescription = request.form.get('prescription', '')

        diag_id = f"DIAG-{5000 + len(diagnoses) + 1}"
        new_diag = {
            'diagnosis_id': diag_id,
            'appointment_id': appointment_id,
            'patient_id': app_obj['patient_id'],
            'patient_name': app_obj['patient_name'],
            'doctor_id': doctor_obj['doctor_id'] if doctor_obj else app_obj['doctor_id'],
            'doctor_name': doctor_obj['name'] if doctor_obj else app_obj['doctor_name'],
            'report_title': report_title,
            'symptoms': symptoms,
            'findings': findings,
            'prescription': prescription,
            'date': datetime.now().strftime("%Y-%m-%d")
        }

        diagnoses.append(new_diag)
        app_obj['status'] = 'Completed'

        # Notify Patient
        patient_obj = next((p for p in patients if p['patient_id'] == app_obj['patient_id']), None)
        if patient_obj:
            add_notification(patient_obj['user_id'], patient_obj['name'],
                             f"New diagnosis report ({diag_id}) published by {new_diag['doctor_name']}.",
                             "Medical Report")

        print(f"Diagnosis Submitted: {new_diag}")
        flash(f"Diagnosis report {diag_id} submitted successfully and appointment marked as Completed!", "success")
        return redirect(url_for('medical_history'))

    # GET Request
    target_app_id = request.args.get('appointment_id')
    doc_id = doctor_obj['doctor_id'] if doctor_obj else None
    eligible_apps = [a for a in appointments if (not doc_id or a['doctor_id'] == doc_id) and a['status'] in ['Confirmed', 'Pending']]

    return render_template('submit_diagnosis.html',
                           user=user,
                           doctor=doctor_obj,
                           eligible_appointments=eligible_apps,
                           target_app_id=target_app_id)

@app.route('/medical_history')
@login_required
def medical_history():
    user = session.get('user')
    role = user.get('role')

    if role == 'Patient':
        patient_obj = next((p for p in patients if p['user_id'] == user['id']), None)
        patient_id = patient_obj['patient_id'] if patient_obj else None
        view_diagnoses = [d for d in diagnoses if d['patient_id'] == patient_id]
        patient_record = patient_obj
    elif role == 'Doctor':
        doctor_obj = next((d for d in doctors if d['user_id'] == user['id']), None)
        doc_id = doctor_obj['doctor_id'] if doctor_obj else None
        view_diagnoses = [d for d in diagnoses if d['doctor_id'] == doc_id]
        patient_record = None
    else: # Admin sees all
        view_diagnoses = diagnoses
        patient_record = None

    return render_template('medical_history.html',
                           user=user,
                           diagnoses=view_diagnoses,
                           patient=patient_record,
                           all_patients=patients)

# ------------------------------------------
# ADMIN PORTAL ROUTE
# ------------------------------------------

@app.route('/admin/dashboard')
@login_required
@role_required(['Admin'])
def admin_dashboard():
    user = session.get('user')
    return render_template('admin_dashboard.html',
                           user=user,
                           users=users,
                           doctors=doctors,
                           patients=patients,
                           appointments=appointments,
                           diagnoses=diagnoses,
                           notifications=notifications)

# ------------------------------------------
# NOTIFICATIONS & DEBUG API ROUTES
# ------------------------------------------

@app.route('/notifications')
@login_required
def view_user_notifications():
    user = session.get('user')
    user_notifs = [n for n in notifications if n['user_id'] == user['id']]
    # Mark as read
    for n in user_notifs:
        n['read'] = True
    return render_template('notifications.html', notifications=user_notifs, user=user)

@app.route('/api/debug/state')
def debug_state():
    """Returns full JSON state of local dataset for verification."""
    return jsonify({
        'users_count': len(users),
        'doctors_count': len(doctors),
        'patients_count': len(patients),
        'appointments_count': len(appointments),
        'diagnoses_count': len(diagnoses),
        'notifications_count': len(notifications),
        'users': users,
        'appointments': appointments,
        'diagnoses': diagnoses,
        'notifications': notifications
    })

# ==========================================
# APP EXECUTION
# ==========================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f"MedTrack Cloud Healthcare System Starting on http://127.0.0.1:{port} (Local Phase)...")
    app.run(host='127.0.0.1', port=port, debug=True)

