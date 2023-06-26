import json, os
from app import app, db
from app.models import User, UserRole, Patient, Immunization, Observation, Practitioner
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib
import csv

def read_json(path): 
    with open(path, "r") as f:
        return json.load(f)

def load_patient(immunization_id=None, practitioner_id=None, observation_id=None, name=None, gender=None):
    patients = Patient.query.filter(Patient.active.__eq__(True))

    if immunization_id:
        patients = patients.filter(Patient.service_id.__eq__(immunization_id))

    if practitioner_id:
        patients = patients.filter(Patient.status_id.__eq__(practitioner_id))

    if observation_id:
        patients = patients.filter(Patient.status_id.__eq__(observation_id))

    if name:
        patients = patients.filter(Patient.name.contains(name))

    if gender:
        patients = patients.filter(Patient.gender.contains(gender))

    return patients

def load_immunization():
    return Immunization.query.all()

def load_observation():
    return Observation.query.all()

def load_practitioner():
    return Practitioner.query.all()

def get_patient_by_id(patient_id):
    return Patient.query.get(patient_id)

def get_immunization_by_id(immunization_id): 
    return Immunization.query.get(immunization_id)

def get_observation_by_id(observation_id): 
    return Observation.query.get(observation_id)

def get_practitioner_by_id(practionner_id):
    return Practitioner.query.get(practionner_id)

def add_user(name, username, password, email, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=email.strip(),
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

def add_patient(namePatient, genderPatient, birthDatePatient, addressPatient, statusVaccine, vaccineCode, occurrenceDateTime, statusObservation, effectiveDateTime, value, unit, namePractitioner, genderPractitioner, birthDatePractitioner, addressPractitioner, language, **kwargs):

    immunization = Immunization(status=statusVaccine.strip(),
                                vaccineCode=vaccineCode.strip(),
                                occurrenceDateTime=occurrenceDateTime)

    db.session.add(immunization)
    db.session.commit()

    observation = Observation(status=statusObservation.strip(),
                              effectiveDateTime=effectiveDateTime,
                              value=value.strip(),
                              unit=unit.strip())
    db.session.add(observation)
    db.session.commit()

    practitioner = Practitioner(name=namePractitioner.strip(),
                                gender=genderPractitioner.strip(),
                                birthDate=birthDatePractitioner,
                                address=addressPractitioner.strip(),
                                language=language.strip())

    db.session.add(practitioner)
    db.session.commit()

    patient = Patient(name=namePatient.strip(),
                      gender=genderPatient,
                      birthDate=birthDatePatient,
                      address=addressPatient.strip(),
                      immunization_id=immunization.id,
                      observation_id=observation.id,
                      practitioner_id=practitioner.id)
    db.session.add(patient)
    db.session.commit()