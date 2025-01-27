
# Hospital Management System  

The **Hospital Management System** is a web application built using **Django** and **Firebase**. It allows admins and doctors to manage patients, schedule appointments, and view dashboards with relevant information. Firebase is used for authentication and as the database.  

---

## Features  

- **User Authentication**:  
  - Admins and doctors can register and log in using Firebase Authentication.  
  - Role-based access control (Admin and Doctor roles).  

- **Patient Management**:  
  - Admins can add, view, edit, and delete patient records.  
  - Patient details include name, age, gender, contact information, and medical history.  

- **Appointment Scheduling**:  
  - Admins can schedule appointments for patients with doctors.  
  - Doctors can view their appointments for the day.  

- **Dashboards**:  
  - **Admin Dashboard**: Displays total patients and upcoming appointments.  
  - **Doctor Dashboard**: Displays today's appointments.  

---

## Technologies Used  

- **Backend**: Django (Python)  
- **Database**: Firebase Firestore  
- **Authentication**: Firebase Authentication  
- **Frontend**: HTML, CSS, JavaScript  
- **Styling**: Custom CSS  

---

## Workflow Block Diagram


```mermaid
graph TD
    A[Start] --> B[User Authentication]
    B -->|Login| C[Dashboard]
    B -->|Register| D[Create User]
    C -->|Admin| E[Admin Dashboard]
    C -->|Doctor| F[Doctor Dashboard]
    C -->|Patient| G[Patient Dashboard]

    %% Admin Actions
    E --> H[Manage Users]
    E --> I[View Appointments]
    E --> J[Generate Reports]

    %% Doctor Actions
    F --> K[View Assigned Patients]
    F --> L[Manage Appointments]

    %% Patient Actions
    G --> M[View Appointments]
    G --> N[Add Medical History]

    %% Patients Module
    H -->|Add/Edit| O[Add Patient]
    H -->|View/Delete| P[View Patients]

    %% Appointments Module
    I -->|Add/Edit| Q[Add Appointment]
    I -->|View/Delete| R[View Appointments]

    %% Database Interaction
    O --> S[Firestore: Patients Collection]
    P --> S
    Q --> T[Firestore: Appointments Collection]
    R --> T

    %% Error Handling and Redirects
    S --> U[Error Handling: Firebase Exceptions]
    T --> U
    U -->|Log & Redirect| C
    U -->|Log & Redirect| B

    %% End Process
    J --> V[End]
    L --> V
    M --> V
    N --> V

```

## Setup Instructions  

### Prerequisites  

1. **Python**: Ensure Python 3.8 or higher is installed.  
2. **Firebase Project**: Create a Firebase project and enable Firestore and Authentication.  
3. **Firebase Admin SDK**:  
   - Go to the Firebase Console: [Firebase Console](https://console.firebase.google.com/)  
   - Select your project.  
   - Navigate to **Project Settings** > **Service Accounts** > **Generate New Private Key**.  
   - Download the generated `json` file and rename it to **firebase-adminsdk.json**.  

---

### Installation  

1. **Clone the Repository**:  
   ```bash  
   git clone https://github.com/sinup69/collage-project.git  
   cd hospital-management-system  
   ```  

2. **Set Up a Virtual Environment**:  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate  
   ```  

3. **Install Dependencies**:  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. **Re-add the Firebase Admin SDK File**:  
   - Place the downloaded `firebase-adminsdk.json` file in the `accounts` directory.  

5. **Update Firebase Configuration**:  
   - Ensure the Firebase initialization code in `accounts/firebase.py` points to the correct path for `firebase-adminsdk.json`.  

6. **Run Migrations**:  
   ```bash  
   python manage.py migrate  
   ```  

7. **Run the Development Server**:  
   ```bash  
   python manage.py runserver  
   ```  

8. **Access the Application**:  
   - Open your browser and go to `http://127.0.0.1:8000/`.  

---

## Contribution Guide  

We welcome contributions to the **Hospital Management System**! Here’s how you can contribute:  

### 1. **Fork the Repository**  
   - Fork the repository to your GitHub account.  

### 2. **Clone the Repository**  
   ```bash  
   git clone https://github.com/sinup69/collage-project.git  
   cd hospital-management-system  
   ```  

### 3. **Set Up the Development Environment**  
   - Follow the [Setup Instructions](#setup-instructions) to set up the project locally.  

### 4. **Create a New Branch**  
   ```bash  
   git checkout -b feature/your-feature-name  
   ```  

### 5. **Make Your Changes**  
   - Implement your changes or fixes.  
   - Ensure your code follows the project's coding standards.  

### 6. **Test Your Changes**  
   - Run the development server and test your changes thoroughly.  
   ```bash  
   python manage.py runserver  
   ```  

### 7. **Commit Your Changes**  
   ```bash  
   git add .  
   git commit -m "Add your commit message here"  
   ```  

### 8. **Push Your Changes**  
   ```bash  
   git push origin feature/your-feature-name  
   ```  

### 9. **Create a Pull Request**  
   - Go to the original repository and create a pull request (PR).  
   - Provide a clear description of your changes and their purpose.  

### 10. **Code Review**  
   - Your PR will be reviewed by the maintainers. Address any feedback or requested changes.  

---

## Code of Conduct  

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing to ensure a welcoming and inclusive environment for all contributors.  

---

## License  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  

---

## Contact  

For questions or feedback, leave a comment ☺️  

---  

Thank you for your interest in the **Hospital Management System**! We look forward to your contributions. 🚀  


