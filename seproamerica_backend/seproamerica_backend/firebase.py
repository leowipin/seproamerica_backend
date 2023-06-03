import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('seproamerica_backend/seproamericaServiceAccountKey.json')
firebase_admin.initialize_app(cred)
