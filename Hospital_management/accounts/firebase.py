# accounts/firebase_config.py
import firebase_admin
from firebase_admin import credentials
import os

def initialize_firebase():
    # Get the relative path to the firebase credentials file
    cred_path = os.path.join(os.path.dirname(__file__), 'firebase-adminsdk.json')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
