from flask import render_template, request, redirect, url_for, session, jsonify, send_file, Response
from app import app, login
from app import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, current_user
from flask_login import login_required
from app.models import UserRole
import os
from datetime import date, datetime, timedelta
import random
from string import ascii_uppercase
from flask_socketio import SocketIO, join_room, leave_room, send, emit


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
                           practitioners=utils.load_practitioner(),
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
        emailPatient = request.form.get('emailPatient')
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
                              emailPatient=emailPatient,
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
        emailPatient = request.form.get('emailPatient')
        practitioner_id = request.form.get('practitioner_id')

        try:
            utils.update_patient_info(patient_id=int(patient_id),
                                      namePatient=namePatient,
                                      genderPatient=genderPatient,
                                      birthDatePatient=birthDatePatient,
                                      addressPatient=addressPatient,
                                      emailPatient=emailPatient,
                                      practitioner_id=int(practitioner_id))
            return redirect("/fhir/Patient/{}".format(patient_id))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('patient_edit_info.html',
                           patient=patient,
                           practitioners=utils.load_practitioner(),
                           err_msg=err_msg,
                           UserRole=UserRole)


@app.route("/fhir/Patient/editImmunization", methods=['get', 'post'])
@login_required
def patient_edit_immunization():
    err_msg = ""
    immunization_id = request.args.get('immunization_id')
    immunization = None
    if immunization_id:
        immunization = utils.get_immunization_by_id(
            immunization_id=int(immunization_id))

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
        observation = utils.get_observation_by_id(
            observation_id=int(observation_id))

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
        practitioner = utils.get_practitioner_by_id(
            practitioner_id=int(practitioner_id))

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


@app.route('/register_doctor', methods=['get', 'post'])
def user_register_doctor():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None
        genderPractitioner = request.form.get('genderPractitioner')
        birthDatePractitioner = request.form.get('birthDatePractitioner')
        addressPractitioner = request.form.get('addressPractitioner')
        language = request.form.get('language')
        position = request.form.get('position')

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user_doctor(name=name,
                                      username=username,
                                      password=password,
                                      email=email,
                                      avatar=avatar_path,
                                      genderPractitioner=genderPractitioner,
                                      birthDatePractitioner=birthDatePractitioner,
                                      addressPractitioner=addressPractitioner,
                                      language=language,
                                      position=position)
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'The re-entered password is incorrect'
        except Exception as ex:
            err_msg = 'Your identifier or email already exists' + str(ex)

    return render_template('register_doctor.html',
                           err_msg=err_msg)


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
                               avatar=avatar_path,
                               genderPatient=genderPatient,
                               birthDatePatient=birthDatePatient,
                               addressPatient=addressPatient,
                               statusVaccine=statusVaccine,
                               vaccineCode=vaccineCode,
                               occurrenceDateTime=occurrenceDateTime,
                               statusObservation=statusObservation,
                               effectiveDateTime=effectiveDateTime,
                               value=value,
                               unit=unit)
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
    if current_user.user_role == UserRole.DOCTOR:
        return render_template('info_perso_doctor.html', practitioners=utils.load_practitioner(), UserRole=UserRole)
    elif current_user.user_role == UserRole.PATIENT:
        return render_template('info_perso.html', patients=utils.load_patient(), practitioners=utils.load_practitioner(), UserRole=UserRole)


@app.route('/upload', methods=['post'])
def upload():
    f = request.files['prescription']
    f.save(os.path.join(app.root_path, 'static/uploads/', f.filename))
    return 'DONE.'


@app.route("/room_teleconsultation")
@login_required
def room_teleconsultation():

    return redirect("http://127.0.0.1:3000/", code=302)

# ------------------------ appointment ------------------------


@app.route("/fhir/Appointment")
@login_required
def appointment_list():
    practitioner_id = request.args.get('practitioner_id')
    user_id = request.args.get('user_id')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    appointmentType = request.args.get('appointmentType')
    reason = request.args.get('reason')
    patient_id = request.args.get('patient_id')

    if not user_id:
        if current_user.user_role == UserRole.PATIENT:
            patient_id = current_user.patient_id
        elif current_user.user_role == UserRole.DOCTOR:
            practitioner_id = current_user.practitioner_id

    appointments = utils.load_appointment(practitioner_id=practitioner_id,
                                          user_id=user_id,
                                          from_date=from_date,
                                          to_date=to_date,
                                          appointmentType=appointmentType,
                                          reason=reason,
                                          patient_id=patient_id)

    return render_template('appointment.html', 
                           appointments=appointments, 
                           users=utils.load_user(), 
                           practitioners=utils.load_practitioner(), 
                           patients=utils.load_patient(), 
                           UserRole=UserRole)


@app.route("/fhir/Appointment/add", methods=['get', 'post'])
@login_required
def appointment_add():
    if current_user.user_role == UserRole.PATIENT:
        err_msg = ""
        current_date = date.today().strftime('%Y-%m-%d')

        # Générer les créneaux de 08:00 à 19:00
        start_time = datetime.strptime("08:00", "%H:%M")
        end_time = datetime.strptime("19:00", "%H:%M")
        time_step = timedelta(minutes=30)
        time_slots = []
        current_time = start_time
        while current_time <= end_time:
            time_slots.append(current_time.strftime("%H:%M"))
            current_time += time_step

        if request.method.__eq__('POST'):
            dateApp = request.form.get('dateApp')
            timeApp = request.form.get('timeApp')
            appointmentType = request.form.get('appointmentType')
            reasonApp = request.form.get('reasonApp')
            patient_id = current_user.patient_id
            practitioner_id = request.form.get('practitioner_id')
            user_id = current_user.id

            try:
                utils.add_appointment(dateApp=dateApp,
                                      timeApp=timeApp,
                                      appointmentType=appointmentType,
                                      reasonApp=reasonApp,
                                      patient_id=int(patient_id),
                                      practitioner_id=int(practitioner_id),
                                      user_id=int(user_id))
                return redirect(url_for('appointment_list'))
            except Exception as ex:
                err_msg = 'Something wrong!!! Please back later!' + str(ex)

        return render_template('appointment_add_patient.html',
                               practitioners=utils.load_practitioner(),
                               err_msg=err_msg,
                               UserRole=UserRole,
                               current_date=current_date,
                               time_slots=time_slots)
    elif current_user.user_role == UserRole.DOCTOR:
        err_msg = ""
        current_date = date.today().strftime('%Y-%m-%d')

        # Générer les créneaux de 08:00 à 19:00
        start_time = datetime.strptime("08:00", "%H:%M")
        end_time = datetime.strptime("19:00", "%H:%M")
        time_step = timedelta(minutes=30)
        time_slots = []
        current_time = start_time
        while current_time <= end_time:
            time_slots.append(current_time.strftime("%H:%M"))
            current_time += time_step

        if request.method.__eq__('POST'):
            dateApp = request.form.get('dateApp')
            timeApp = request.form.get('timeApp')
            appointmentType = request.form.get('appointmentType')
            reasonApp = request.form.get('reasonApp')
            patient_id = request.form.get('patient_id')
            practitioner_id = request.form.get('practitioner_id')
            user_id = current_user.id

            try:
                utils.add_appointment(dateApp=dateApp,
                                      timeApp=timeApp,
                                      appointmentType=appointmentType,
                                      reasonApp=reasonApp,
                                      patient_id=int(patient_id),
                                      practitioner_id=int(practitioner_id),
                                      user_id=int(user_id))
                return redirect(url_for('appointment_list'))
            except Exception as ex:
                err_msg = 'Something wrong!!! Please back later!' + str(ex)

        return render_template('appointment_add_doctor.html',
                               practitioners=utils.load_practitioner(),
                               patients=utils.load_patient(),
                               err_msg=err_msg,
                               UserRole=UserRole,
                               current_date=current_date,
                               time_slots=time_slots)


@app.route("/fhir/Appointment/edit", methods=['get', 'post'])
@login_required
def appointment_edit():
    err_msg = ""
    appointment_id = request.args.get('appointment_id')
    appointment = None
    if appointment_id:
        appointment = utils.get_appointment_by_id(
            appointment_id=int(appointment_id))

    current_date = date.today().strftime('%Y-%m-%d')

    # Générer les créneaux de 08:00 à 19:00
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("19:00", "%H:%M")
    time_step = timedelta(minutes=30)
    time_slots = []
    current_time = start_time
    while current_time <= end_time:
        time_slots.append(current_time.strftime("%H:%M"))
        current_time += time_step

    if request.method.__eq__('POST'):
        dateApp = request.form.get('dateApp')
        timeApp = request.form.get('timeApp')
        appointmentType = request.form.get('appointmentType')
        reasonApp = request.form.get('reasonApp')
        practitioner_id = request.form.get('practitioner_id')

        try:
            utils.update_appointment(appointment_id=int(appointment_id),
                                     dateApp=dateApp,
                                     timeApp=timeApp,
                                     appointmentType=appointmentType,
                                     reasonApp=reasonApp,
                                     practitioner_id=int(practitioner_id))
            return redirect(url_for('appointment_list'))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('appointment_edit.html',
                           appointment=appointment,
                           current_date=current_date,
                           time_slots=time_slots,
                           practitioners=utils.load_practitioner(),
                           err_msg=err_msg,
                           UserRole=UserRole)


@app.route('/fhir/deleteAppointment', methods=['POST', 'DELETE'])
def appointment_delete():
    if request.method == 'POST' or request.method == 'DELETE':
        appointment_id = request.args.get('appointment_id')
        utils.delete_appointment(appointment_id=int(appointment_id))

        appointments = utils.load_appointment()

        return render_template('appointment.html', appointments=appointments, UserRole=UserRole)


# ------------------------ chatRoom ------------------------
socketio = SocketIO(app)

rooms = {}


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code


@app.route("/room_home", methods=["POST", "GET"])
def room_home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home_room.html", error="Please enter a name.", code=code, name=name, UserRole=UserRole)

        if join != False and not code:
            return render_template("home_room.html", error="Please enter a room code.", code=code, name=name, UserRole=UserRole)

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home_room.html", error="Room does not exist.", code=code, name=name, UserRole=UserRole)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home_room.html", UserRole=UserRole)


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("room_home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


@app.route("/SendMail")
def send_mail():
    # if current_user.user_role == UserRole.PATIENT:
    return render_template('room_email.html', practitioners=utils.load_practitioner(), UserRole=UserRole)

# ------------------------ edit Info Practitioner ------------------------


@app.route("/fhir/editPractitioner/gender", methods=['GET', 'POST'])
@login_required
def practitioner_edit_gender():
    err_msg = ""
    practitioner_id = request.args.get('practitioner_id')
    practitioner = None
    if practitioner_id:
        practitioner = utils.get_practitioner_by_id(
            practitioner_id=int(practitioner_id))

    if request.method.__eq__('POST'):
        genderPractitioner = request.form.get('genderPractitioner')

        try:
            utils.update_practitioner_gender(practitioner_id=int(practitioner_id),
                                             genderPractitioner=genderPractitioner)
            return redirect(url_for('info_perso'))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('practitioner_edit_gender.html',
                           practitioner=practitioner,
                           err_msg=err_msg,
                           UserRole=UserRole)


@app.route("/fhir/editPractitioner/birthDate", methods=['GET', 'POST'])
@login_required
def practitioner_edit_birthDate():
    err_msg = ""
    practitioner_id = request.args.get('practitioner_id')
    practitioner = None
    if practitioner_id:
        practitioner = utils.get_practitioner_by_id(
            practitioner_id=int(practitioner_id))

    if request.method.__eq__('POST'):
        birthDatePractitioner = request.form.get('birthDatePractitioner')

        try:
            utils.update_practitioner_birthDate(practitioner_id=int(practitioner_id),
                                                birthDatePractitioner=birthDatePractitioner)
            return redirect(url_for('info_perso'))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('practitioner_edit_birthDate.html',
                           practitioner=practitioner,
                           err_msg=err_msg,
                           UserRole=UserRole)


@app.route("/fhir/editPractitioner/Address", methods=['GET', 'POST'])
@login_required
def practitioner_edit_address():
    err_msg = ""
    practitioner_id = request.args.get('practitioner_id')
    practitioner = None
    if practitioner_id:
        practitioner = utils.get_practitioner_by_id(
            practitioner_id=int(practitioner_id))

    if request.method.__eq__('POST'):
        addressPractitioner = request.form.get('addressPractitioner')

        try:
            utils.update_practitioner_address(practitioner_id=int(practitioner_id),
                                              addressPractitioner=addressPractitioner)
            return redirect(url_for('info_perso'))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('practitioner_edit_address.html',
                           practitioner=practitioner,
                           err_msg=err_msg,
                           UserRole=UserRole)


@app.route("/fhir/editPractitioner/Language", methods=['GET', 'POST'])
@login_required
def practitioner_edit_language():
    err_msg = ""
    practitioner_id = request.args.get('practitioner_id')
    practitioner = None
    if practitioner_id:
        practitioner = utils.get_practitioner_by_id(
            practitioner_id=int(practitioner_id))

    if request.method.__eq__('POST'):
        language = request.form.get('language')

        try:
            utils.update_practitioner_language(practitioner_id=int(practitioner_id),
                                               language=language)
            return redirect(url_for('info_perso'))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('practitioner_edit_language.html',
                           practitioner=practitioner,
                           err_msg=err_msg,
                           UserRole=UserRole)

# ------------------------ edit Info Patient ------------------------


@app.route("/fhir/editPatient/gender", methods=['GET', 'POST'])
@login_required
def patient_edit_gender():
    err_msg = ""
    patient_id = request.args.get('patient_id')
    patient = None
    if patient_id:
        patient = utils.get_patient_by_id(patient_id=int(patient_id))

    if request.method.__eq__('POST'):
        genderPatient = request.form.get('genderPatient')

        try:
            utils.update_patient_gender(patient_id=int(patient_id),
                                        genderPatient=genderPatient)
            return redirect(url_for('info_perso'))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('patient_edit_gender.html',
                           patient=patient,
                           err_msg=err_msg,
                           UserRole=UserRole)


@app.route("/fhir/editPatient/birthDate", methods=['GET', 'POST'])
@login_required
def patient_edit_birthDate():
    err_msg = ""
    patient_id = request.args.get('patient_id')
    patient = None
    if patient_id:
        patient = utils.get_patient_by_id(patient_id=int(patient_id))

    if request.method.__eq__('POST'):
        birthDatePatient = request.form.get('birthDatePatient')

        try:
            utils.update_patient_birthDate(patient_id=int(patient_id),
                                           birthDatePatient=birthDatePatient)
            return redirect(url_for('info_perso'))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('patient_edit_birthDate.html',
                           patient=patient,
                           err_msg=err_msg,
                           UserRole=UserRole)


@app.route("/fhir/editPatient/Address", methods=['GET', 'POST'])
@login_required
def patient_edit_address():
    err_msg = ""
    patient_id = request.args.get('patient_id')
    patient = None
    if patient_id:
        patient = utils.get_patient_by_id(patient_id=int(patient_id))

    if request.method.__eq__('POST'):
        addressPatient = request.form.get('addressPatient')

        try:
            utils.update_patient_address(patient_id=int(patient_id),
                                         addressPatient=addressPatient)
            return redirect(url_for('info_perso'))
        except Exception as ex:
            err_msg = 'Something wrong!!! Please back later!' + str(ex)

    return render_template('patient_edit_address.html',
                           patient=patient,
                           err_msg=err_msg,
                           UserRole=UserRole)


@app.route("/fhir/Patient/export")
@login_required
def patient_export():
    return send_file(utils.export_csv())


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    socketio.run(app, debug=True)
