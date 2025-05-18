import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(os.path.dirname(current_dir), "firebase-config.json")
cred = credentials.Certificate(config_path)

firebase_app = firebase_admin.initialize_app(cred)