import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-config.json")

firebase_app = firebase_admin.initialize_app(cred)