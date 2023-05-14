import math
from flask import render_template, request, redirect, url_for, session, jsonify, send_file
from app import app, login
from app import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, current_user
from flask_login import login_required
from app.models import UserRole


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/blog")
def blog():
    return render_template('blog.html')


@app.route("/blog-single-1")
def blog_single_1():
    return render_template('blog-single-1.html')


@app.route("/blog-single-2")
def blog_single_2():
    return render_template('blog-single-2.html')


@app.route("/blog-single-3")
def blog_single_3():
    return render_template('blog-single-3.html')


@app.route("/blog-single-4")
def blog_single_4():
    return render_template('blog-single-4.html')


@app.route("/blog-single-5")
def blog_single_5():
    return render_template('blog-single-5.html')


@app.route("/blog-single-6")
def blog_single_6():
    return render_template('blog-single-6.html')


@app.route("/services")
def services():
    return render_template('services.html')


@app.route("/doctors")
def doctors():
    return render_template('doctors.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/fhir/Patient")
@login_required
def patient_list():
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

    return render_template('patient.html', patients=patients)


@app.route("/fhir/Patient/<int:patient_id>")
@login_required
def patient_detail(patient_id):
    patient = utils.get_patient_by_id(patient_id)

    return render_template('patient_detail.html',
                           patient=patient)


@app.route("/fhir/Patient/add", methods=['get', 'post'])
@login_required
def add_or_update_patient():
    if request.method.lower() == "post":
        return redirect(url_for('patient_list'))

    return render_template("patient_add.html",
                           immunization=utils.load_immunization(),
                           practitioner=utils.load_practitioner(),
                           observation=utils.load_observation())


@app.route("/fhir/Immunization/<int:immunization_id>")
@login_required
def immunization_detail(immunization_id):
    immunization = utils.get_immunization_by_id(immunization_id)

    return render_template('immunization_detail.html',
                           immunization=immunization)


@app.route("/fhir/Observation/<int:observation_id>")
@login_required
def observation_detail(observation_id):
    observation = utils.get_observation_by_id(observation_id)

    return render_template('observation_detail.html',
                           observation=observation)


@app.route("/fhir/Practitioner/<int:practitioner_id>")
@login_required
def practitioner_detail(practitioner_id):
    practitioner = utils.get_practitioner_by_id(practitioner_id)

    return render_template('practitioner_detail.html',
                           practitioner=practitioner)


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
                           practitioners=practitioners)


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
                err_msg = 'Le mot de passe ressaisi est incorrect'
        except Exception as ex:
            err_msg = 'Le système a une erreur' + str(ex)

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
            err_msg = "Identifiant ou mot de passe incorrect!!!"

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
    return render_template('info_perso.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
