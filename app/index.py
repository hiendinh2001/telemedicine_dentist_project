import math
from flask import render_template, request, redirect, url_for, session, jsonify, send_file, Response
from app import app, login
from app import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, current_user
from flask_login import login_required
from app.models import UserRole
import os
import cv2
import random
from string import ascii_letters as ascii


@app.route("/")
def home():
    return render_template('index.html', UserRole=UserRole)

@app.route("/about")
def about():
    return render_template('about.html', UserRole=UserRole)


@app.route("/blog")
def blog():
    return render_template('blog.html', UserRole=UserRole)


@app.route("/blog-single-1")
def blog_single_1():
    return render_template('blog-single-1.html', UserRole=UserRole)


@app.route("/blog-single-2")
def blog_single_2():
    return render_template('blog-single-2.html', UserRole=UserRole)


@app.route("/blog-single-3")
def blog_single_3():
    return render_template('blog-single-3.html', UserRole=UserRole)


@app.route("/blog-single-4")
def blog_single_4():
    return render_template('blog-single-4.html', UserRole=UserRole)


@app.route("/blog-single-5")
def blog_single_5():
    return render_template('blog-single-5.html', UserRole=UserRole)


@app.route("/blog-single-6")
def blog_single_6():
    return render_template('blog-single-6.html', UserRole=UserRole)


@app.route("/services")
def services():
    return render_template('services.html', UserRole=UserRole)


@app.route("/doctors")
def doctors():
    return render_template('doctors.html', UserRole=UserRole)


@app.route("/contact")
def contact():
    return render_template('contact.html', UserRole=UserRole)


@app.route("/fhir/Patient")
@login_required
def patient_list():
    if current_user.user_role == UserRole.DOCTOR:
        immunization_id = request.args.get('immunization_id')
        practitioner_id = request.args.get('practitioner_id')
        observation_id = request.args.get('observation_id')
        name = request.args.get("name")
        gender = request.args.get("gender")

        patients = utils.load_patient(immunization_id=immunization_id,
                                      practitioner_id=practitioner_id,
                                      observation_id=observation_id,
                                      name=name,
                                      gender=gender)

        return render_template('patient.html', patients=patients, UserRole=UserRole)


@app.route("/fhir/Patient/<int:patient_id>")
@login_required
def patient_detail(patient_id):
    patient = utils.get_patient_by_id(patient_id)

    return render_template('patient_detail.html',
                           patient=patient,
                           UserRole=UserRole)


@app.route("/fhir/Patient/add", methods=['get', 'post'])
@login_required
def patient_add():
    err_msg = ""
    if request.method.__eq__('POST'):
        namePatient = request.form.get('namePatient')
        genderPatient = request.form.get('genderPatient')
        birthDatePatient = request.form.get('birthDatePatient')
        addressPatient = request.form.get('addressPatient')
        statusVaccine = request.form.get('statusVaccine')
        vaccineCode = request.form.get('vaccineCode')
        occurrenceDateTime = request.form.get('occurrenceDateTime')
        statusObservation = request.form.get('statusObservation')
        effectiveDateTime = request.form.get('effectiveDateTime')
        value = request.form.get('value')
        unit = request.form.get('unit')
        practitioner_id = request.form.get('practitioner_id')

        try:
            utils.add_patient(namePatient=namePatient,
                              genderPatient=genderPatient,
                              birthDatePatient=birthDatePatient,
                              addressPatient=addressPatient,
                              statusVaccine=statusVaccine,
                              vaccineCode=vaccineCode,
                              occurrenceDateTime=occurrenceDateTime,
                              statusObservation=statusObservation,
                              effectiveDateTime=effectiveDateTime,
                              value=value,
                              unit=unit,
                              practitioner_id=int(practitioner_id))
            return redirect(url_for('patient_list'))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('patient_add.html',
                           practitioners=utils.load_practitioner(),
                           err_msg=err_msg,
                           UserRole=UserRole)

@app.route("/fhir/Patient/editInfo", methods=['get', 'post'])
@login_required
def patient_edit_info():
    err_msg = ""
    patient_id = request.args.get('patient_id')
    patient = None
    if patient_id:
        patient = utils.get_patient_by_id(patient_id=int(patient_id))

    if request.method.__eq__('POST'):
        namePatient = request.form.get('namePatient')
        genderPatient = request.form.get('genderPatient')
        birthDatePatient = request.form.get('birthDatePatient')
        addressPatient = request.form.get('addressPatient')

        try:
            utils.update_patient_info(patient_id=int(patient_id),
                                      namePatient=namePatient,
                                      genderPatient=genderPatient,
                                      birthDatePatient=birthDatePatient,
                                      addressPatient=addressPatient)
            return redirect("/fhir/Patient/{}".format(patient_id))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('patient_edit_info.html',
                           patient=patient,
                           err_msg=err_msg,
                           UserRole=UserRole)

@app.route("/fhir/Patient/editImmunization", methods=['get', 'post'])
@login_required
def patient_edit_immunization():
    err_msg = ""
    immunization_id = request.args.get('immunization_id')
    immunization = None
    if immunization_id:
        immunization = utils.get_immunization_by_id(immunization_id=int(immunization_id))

    if request.method.__eq__('POST'):
        statusVaccine = request.form.get('statusVaccine')
        vaccineCode = request.form.get('vaccineCode')
        occurrenceDateTime = request.form.get('occurrenceDateTime')

        try:
            utils.update_patient_immunization(immunization_id=int(immunization_id),
                                              statusVaccine=statusVaccine,
                                              vaccineCode=vaccineCode,
                                              occurrenceDateTime=occurrenceDateTime)
            return redirect("/fhir/Immunization/{}".format(immunization_id))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('patient_edit_immunization.html',
                           immunization=immunization,
                           err_msg=err_msg,
                           UserRole=UserRole)

@app.route("/fhir/Patient/editObservation", methods=['get', 'post'])
@login_required
def patient_edit_observation():
    err_msg = ""
    observation_id = request.args.get('observation_id')
    observation = None
    if observation_id:
        observation = utils.get_observation_by_id(observation_id=int(observation_id))

    if request.method.__eq__('POST'):
        statusObservation = request.form.get('statusObservation')
        effectiveDateTime = request.form.get('effectiveDateTime')
        value = request.form.get('value')
        unit = request.form.get('unit')

        try:
            utils.update_patient_observation(observation_id=int(observation_id),
                                             statusObservation=statusObservation,
                                             effectiveDateTime=effectiveDateTime,
                                             value=value,
                                             unit=unit)
            return redirect("/fhir/Observation/{}".format(observation_id))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('patient_edit_observation.html',
                           observation=observation,
                           err_msg=err_msg,
                           UserRole=UserRole)

@app.route("/fhir/Patient/editPractitioner", methods=['GET', 'POST'])
@login_required
def patient_edit_practitioner():
    err_msg = ""
    practitioner_id = request.args.get('practitioner_id')
    practitioner = None
    if practitioner_id:
        practitioner = utils.get_practitioner_by_id(practitioner_id=int(practitioner_id))

    if request.method.__eq__('POST'):
        namePractitioner = request.form.get('namePractitioner')
        genderPractitioner = request.form.get('genderPractitioner')
        birthDatePractitioner = request.form.get('birthDatePractitioner')
        addressPractitioner = request.form.get('addressPractitioner')
        language = request.form.get('language')

        try:
            utils.update_patient_practitioner(practitioner_id=int(practitioner_id),
                                              namePractitioner=namePractitioner,
                                              genderPractitioner=genderPractitioner,
                                              birthDatePractitioner=birthDatePractitioner,
                                              addressPractitioner=addressPractitioner,
                                              language=language)
            return redirect("/fhir/Practitioner/{}".format(practitioner_id))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('patient_edit_practitioner.html',
                           practitioner=practitioner,
                           err_msg=err_msg,
                           UserRole=UserRole)

@app.route("/fhir/Immunization/<int:immunization_id>")
@login_required
def immunization_detail(immunization_id):
    immunization = utils.get_immunization_by_id(immunization_id)

    return render_template('immunization_detail.html',
                           immunization=immunization,
                           UserRole=UserRole)


@app.route("/fhir/Observation/<int:observation_id>")
@login_required
def observation_detail(observation_id):
    observation = utils.get_observation_by_id(observation_id)

    return render_template('observation_detail.html',
                           observation=observation,
                           UserRole=UserRole)


@app.route("/fhir/Practitioner/<int:practitioner_id>")
@login_required
def practitioner_detail(practitioner_id):
    practitioner = utils.get_practitioner_by_id(practitioner_id)

    return render_template('practitioner_detail.html',
                           practitioner=practitioner,
                           UserRole=UserRole)

@app.route('/fhir/deletePatient', methods=['POST', 'DELETE'])
def patient_delete():
    if request.method == 'POST' or request.method == 'DELETE':
        patient_id = request.args.get('patient_id')
        utils.delete_patient(patient_id=int(patient_id))

        patients = utils.load_patient()

        return render_template('patient.html', patients=patients, UserRole=UserRole)

@app.route('/fhir/_history')
@login_required
def history():
    patients = utils.load_patient()
    immunizations = utils.load_immunization()
    observations = utils.load_observation()
    practitioners = utils.load_practitioner()

    return render_template('history.html',
                           patients=patients,
                           immunizations=immunizations,
                           observations=observations,
                           practitioners=practitioners,
                           UserRole=UserRole)


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name,
                               username=username,
                               password=password,
                               email=email,
                               avatar=avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'The re-entered password is incorrect'
        except Exception as ex:
            err_msg = 'Your identifier or email already exists'

    return render_template('register.html',
                           err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username,
                                 password=password)
        if user:
            login_user(user=user)

            return redirect(url_for(request.args.get('next', 'home')))
        else:
            err_msg = "Your identifier or password incorrect"

    return render_template('login.html',
                           err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/info-perso')
@login_required
def info_perso():
    return render_template('info_perso.html', UserRole=UserRole)

@app.route('/upload', methods=['post'])
def upload():
    f = request.files['prescription']
    f.save(os.path.join(app.root_path, 'static/uploads/', f.filename))
    return 'DONE.'

@app.route("/room_teleconsultation")
@login_required
def room_teleconsultation():

    return redirect("http://127.0.0.1:3000/", code=302)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
