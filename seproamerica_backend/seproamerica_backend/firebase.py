import firebase_admin
from firebase_admin import credentials
import os

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
service_account_file = os.path.join(SETTINGS_DIR, 'seproamericaServiceAccountKey.json')
cred = credentials.Certificate(service_account_file)
firebase_admin.initialize_app(cred)
