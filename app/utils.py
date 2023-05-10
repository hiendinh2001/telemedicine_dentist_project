import json, os
from app import app, db
from app.models import User, UserRole, Patient, Immunization
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib

def read_json(path): 
    with open(path, "r") as f:
        return json.load(f)

def load_patient(name=None, gender=None):
    patients = Patient.query.filter(Patient.active.__eq__(True))

    if name:
        patients = patients.filter(Patient.name.contains(name))

    if gender:
        patients = patients.filter(Patient.gender.contains(gender))

    return patients

def load_immunization():
    immunizations = read_json(os.path.join(app.root_path, 'data/immunization.json'))

    return immunizations

def load_observation():
    observations = read_json(os.path.join(app.root_path, 'data/observation.json'))

    return observations

def load_practitioner():
    practitioners = read_json(os.path.join(app.root_path, 'data/practitioner.json'))

    return practitioners

def get_patient_by_id(patient_id):
    return Patient.query.get(patient_id)

def get_immunization_by_id(immunization_id): 
    immunizations = read_json(os.path.join(app.root_path, 'data/immunization.json'))

    for i in immunizations:
        if i['identifier'] == immunization_id:
            return i

def get_observation_by_id(observation_id): 
    observations = read_json(os.path.join(app.root_path, 'data/observation.json'))

    for o in observations:
        if o['identifier'] == observation_id:
            return o

def get_practitioner_by_id(practionner_id):
    practitioners = read_json(os.path.join(app.root_path, 'data/practitioner.json'))

    for pr in practitioners:
        if pr['identifier'] == practionner_id:
            return pr

def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))
    db.session.add(user)
    db.session.commit()

def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                                User.user_role.__eq__(role)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)