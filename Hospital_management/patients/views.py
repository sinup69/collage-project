from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import firestore, exceptions as firebase_exceptions

from datetime import datetime

db = firestore.client()

def add_patient(request):
    """
    Handles adding a new patient to the Firestore database.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        contact = request.POST.get('contact')
        medical_history = request.POST.get('medical_history')

        # Validate required fields
        if not name or not age or not gender or not contact:
            messages.error(request, "All fields are required except Medical History.")
            return render(request, 'add_patient.html')

        try:
            # Create patient data dictionary
            patient_data = {
                'name': name,
                'age': int(age),  # Convert age to integer
                'gender': gender,
                'contact': contact,
                'medical_history': medical_history if medical_history else "None"
            }

            # Add patient to Firestore
            db.collection('patients').add(patient_data)
            messages.success(request, "Patient added successfully!")
            return redirect('view_patients')

        except ValueError:
            messages.error(request, "Age must be a valid number.")
            return render(request, 'add_patient.html')

        except firebase_exceptions.FirebaseError as e:
            error_message = f"Firebase error: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

    return render(request, 'add_patient.html')


def view_patients(request):
    """
    Fetches and displays all patients from the Firestore database.
    """
    try:
        # Fetch all patients from Firestore
        patients = db.collection('patients').stream()
        patient_list = [{'id': patient.id, **patient.to_dict()} for patient in patients]
        return render(request, 'view_patients.html', {'patients': patient_list})

    except firebase_exceptions.FirebaseError as e:
        error_message = f"Firebase error: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return render(request, 'view_patients.html', {'patients': []})

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return render(request, 'view_patients.html', {'patients': []})


def edit_patient(request, patient_id):
    """
    Handles editing an existing patient's details in the Firestore database.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        contact = request.POST.get('contact')
        medical_history = request.POST.get('medical_history')

        # Validate required fields
        if not name or not age or not gender or not contact:
            messages.error(request, "All fields are required except Medical History.")
            return render(request, 'edit_patient.html', {'patient_id': patient_id})

        try:
            # Update patient data in Firestore
            patient_ref = db.collection('patients').document(patient_id)
            patient_ref.update({
                'name': name,
                'age': int(age),  # Convert age to integer
                'gender': gender,
                'contact': contact,
                'medical_history': medical_history if medical_history else "None"
            })
            messages.success(request, "Patient updated successfully!")
            return redirect('view_patients')

        except ValueError:
            messages.error(request, "Age must be a valid number.")
            return render(request, 'edit_patient.html', {'patient_id': patient_id})

        except firebase_exceptions.FirebaseError as e:
            error_message = f"Firebase error: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

    try:
        # Fetch patient data for pre-filling the form
        patient_ref = db.collection('patients').document(patient_id)
        patient_data = patient_ref.get().to_dict()
        return render(request, 'edit_patient.html', {'patient': patient_data, 'patient_id': patient_id})

    except firebase_exceptions.FirebaseError as e:
        error_message = f"Firebase error: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return redirect('view_patients')

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return redirect('view_patients')


def delete_patient(request, patient_id):
    """
    Handles deleting a patient from the Firestore database.
    """
    try:
        # Delete patient from Firestore
        db.collection('patients').document(patient_id).delete()
        messages.success(request, "Patient deleted successfully!")
    except firebase_exceptions.FirebaseError as e:
        error_message = f"Firebase error: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        messages.error(request, error_message)

    return redirect('view_patients')

from datetime import datetime


def add_appointment(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        appointment_time = request.POST.get('appointment_time')

        if not patient_id or not doctor_id or not appointment_time:
            messages.error(request, "All fields are required.")
            return render(request, 'add_appointment.html')

        try:
            # Convert appointment_time to a datetime object
            from datetime import datetime
            appointment_time = datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M')

            # Create appointment data
            appointment_data = {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'appointment_time': appointment_time.strftime('%Y-%m-%dT%H:%M'),  # Store as string
                'status': 'Scheduled'
            }

            # Add appointment to Firestore
            db.collection('appointments').add(appointment_data)
            messages.success(request, "Appointment scheduled successfully!")
            return redirect('view_appointments')

        except ValueError as e:
            messages.error(request, f"Invalid appointment time format: {e}")
            return render(request, 'add_appointment.html')

        except firebase_exceptions.FirebaseError as e:
            error_message = f"Firebase error: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

    # Fetch the list of patients and doctors for the dropdowns
    try:
        # Fetch patients
        patients = db.collection('patients').stream()
        patient_list = [{'id': patient.id, **patient.to_dict()} for patient in patients]

        # Fetch doctors (users with role 'Doctor')
        doctors = db.collection('users').where('role', '==', 'Doctor').stream()
        doctor_list = [{'id': doctor.id, **doctor.to_dict()} for doctor in doctors]

        # Debug: Print the list of doctors
        print(f"Doctors: {doctor_list}")

    except Exception as e:
        print(f"Error fetching data: {e}")
        patient_list = []
        doctor_list = []

    return render(request, 'add_appointment.html', {
        'patients': patient_list,
        'doctors': doctor_list,
    })


def view_appointments(request):
    """
    Fetches and displays all appointments from the Firestore database.
    """
    try:
        # Fetch all appointments from Firestore
        appointments = db.collection('appointments').stream()
        appointment_list = [{'id': appointment.id, **appointment.to_dict()} for appointment in appointments]
        print(appointment_list)
        return render(request, 'view_appointments.html', {'appointments': appointment_list})

    except firebase_exceptions.FirebaseError as e:
        error_message = f"Firebase error: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return render(request, 'view_appointments.html', {'appointments': []})

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return render(request, 'view_appointments.html', {'appointments': []})
    


def edit_appointment(request, appointment_id):
    """
    Handles editing an existing appointment in Firestore.
    """
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        appointment_time = request.POST.get('appointment_time')
        status = request.POST.get('status')

        # Validate required fields
        if not patient_id or not doctor_id or not appointment_time or not status:
            messages.error(request, "All fields are required.")
            return render(request, 'edit_appointment.html', {'appointment_id': appointment_id})

        try:
            # Update appointment data in Firestore
            appointment_ref = db.collection('appointments').document(appointment_id)
            appointment_ref.update({
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'appointment_time': appointment_time,
                'status': status
            })
            messages.success(request, "Appointment updated successfully!")
            return redirect('view_appointments')

        except firebase_exceptions.FirebaseError as e:
            error_message = f"Firebase error: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(error_message)
            messages.error(request, error_message)

    try:
        # Fetch appointment data for pre-filling the form
        appointment_ref = db.collection('appointments').document(appointment_id)
        appointment_data = appointment_ref.get().to_dict()
        return render(request, 'edit_appointment.html', {'appointment': appointment_data, 'appointment_id': appointment_id})

    except firebase_exceptions.FirebaseError as e:
        error_message = f"Firebase error: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return redirect('view_appointments')

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
        return redirect('view_appointments')
    



def delete_appointment(request, appointment_id):
    """
    Handles deleting an existing appointment from Firestore.
    """
    try:
        # Delete the appointment from Firestore
        db.collection('appointments').document(appointment_id).delete()
        messages.success(request, "Appointment deleted successfully!")
    except firebase_exceptions.FirebaseError as e:
        error_message = f"Firebase error: {str(e)}"
        print(error_message)
        messages.error(request, error_message)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        messages.error(request, error_message)

    # Redirect to the view_appointments page
    return redirect('view_appointments')