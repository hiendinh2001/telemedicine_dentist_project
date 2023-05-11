from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum

class BaseModel(db.Model):
    __abstract__ = True

    identifier = Column(Integer, primary_key=True, autoincrement=True)

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name
class Immunization(BaseModel):
    __tablename__ = 'Immunization'

    status = Column(String(50), nullable=False)
    vaccineCode = Column(Integer)
    patient = relationship('Patient', backref='Immunization', lazy=False)
    occurrenceDateTime = Column(DateTime)

    def __str__(self):
        return self.name

class Patient(BaseModel):
    __tablename__ = 'Patient'

    name = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    birthDate = Column(DateTime)
    address = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    immunization_id = Column(Integer, ForeignKey(Immunization.identifier), nullable=False)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        i1 = Immunization(status='completed',
                          vaccineCode='560',
                            occurrenceDateTime='2020-12-12')

        i2 = Immunization(status='entered-in-error',
                          vaccineCode='610',
                          occurrenceDateTime='2020-11-12')

        i3 = Immunization(status='completed',
                          vaccineCode='570',
                          occurrenceDateTime='2020-09-12')

        i4 = Immunization(status='not-done',
                          vaccineCode='580',
                          occurrenceDateTime='2020-08-12')

        i5 = Immunization(status='completed',
                          vaccineCode='590',
                          occurrenceDateTime='2020-07-12')

        i6 = Immunization(status='completed',
                          vaccineCode='600',
                          occurrenceDateTime='2020-06-12')

        i7 = Immunization(status='not-done',
                          vaccineCode='610',
                          occurrenceDateTime='2020-05-12')

        i8 = Immunization(status='entered-in-error',
                          vaccineCode='620',
                          occurrenceDateTime='2020-04-12')

        i9 = Immunization(status='completed',
                          vaccineCode='630',
                          occurrenceDateTime='2020-03-12')

        i10 = Immunization(status='completed',
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

        p1 = Patient(name='SANTOS Samuel',
                     gender='Male',
                     birthDate='1990-12-12',
                     address='1 rue de la paix, Paris, France',
                     immunization_id=i1.identifier)

        p2 = Patient(name='MARTIN Pierre',
                     gender='Male',
                     birthDate='1984-11-16',
                     address='1 rue de la paix, Nice, France',
                     immunization_id=i2.identifier)

        p3 = Patient(name='LEFEBVRE Sophie',
                     gender='Female',
                     birthDate='1969-10-17',
                     address='3 rue de la paix, Rouen, France',
                     immunization_id=i3.identifier)

        p4 = Patient(name='ROUSSEAU Guillaume',
                     gender='Male',
                     birthDate='1956-07-02',
                     address='1 rue de la paix, Le Havre, France',
                     immunization_id=i4.identifier)

        p5 = Patient(name='DUPONT Marie-Claire',
                     gender='Female',
                     birthDate='2003-11-12',
                     address='1 rue de la paix, Cannes, France',
                     immunization_id=i5.identifier)

        p6 = Patient(name='GIRARD Nicolas',
                     gender='Male',
                     birthDate='1996-05-18',
                     address='1 rue de la paix, Marseille, France',
                     immunization_id=i6.identifier)

        p7 = Patient(name='BOUCHER Élodie',
                     gender='Female',
                     birthDate='1988-02-05',
                     address='1 rue de la paix, Rennes, France',
                     immunization_id=i7.identifier)

        p8 = Patient(name='DELACROIX Baptiste',
                     gender='Male',
                     birthDate='1978-12-12',
                     address='1 rue de la paix, Angers, France',
                     immunization_id=i8.identifier)

        p9 = Patient(name='MOREAU Lucie',
                     gender='Female',
                     birthDate='1991-11-15',
                     address='1 rue de la paix, Orléans, France',
                     immunization_id=i9.identifier)

        p10 = Patient(name='DUBOIS Amélie',
                      gender='Female',
                      birthDate='1995-01-09',
                      address='1 rue de la paix, Tours, France',
                      immunization_id=i10.identifier)

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
