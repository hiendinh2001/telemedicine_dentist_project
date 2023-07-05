import json
import os
from app import app, db
from app.models import User, UserRole, Patient, Immunization, Observation, Practitioner, Appointment
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib
import csv
from datetime import datetime
from collections import OrderedDict


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_patient(immunization_id=None, practitioner_id=None, observation_id=None, name=None, gender=None):
    patients = Patient.query.filter(Patient.active.__eq__(True))

    if immunization_id:
        patients = patients.filter(
            Patient.immunization_id.__eq__(immunization_id))

    if practitioner_id:
        patients = patients.filter(
            Patient.practitioner_id.__eq__(practitioner_id))

    if observation_id:
        patients = patients.filter(
            Patient.observation_id.__eq__(observation_id))

    if name:
        patients = patients.filter(Patient.name.contains(name))

    if gender:
        patients = patients.filter(Patient.gender == gender)

    return patients


def load_user():
    return User.query.all()


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


def get_practitioner_by_id(practitioner_id):
    return Practitioner.query.get(practitioner_id)


def add_user_doctor(name, username, password, email, genderPractitioner, birthDatePractitioner, 
                    addressPractitioner, language, position, **kwargs):
    practitioner = Practitioner(name=name.strip(),
                                gender=genderPractitioner,
                                birthDate=birthDatePractitioner,
                                address=addressPractitioner.strip(),
                                email=email.strip(),
                                language=language.strip(),
                                position=position.strip())

    db.session.add(practitioner)
    db.session.commit()

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=email.strip(),
                avatar=kwargs.get('avatar'),
                user_role=UserRole.DOCTOR,
                practitioner_id=practitioner.id)
    db.session.add(user)
    db.session.commit()


def add_user(name, username, password, email, genderPatient, birthDatePatient, addressPatient, 
             statusVaccine, vaccineCode, occurrenceDateTime, statusObservation, effectiveDateTime, value, unit, **kwargs):
    immunization = Immunization(status=None if not statusVaccine else statusVaccine,
                                vaccineCode=None if not vaccineCode else vaccineCode,
                                occurrenceDateTime=None if not occurrenceDateTime else occurrenceDateTime)

    db.session.add(immunization)
    db.session.commit()

    observation = Observation(status=None if not statusObservation else statusObservation,
                              effectiveDateTime=None if not effectiveDateTime else effectiveDateTime,
                              value=None if not value else value,
                              unit=None if not unit else unit)
    db.session.add(observation)
    db.session.commit()

    patient = Patient(name=name.strip(),
                      gender=genderPatient,
                      birthDate=birthDatePatient,
                      address=addressPatient.strip(),
                      email=email.strip(),
                      immunization_id=immunization.id,
                      observation_id=observation.id)

    db.session.add(patient)
    db.session.commit()

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=email.strip(),
                avatar=kwargs.get('avatar'),
                patient_id=patient.id)
    db.session.add(user)
    db.session.commit()


def check_login(username, password, role=UserRole.PATIENT):
    if username and password:
        password = str(hashlib.md5(
            password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 (User.user_role.__eq__(role) | User.user_role.__eq__(UserRole.DOCTOR))).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_patient(namePatient, genderPatient, birthDatePatient, addressPatient, emailPatient, 
                statusVaccine, vaccineCode, occurrenceDateTime, statusObservation, effectiveDateTime, 
                value, unit, practitioner_id):

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

    patient = Patient(name=namePatient.strip(),
                      gender=genderPatient,
                      birthDate=birthDatePatient,
                      address=addressPatient.strip(),
                      email=emailPatient.strip(),
                      immunization_id=immunization.id,
                      observation_id=observation.id,
                      practitioner_id=int(practitioner_id))
    db.session.add(patient)
    db.session.commit()


def update_patient_info(patient_id, namePatient, genderPatient, birthDatePatient, addressPatient, emailPatient, practitioner_id):
    info = db.session.query(Patient).get(patient_id)
    if info:
        info.name = namePatient.strip()
        info.gender = genderPatient
        info.birthDate = birthDatePatient
        info.address = addressPatient.strip()
        info.email = emailPatient.strip()
        info.practitioner_id = int(practitioner_id)

        db.session.commit()


def update_patient_immunization(immunization_id, statusVaccine, vaccineCode, occurrenceDateTime):
    immunization = db.session.query(Immunization).get(immunization_id)
    if immunization:
        immunization.status = statusVaccine.strip()
        immunization.vaccineCode = vaccineCode.strip()
        immunization.occurrenceDateTime = occurrenceDateTime

        db.session.commit()


def update_patient_observation(observation_id, statusObservation, effectiveDateTime, value, unit):
    observation = db.session.query(Observation).get(observation_id)
    if observation:
        observation.status = statusObservation.strip()
        observation.effectiveDateTime = effectiveDateTime
        observation.value = value.strip()
        observation.unit = unit

        db.session.commit()


def update_patient_practitioner(practitioner_id, namePractitioner, genderPractitioner, birthDatePractitioner, addressPractitioner, language):
    practitioner = db.session.query(Practitioner).get(practitioner_id)
    if practitioner:
        practitioner.name = namePractitioner.strip()
        practitioner.gender = genderPractitioner
        practitioner.birthDate = birthDatePractitioner
        practitioner.address = addressPractitioner.strip()
        practitioner.language = language.strip()

        db.session.commit()


def delete_patient(patient_id):
    patient = db.session.query(Patient).get(patient_id)
    if patient:
        immunization = db.session.query(Immunization).filter_by(
            id=patient.immunization_id).first()
        observation = db.session.query(Observation).filter_by(
            id=patient.observation_id).first()

        if immunization:
            db.session.delete(immunization)
        if observation:
            db.session.delete(observation)

        db.session.delete(patient)
        db.session.commit()


def load_appointment(practitioner_id=None, patient_id=None, user_id=None, from_date=None, to_date=None, appointmentType=None, reason=None):
    appointments = Appointment.query.filter(Appointment.active.__eq__(True))

    if practitioner_id:
        appointments = appointments.filter(
            Appointment.practitioner_id.__eq__(practitioner_id))

    if patient_id:
        appointments = appointments.filter(
            Appointment.patient_id.__eq__(patient_id))

    if user_id:
        appointments = appointments.filter(Appointment.user_id.__eq__(user_id))

    if from_date:
        appointments = appointments.filter(Appointment.date.__ge__(from_date))

    if to_date:
        appointments = appointments.filter(Appointment.date.__le__(to_date))

    if appointmentType:
        appointments = appointments.filter(
            Appointment.appointmentType == appointmentType)

    if reason:
        appointments = appointments.filter(Appointment.reason == reason)

    return appointments


def get_appointment_by_id(appointment_id):
    return Appointment.query.get(appointment_id)


def add_appointment(dateApp, timeApp, appointmentType, reasonApp, practitioner_id, patient_id, user_id):

    appointment = Appointment(date=dateApp,
                              time=timeApp,
                              appointmentType=appointmentType,
                              reason=reasonApp,
                              patient_id=int(patient_id),
                              practitioner_id=int(practitioner_id),
                              user_id=int(user_id))
    db.session.add(appointment)
    db.session.commit()


def update_appointment(appointment_id, dateApp, timeApp, appointmentType, reasonApp, practitioner_id):
    info = db.session.query(Appointment).get(appointment_id)
    if info:
        info.date = dateApp
        info.time = timeApp
        info.appointmentType = appointmentType
        info.reason = reasonApp
        info.practitioner_id = int(practitioner_id)

        db.session.commit()


def delete_appointment(appointment_id):
    appointment = db.session.query(Appointment).get(appointment_id)

    db.session.delete(appointment)
    db.session.commit()


def update_practitioner_gender(practitioner_id, genderPractitioner):
    practitioner = db.session.query(Practitioner).get(practitioner_id)
    if practitioner:
        practitioner.gender = genderPractitioner

        db.session.commit()


def update_practitioner_birthDate(practitioner_id, birthDatePractitioner):
    practitioner = db.session.query(Practitioner).get(practitioner_id)
    if practitioner:
        practitioner.birthDate = birthDatePractitioner

        db.session.commit()


def update_practitioner_address(practitioner_id, addressPractitioner):
    practitioner = db.session.query(Practitioner).get(practitioner_id)
    if practitioner:
        practitioner.address = addressPractitioner.strip()

        db.session.commit()


def update_practitioner_language(practitioner_id, language):
    practitioner = db.session.query(Practitioner).get(practitioner_id)
    if practitioner:
        practitioner.language = language.strip()

        db.session.commit()


def update_patient_gender(patient_id, genderPatient):
    patient = db.session.query(Patient).get(patient_id)
    if patient:
        patient.gender = genderPatient

        db.session.commit()


def update_patient_birthDate(patient_id, birthDatePatient):
    patient = db.session.query(Patient).get(patient_id)
    if patient:
        patient.birthDate = birthDatePatient

        db.session.commit()


def update_patient_address(patient_id, addressPatient):
    patient = db.session.query(Patient).get(patient_id)
    if patient:
        patient.address = addressPatient.strip()

        db.session.commit()


def export_csv():
    patients = Patient.query.filter(Patient.active.__eq__(True))

    p = os.path.join(app.root_path, "data/patient-%s.csv" %
                     str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
    with open(p, 'w', encoding="utf-8") as f:
        writer = csv.DictWriter(f,
                                fieldnames=["Id", "Name", "Gender", "Birth Date",
                                            "Address", "Email", "Vaccine Status",
                                            "Vaccine Code", "Vaccine Date", "Temperature Status", "Effective Date",
                                            "Temperature", "Unit", "Practitioner Name"])
        writer.writeheader()
        for patient in patients:
            vaccineStatus = ""
            vaccineCode = ""
            occurrenceDateTime = ""
            if patient.immunization_id:
                vaccineStatus = patient.Immunization.status
                vaccineCode = patient.Immunization.vaccineCode
                occurrenceDateTime = patient.Immunization.occurrenceDateTime

            temperatureStatus = ""
            effectiveDateTime = ""
            value = ""
            unit = ""
            if patient.observation_id:
                temperatureStatus = patient.Observation.status
                effectiveDateTime = patient.Observation.effectiveDateTime
                value = patient.Observation.value
                unit = patient.Observation.unit

            practitionerName = ""
            if patient.practitioner_id:
                practitionerName = patient.Practitioner.name

            patient_dict = OrderedDict([
                ("Id", patient.id),
                ("Name", patient.name),
                ("Gender", patient.gender),
                ("Birth Date", patient.birthDate),
                ("Address", patient.address),
                ("Email", patient.email),
                ("Vaccine Status", vaccineStatus),
                ("Vaccine Code", vaccineCode),
                ("Vaccine Date", occurrenceDateTime),
                ("Temperature Status", temperatureStatus),
                ("Effective Date", effectiveDateTime),
                ("Temperature", value),
                ("Unit", unit),
                ("Practitioner Name", practitionerName)
            ])
            writer.writerow(patient_dict)
    return p
