from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
import os



app = Flask(__name__)

project_dir= os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(project_dir, "attendance.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# name of class must always start with upper case
class Attendance(db.Model):
    firstname = db.Column(db.String(40), unique = False, nullable = False)
    lastname = db.Column(db.String(40), unique = False, nullable = False)
    email = db.Column(db.String(60), unique = True, nullable = False, primary_key =True)

    def __repr__(self):
        return "First Name: {}: Last Name: {}".format(self.firstname, self.lastname)


@app.route('/', methods = ["GET","POST"])
def home():

    if request.form:
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")

        fellow = Attendance(firstname=firstname, lastname=lastname, email=email)
        db.session.add(fellow)
        db.session.commit()

    fellow = Attendance.query.all()
    return render_template("index.html", guys = fellow)



if __name__  =="__main__":
    app.run(debug=True)