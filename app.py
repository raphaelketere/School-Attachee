import mysql.connector
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

mdb = mysql.connector.connect(
    host="localhost",
    user="rootuser",
    password="qwerty123",
    database="attachees"
)
def get_Attachee():
    cursor = mdb.cursor()
    sql = "SELECT * FROM attachee"
    cursor.execute(sql)
    Attachee_data = cursor.fetchall()
    cursor.close()
    return Attachee_data

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/supervisor_login")
def supervisor_login():
    return render_template("supervisorLogin.html")


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin_username = request.form.get("username")
        admin_password = request.form.get("password")

        cursor = mdb.cursor()

        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        params = (admin_username, admin_password)

        cursor.execute(query, params)

        result = cursor.fetchone()

        cursor.close()
        if result:
            return redirect("/admin_home")
        else:
            return "Invalid credentials"

    return render_template("adminLogin.html")

@app.route("/adminhome")
def admin_home():
    return render_template("adminhome.html", attachees = get_Attachee())

@app.route("/assign_supervisor")
def assign_supervisor():
    supervisors = ["Supervisor 1", "Supervisor 2", "Supervisor 3"]
    return render_template("supervisor.html", supervisors=supervisors)

@app.route("/attachees_registration", methods=["GET", "POST"])
def attachees_registration():
    if request.method == "POST":
        attachee_name = request.form.get("name")
        attachee_university = request.form.get("university")
        attachee_course = request.form.get("course")
        attachee_email = request.form.get("email")
        attachee_contact = request.form.get("contact")
        attachee_interests = request.form.getlist("interests[]")
        attachee_start_date = request.form.get("start_date")
        attachee_end_date = request.form.get("end_date")

        cursor = mdb.cursor()

        query = "INSERT INTO attachee (Name, University, Course, Email, Contact, Interests, StartDate, EndDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        params = (attachee_name, attachee_university, attachee_course, attachee_email, attachee_contact, ", ".join(attachee_interests), attachee_start_date, attachee_end_date)

        cursor.execute(query, params)
        mdb.commit()
        cursor.close()

        return redirect("/admin_home")
    return render_template("registerAttachee.html")

@app.route("/supervisor_assignment_success")
def supervisor_assignment_success():
    return "Supervisor assignment successful!"

@app.route("/registered_attachees")
def registered_attachees():
    cursor = mdb.cursor()

    query = "SELECT * FROM attachee"

    cursor.execute(query)

    attachees = cursor.fetchall()

    cursor.close()

    return render_template("adminhome.html", attachee=attachees)


@app.route("/attachee_login", methods=['GET', 'POST'])
def attachee_login():
    if request.method == 'POST':
        attachee_email = request.form.get('email')
        attachee_password = request.form.get('password')

       
        cursor = mdb.cursor()
        query = "SELECT * FROM attachee WHERE email = %s AND password = %s"
        params = (attachee_email, attachee_password)

        cursor.execute(query, params)

        attachee_data = cursor.fetchone()
        # Attachee_data = cursor.fetchall()
        print(attachee_data)

        cursor.close()

        if attachee_data:
            attachee_fname = attachee_data[0]
            attachee_university = attachee_data[2]
            attachee_course = attachee_data[3]
            attachee_email = attachee_data[1]
            attachee_contact = attachee_data[4]
            attachee_interests = attachee_data[5]
            # attachee_start_date = attachee_data[7]
            # attachee_end_date = attachee_data[8]

            return render_template("attacheeDashboard.html", attachee_fname=attachee_fname,
                                   attachee_university=attachee_university, attachee_course=attachee_course,
                                   attachee_email=attachee_email, attachee_contact=attachee_contact,
                                    attachee_interests=attachee_interests,
                                    #   attachee_start_date=attachee_start_date,
                                    # attachee_end_date=attachee_end_date
                                )
        else:
            return "Invalid details entered"

    return render_template("attacheeLogin.html")



if __name__ == "__main__":
    app.run(debug=True)
