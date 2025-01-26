from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import auth, firestore, exceptions as firebase_exceptions
from .firebase import initialize_firebase
from datetime import datetime

# Initialize Firebase
initialize_firebase()


def register_view(request):
    """
    Handles user registration using Firebase Authentication and stores user data in Firestore.
    """
    if request.method == 'POST':
        username = request.POST.get('username')  # Email
        password = request.POST.get('password')
        role = request.POST.get('role')  # Admin or Doctor

        if not username or not password or not role:
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html')

        try:
            # Create user in Firebase Authentication
            user = auth.create_user(
                email=username,
                password=password,
                email_verified=False
            )

            # Set custom claims for the user role
            auth.set_custom_user_claims(user.uid, {'role': role})

            # Store user data in Firestore
            db = firestore.client()
            user_data = {
                'email': username,
                'role': role,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Add a timestamp
            }
            db.collection('users').document(user.uid).set(user_data)

            print(f'Successfully created new user: {user.uid} with role: {role}')
            messages.success(request, "User created successfully! Please log in.")
            return redirect('login')

        except firebase_exceptions.FirebaseError as e:
            error_message = f"Firebase error: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Email
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Email and password are required.")
            return render(request, 'login.html')

        try:
            # Authenticate user using Firebase
            user = auth.get_user_by_email(username)
            if user:
                # Store Firebase user UID in the session
                request.session['firebase_user_uid'] = user.uid
                request.session['firebase_user_email'] = user.email

                # Redirect based on role
                role = user.custom_claims.get('role', '')
                if role == 'Admin':
                    return redirect('admin_dashboard')
                elif role == 'Doctor':
                    return redirect('doctor_dashboard')
                else:
                    messages.error(request, "Invalid role.")
            else:
                messages.error(request, "Invalid email or password.")

        except firebase_exceptions.FirebaseError as e:
            error_message = f"Firebase error: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

    return render(request, 'login.html')

def logout_view(request):
    # Clear Firebase user data from the session
    if 'firebase_user_uid' in request.session:
        del request.session['firebase_user_uid']
    if 'firebase_user_email' in request.session:
        del request.session['firebase_user_email']
    messages.success(request, "You have been logged out.")
    return redirect('login')


def dashboard_view(request):
    """
    A generic dashboard view that redirects based on the user's role.
    """
    try:
        user = auth.get_user(request.user.uid)  # Get Firebase user
        role = user.custom_claims.get('role', '')
        if role == 'Admin':
            return redirect('admin_dashboard')
        elif role == 'Doctor':
            return redirect('doctor_dashboard')
        else:
            messages.error(request, "Invalid role.")
            return redirect('login')

    except firebase_exceptions.FirebaseError as e:
        error_message = f"Firebase error: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return redirect('login')

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return redirect('login')

def admin_dashboard(request):
    try:
        # Get Firebase user UID from the session
        firebase_user_uid = request.session.get('firebase_user_uid')
        if not firebase_user_uid:
            messages.error(request, "You are not logged in.")
            return redirect('login')

        # Fetch user data from Firebase
        user = auth.get_user(firebase_user_uid)
        role = user.custom_claims.get('role', '')
        if role != 'Admin':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('login')

        # Fetch data for the admin dashboard (e.g., total patients, appointments)
        from firebase_admin import firestore
        db = firestore.client()
        patients = db.collection('patients').stream()
        total_patients = len(list(patients))

        return render(request, 'admin_dashboard.html', {
            'total_patients': total_patients,
        })

    except firebase_exceptions.FirebaseError as e:
        error_message = f"Firebase error: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return redirect('login')

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return redirect('login')




def doctor_dashboard(request):
    try:
        # Get Firebase user UID from the session
        firebase_user_uid = request.session.get('firebase_user_uid')
        if not firebase_user_uid:
            messages.error(request, "You are not logged in.")
            return redirect('login')

        # Fetch user data from Firebase
        user = auth.get_user(firebase_user_uid)
        role = user.custom_claims.get('role', '')
        if role != 'Doctor':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('login')

        # Fetch data for the doctor dashboard (e.g., today's appointments)
        from firebase_admin import firestore
        from datetime import datetime
        db = firestore.client()
        today = datetime.now().date()

        # Fetch appointments for the logged-in doctor
        appointments = db.collection('appointments').where('doctor_id', '==', firebase_user_uid).stream()

        # Fetch patient details for each appointment
        today_appointments = []
        for appointment in appointments:
            appointment_data = appointment.to_dict()
            appointment_time_str = appointment_data.get('appointment_time')

            # Debug: Print appointment data
            print(f"Appointment Data: {appointment_data}")

            # Convert appointment_time to datetime object
            try:
                appointment_time = datetime.strptime(appointment_time_str, '%Y-%m-%dT%H:%M')
            except (ValueError, TypeError) as e:
                print(f"Error parsing appointment_time: {e}")
                continue

            # Check if the appointment is for today
            if appointment_time.date() == today:
                # Fetch patient details using patient_id
                patient_id = appointment_data.get('patient_id')
                if patient_id:
                    patient_ref = db.collection('patients').document(patient_id)
                    patient_data = patient_ref.get().to_dict()
                    if patient_data:
                        appointment_data['patient_name'] = patient_data.get('name', 'N/A')
                        appointment_data['patient_contact'] = patient_data.get('contact', 'N/A')
                    else:
                        appointment_data['patient_name'] = 'N/A'
                        appointment_data['patient_contact'] = 'N/A'
                else:
                    appointment_data['patient_name'] = 'N/A'
                    appointment_data['patient_contact'] = 'N/A'

                # Add formatted appointment_time to the data
                appointment_data['appointment_time'] = appointment_time.strftime('%B %d, %Y, %I:%M %p')
                today_appointments.append(appointment_data)

        # Debug: Print today's appointments
        print(f"Today's appointments: {today_appointments}")

        return render(request, 'doctor_dashboard.html', {
            'today_appointments': today_appointments,
        })

    except firebase_exceptions.FirebaseError as e:
        error_message = f"Firebase error: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return redirect('login')

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return redirect('login')