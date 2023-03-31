import datetime, uuid, pathlib, os
from flask import Flask, render_template, request, redirect, session, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/data1'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = "mysecretkey"


class Users(db.Model):
    __tablename__ = "users"
    UserId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    OTP = db.Column(db.Integer)


class SchoolProgramme(db.Model):
    __tablename__ = "schoolprogramme"
    Id = db.Column(db.Integer, primary_key=True)
    SchoolProgramme = db.Column(db.Text, nullable=True)


class Schoolcelebration(db.Model):
    __tablename__ = "schoolcelebration"
    Id = db.Column(db.Integer, primary_key=True)
    Schoolcelebration = db.Column(db.Text, nullable=True)


class StudentProgramme(db.Model):
    __tablename__ = "studentprogramme"
    Id = db.Column(db.Integer, primary_key=True)
    StudentProgramme = db.Column(db.Text, nullable=True)


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html', Error=0)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # check if the username and password are valid
        admin = Users.query.all()[0]
        if admin.Username==username and admin.Password == password:
            return redirect(url_for("admin_page"))
        else:
            return render_template('login.html', Error="Invalid login credentials")
    else:
        return render_template("login.html", Error=0)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_custom_name(original_file_name):
    unique_filename = str(
        original_file_name.replace(".", "-") + str(datetime.datetime.now(datetime.timezone.utc)).replace(':',
                                                                                                         '-').replace(
            ".", "-") + str(uuid.uuid4())).replace(" ", "-")
    return unique_filename + pathlib.Path(original_file_name).suffix


app.config['SCHOOLPROGRAMME_UPLOAD_FOLDER'] = "static/images/schoolprogramme/"
app.config['SCHOOLCELEBRATION_UPLOAD_FOLDER'] = "static/images/schoolcelebration/"
app.config['STUDENTPROGRAMME_UPLOAD_FOLDER'] = "static/images/studentprogramme/"

@app.route('/admin/gallery', methods=['GET'])
def admin_gallery_main():
    schoolprogramme = SchoolProgramme.query.all()
    schoolcelebration = Schoolcelebration.query.all()
    studentprogramme = StudentProgramme.query.all()
    return render_template('gallery.html', schoolprogramme=schoolprogramme, schoolcelebration=schoolcelebration,
                           studentprogramme=studentprogramme)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/club', methods=['GET'])
def club():
    return render_template('club.html')



@app.route('/admin/page', methods=['GET'])
def admin_page():
    schoolprogramme = SchoolProgramme.query.all()
    schoolcelebration = Schoolcelebration.query.all()
    studentprogramme = StudentProgramme.query.all()
    return render_template('adminpage.html', schoolprogramme=schoolprogramme, schoolcelebration=schoolcelebration,
                           studentprogramme=studentprogramme)


@app.route('/gallery/page', methods=['GET'])
def gallery_page():
    schoolprogramme = SchoolProgramme.query.all()
    schoolcelebration = Schoolcelebration.query.all()
    studentprogramme = StudentProgramme.query.all()
    return render_template('gallery.html', schoolprogramme=schoolprogramme, schoolcelebration=schoolcelebration,
                           studentprogramme=studentprogramme)


@app.route('/school/programme', methods=['POST'])
def school_programme():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename) and file.filename != '':
            filename = generate_custom_name(file.filename)
            filepath = os.path.join(app.config['SCHOOLPROGRAMME_UPLOAD_FOLDER'], filename)
            file.save(filepath)
            schl = SchoolProgramme(SchoolProgramme=filename)
            db.session.add(schl)
            db.session.commit()
            return redirect(url_for("admin_page"))
            flash("File Upload Successfully", "success")
        return redirect(url_for("admin_page"))
    else:
        return {"status": "error"}


@app.route('/school/celebration', methods=['POST'])
def school_celebration():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename) and file.filename != '':
            filename = generate_custom_name(file.filename)
            filepath = os.path.join(app.config['SCHOOLCELEBRATION_UPLOAD_FOLDER'], filename)
            file.save(filepath)
            schl = Schoolcelebration(Schoolcelebration=filename)
            db.session.add(schl)
            db.session.commit()
            return redirect(url_for("admin_page"))
            flash("File Upload Successfully", "success")
        return redirect(url_for("admin_page"))
    else:
        return {"status": "error"}


@app.route('/student/programme', methods=['POST'])
def student_programme():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename) and file.filename != '':
            filename = generate_custom_name(file.filename)
            filepath = os.path.join(app.config['STUDENTPROGRAMME_UPLOAD_FOLDER'], filename)
            file.save(filepath)
            schl = StudentProgramme(StudentProgramme=filename)
            db.session.add(schl)
            db.session.commit()
            return redirect(url_for("admin_page"))
            flash("File Upload Successfully", "success")
        return redirect(url_for("admin_page"))
    else:
        return {"status": "error"}


@app.route('/SchoolProgramme/delete/<int:id>')
def delete_SchoolProgramme(id):
    schl1 = SchoolProgramme.query.get(id)
    filepath = os.path.join(app.config['SCHOOLPROGRAMME_UPLOAD_FOLDER'], schl1.SchoolProgramme)
    os.remove(filepath)
    db.session.delete(schl1)
    db.session.commit()
    return redirect(url_for("admin_page"))


@app.route('/Schoolcelebration/delete/<int:id>')
def delete_Schoolcelebration(id):
    schl1 = Schoolcelebration.query.get(id)
    filepath = os.path.join(app.config['SCHOOLCELEBRATION_UPLOAD_FOLDER'], schl1.Schoolcelebration)
    os.remove(filepath)
    db.session.delete(schl1)
    db.session.commit()
    return redirect(url_for("admin_page"))


@app.route('/StudentProgramme/delete/<int:id>')
def delete_StudentProgramme(id):
    schl1 = StudentProgramme.query.get(id)
    filepath = os.path.join(app.config['STUDENTPROGRAMME_UPLOAD_FOLDER'], schl1.StudentProgramme)
    os.remove(filepath)
    db.session.delete(schl1)
    db.session.commit()
    return redirect(url_for("admin_page"))


@app.route('/change/password', methods=['GET', 'POST'])
def change_password():
    if request.method == "GET":
        return render_template('changepassword.html', Error=0)
    if request.method == "POST":
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        if str(password) == str(cpassword):
            user = Users.query.all()
            userdata = user[0]
            userdata.Password = str(password)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            return render_template("changepassword.html", Error="Password does not match")
