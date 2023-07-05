from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime, Time
from sqlalchemy.orm import relationship, backref
from app import db, app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    PATIENT = 2
    DOCTOR = 3

    def __str__(self):
        return self.name


class Immunization(BaseModel):
    __tablename__ = 'Immunization'

    status = Column(String(50), nullable=True)
    vaccineCode = Column(Integer)
    occurrenceDateTime = Column(DateTime)
    patient = relationship('Patient', backref='Immunization', lazy=False)

    def __str__(self):
        return self.name


class Practitioner(BaseModel):
    __tablename__ = 'Practitioner'

    name = Column(String(50), nullable=True)
    gender = Column(String(50), nullable=True)
    birthDate = Column(DateTime)
    address = Column(String(50), nullable=True)
    language = Column(String(50), nullable=True)
    position = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    patient = relationship('Patient', backref='Practitioner', lazy=False)
    appointment = relationship(
        'Appointment', backref='Practitioner', lazy=False)
    user = relationship('User', backref='Practitioner', lazy=False)

    def __str__(self):
        return self.name


class Observation(BaseModel):
    __tablename__ = 'Observation'

    status = Column(String(50), nullable=True)
    effectiveDateTime = Column(DateTime)
    value = Column(Float)
    unit = Column(String(50), nullable=True)
    patient = relationship('Patient', backref='Observation', lazy=False)

    def __str__(self):
        return self.name


class Patient(BaseModel):
    __tablename__ = 'Patient'

    name = Column(String(50), nullable=True)
    gender = Column(String(50), nullable=True)
    birthDate = Column(DateTime)
    address = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    immunization_id = Column(Integer, ForeignKey(
        Immunization.id), nullable=True)
    practitioner_id = Column(Integer, ForeignKey(
        Practitioner.id), nullable=True, default=1)
    observation_id = Column(Integer, ForeignKey(Observation.id), nullable=True)
    user = relationship('User', backref='Patient', lazy=False)
    appointment = relationship('Appointment', backref='Patient', lazy=False)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=True, unique=True)
    password = Column(String(50), nullable=True)
    avatar = Column(String(100))
    email = Column(String(50), nullable=True, unique=True)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.PATIENT)
    appointment = relationship('Appointment', backref='User', lazy=False)
    practitioner_id = Column(Integer, ForeignKey(
        Practitioner.id), nullable=True)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=True)


class Appointment(BaseModel):
    __tablename__ = 'Appointment'

    date = Column(DateTime, nullable=True)
    time = Column(Time, nullable=True)
    status = Column(String(50), nullable=True, default='Booked')
    created = Column(DateTime, default=datetime.now())
    appointmentType = Column(String(50), nullable=True)
    reason = Column(String(50), nullable=True)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=True)
    practitioner_id = Column(Integer, ForeignKey(
        Practitioner.id), nullable=True)
    active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        i1 = Immunization(status='Completed',
                          vaccineCode='560',
                          occurrenceDateTime='2020-12-12')

        i2 = Immunization(status='Entered-in-error',
                          vaccineCode='610',
                          occurrenceDateTime='2020-11-12')

        i3 = Immunization(status='Completed',
                          vaccineCode='570',
                          occurrenceDateTime='2020-09-12')

        i4 = Immunization(status='Not-done',
                          vaccineCode='580',
                          occurrenceDateTime='2020-08-12')

        i5 = Immunization(status='Completed',
                          vaccineCode='590',
                          occurrenceDateTime='2020-07-12')

        i6 = Immunization(status='Completed',
                          vaccineCode='600',
                          occurrenceDateTime='2020-06-12')

        i7 = Immunization(status='Not-done',
                          vaccineCode='610',
                          occurrenceDateTime='2020-05-12')

        i8 = Immunization(status='Entered-in-error',
                          vaccineCode='620',
                          occurrenceDateTime='2020-04-12')

        i9 = Immunization(status='Completed',
                          vaccineCode='630',
                          occurrenceDateTime='2020-03-12')

        i10 = Immunization(status='Completed',
                           vaccineCode='640',
                           occurrenceDateTime='2020-02-12')

        db.session.add(i1)
        db.session.add(i2)
        db.session.add(i3)
        db.session.add(i4)
        db.session.add(i5)
        db.session.add(i6)
        db.session.add(i7)
        db.session.add(i8)
        db.session.add(i9)
        db.session.add(i10)

        db.session.commit()

        # pr1 = Practitioner(name='Tom Smith',
        #                    gender='Male',
        #                    birthDate='1990-10-12',
        #                    address='1 rue Constant Coquelin, Paris, France',
        #                    language='French, English, Russian',
        #                    position='Orthodontist',
        #                    email='tomsmithOrthodontist@gmail.com')

        # pr2 = Practitioner(name='Mark Wilson',
        #                    gender='Male',
        #                    birthDate='1980-11-12',
        #                    address='1 rue de la paix, Paris, France',
        #                    language='French, English, Spanish',
        #                    position='Endodontist',
        #                    email='markwilsonEndodontist@gmail.com')

        # pr3 = Practitioner(name='Patrick Jacobson',
        #                    gender='Female',
        #                    birthDate='1984-11-19',
        #                    address='1 rue de la paix, Nice, France',
        #                    language='French, German, Spanish',
        #                    position='Orthodontist',
        #                    email='patrickjacobsonOrthodontist@gmail.com')

        # pr4 = Practitioner(name='Ivan Dorchsner',
        #                    gender='Male',
        #                    birthDate='1980-10-12',
        #                    address='1 rue de la paix, Rouen, France',
        #                    language='French, Vietnamese, German',
        #                    position='Dentist and Oral Surgeon',
        #                    email='ivandorchsnerDentist@gmail.com')

        pr1 = Practitioner(name='Null',
                           gender='Null',
                           birthDate='2012-01-01',
                           address='Null',
                           language='Null',
                           position='Null',
                           email='Null')

        # pr5 = Practitioner(name='SANTOS Anna',
        #                    gender='Female',
        #                    birthDate='1985-06-12',
        #                    address='1 rue de la paix, Cannes, France',
        #                    language='French, English, Arabic')

        # pr6 = Practitioner(name='DUPONT Nicolas',
        #                    gender='Male',
        #                    birthDate='1987-03-12',
        #                    address='1 rue de la paix, Rennes, France',
        #                    language='French, English, Spanish')

        # pr7 = Practitioner(name='MARTIN Noemie',
        #                    gender='Female',
        #                    birthDate='1993-09-12',
        #                    address='1 rue de la paix, Reims, France',
        #                    language='French, Spanish, Italian')

        # pr8 = Practitioner(name='SANTOS Guillermo',
        #                    gender='Male',
        #                    birthDate='1990-12-12',
        #                    address='1 rue de la paix, Caen, France',
        #                    language='French, English, Portuguese')

        # pr9 = Practitioner(name='DUPONT Jean',
        #                    gender='Male',
        #                    birthDate='1980-11-16',
        #                    address='1 rue de la paix, Toulouse, France',
        #                    language='French, English, Spanish')

        # pr10 = Practitioner(name='DUPONT Pierre',
        #                     gender='Female',
        #                     birthDate='1984-11-16',
        #                     address='1 rue de la paix, Nice, France',
        #                     language='French, German, Spanish')

        # db.session.add(pr1)
        # db.session.add(pr2)
        # db.session.add(pr3)
        # db.session.add(pr4)
        db.session.add(pr1)
        # db.session.add(pr6)
        # db.session.add(pr7)
        # db.session.add(pr8)
        # db.session.add(pr9)
        # db.session.add(pr10)

        db.session.commit()

        o1 = Observation(status='Final',
                         effectiveDateTime='2021-12-12',
                         value='37',
                         unit='Cel')

        o2 = Observation(status='Amended +',
                         effectiveDateTime='2021-11-12',
                         value='37',
                         unit='Cel')

        o3 = Observation(status='Preliminary',
                         effectiveDateTime='2021-10-12',
                         value='36.5',
                         unit='Cel')

        o4 = Observation(status='Final',
                         effectiveDateTime='2021-09-12',
                         value='37.5',
                         unit='Cel')

        o5 = Observation(status='Amended +',
                         effectiveDateTime='2021-08-12',
                         value='36.5',
                         unit='Cel')

        o6 = Observation(status='Preliminary',
                         effectiveDateTime='2021-07-12',
                         value='37',
                         unit='Cel')

        o7 = Observation(status='Final',
                         effectiveDateTime='2021-06-12',
                         value='37.5',
                         unit='Cel')

        o8 = Observation(status='Amended +',
                         effectiveDateTime='2021-05-12',
                         value='36.5',
                         unit='Cel')

        o9 = Observation(status='Preliminary',
                         effectiveDateTime='2021-06-12',
                         value='37',
                         unit='Cel')

        o10 = Observation(status='Final',
                          effectiveDateTime='2021-12-12',
                          value='37',
                          unit='Cel')

        db.session.add(o1)
        db.session.add(o2)
        db.session.add(o3)
        db.session.add(o4)
        db.session.add(o5)
        db.session.add(o6)
        db.session.add(o7)
        db.session.add(o8)
        db.session.add(o9)
        db.session.add(o10)

        db.session.commit()

        p1 = Patient(name='SANTOS Samuel',
                     gender='Male',
                     birthDate='1990-12-12',
                     address='1 rue de la paix, Paris, France',
                     email='hello@gmail.com',
                     immunization_id=i1.id,
                     practitioner_id=pr1.id,
                     observation_id=o1.id)

        p2 = Patient(name='MARTIN Pierre',
                     gender='Male',
                     birthDate='1984-11-16',
                     address='1 rue de la paix, Nice, France',
                     email='hello@gmail.com',
                     immunization_id=i2.id,
                     practitioner_id=pr1.id,
                     observation_id=o2.id)

        p3 = Patient(name='LEFEBVRE Sophie',
                     gender='Female',
                     birthDate='1969-10-17',
                     address='3 rue de la paix, Rouen, France',
                     email='hello@gmail.com',
                     immunization_id=i3.id,
                     practitioner_id=pr1.id,
                     observation_id=o3.id)

        p4 = Patient(name='ROUSSEAU Guillaume',
                     gender='Male',
                     birthDate='1956-07-02',
                     address='1 rue de la paix, Le Havre, France',
                     email='hello@gmail.com',
                     immunization_id=i4.id,
                     practitioner_id=pr1.id,
                     observation_id=o4.id)

        p5 = Patient(name='DUPONT Marie-Claire',
                     gender='Female',
                     birthDate='2003-11-12',
                     address='1 rue de la paix, Cannes, France',
                     email='hello@gmail.com',
                     immunization_id=i5.id,
                     practitioner_id=pr1.id,
                     observation_id=o5.id)

        p6 = Patient(name='GIRARD Nicolas',
                     gender='Male',
                     birthDate='1996-05-18',
                     address='1 rue de la paix, Marseille, France',
                     email='hello@gmail.com',
                     immunization_id=i6.id,
                     practitioner_id=pr1.id,
                     observation_id=o6.id)

        p7 = Patient(name='BOUCHER Élodie',
                     gender='Female',
                     birthDate='1988-02-05',
                     address='1 rue de la paix, Rennes, France',
                     email='hello@gmail.com',
                     immunization_id=i7.id,
                     practitioner_id=pr1.id,
                     observation_id=o7.id)

        p8 = Patient(name='DELACROIX Baptiste',
                     gender='Male',
                     birthDate='1978-12-12',
                     address='1 rue de la paix, Angers, France',
                     email='hello@gmail.com',
                     immunization_id=i8.id,
                     practitioner_id=pr1.id,
                     observation_id=o8.id)

        p9 = Patient(name='MOREAU Lucie',
                     gender='Female',
                     birthDate='1991-11-15',
                     address='1 rue de la paix, Orléans, France',
                     email='hello@gmail.com',
                     immunization_id=i9.id,
                     practitioner_id=pr1.id,
                     observation_id=o9.id)

        p10 = Patient(name='DUBOIS Amélie',
                      gender='Female',
                      birthDate='1995-01-09',
                      address='1 rue de la paix, Tours, France',
                      email='hello@gmail.com',
                      immunization_id=i10.id,
                      practitioner_id=pr1.id,
                      observation_id=o10.id)

        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.add(p5)
        db.session.add(p6)
        db.session.add(p7)
        db.session.add(p8)
        db.session.add(p9)
        db.session.add(p10)

        db.session.commit()

        # u1 = User(name='Tom Smith',
        #           username='tomsmithOrthodontist',
        #           password='tomsmithOrthodontist',
        #           email='tomsmithOrthodontist@gmail.com',
        #           user_role=UserRole.DOCTOR,
        #           practitioner_id=pr1.id)

        # u2 = User(name='Mark Wilson',
        #           username='markwilsonEndodontist',
        #           password='markwilsonEndodontist',
        #           email='markwilsonEndodontist@gmail.com',
        #           user_role=UserRole.DOCTOR,
        #           practitioner_id=pr2.id)

        # u3 = User(name='Patrick Jacobson',
        #           username='patrickjacobsonOrthodontist',
        #           password='patrickjacobsonOrthodontist',
        #           email='patrickjacobsonOrthodontist@gmail.com',
        #           user_role=UserRole.DOCTOR,
        #           practitioner_id=pr3.id)

        # u4 = User(name='Ivan Dorchsner',
        #           username='ivandorchsnerDentist',
        #           password='ivandorchsnerDentist',
        #           email='ivandorchsnerDentist@gmail.com',
        #           user_role=UserRole.DOCTOR,
        #           practitioner_id=pr4.id)

        # db.session.add(u1)
        # db.session.add(u2)
        # db.session.add(u3)
        # db.session.add(u4)
        # db.session.commit()
