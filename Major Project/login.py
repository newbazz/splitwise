from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__='usertable'
	name=db.Column(db.String,nullable=False)
	password=db.Column(db.String,nullable=False)
	email=db.Column(db.String,nullable=False,unique=True)
	username=db.Column(db.String,unique=True,primary_key=True)
	country=db.Column(db.String(120),nullable=False)
	dob=db.Column(db.String(120),nullable=False)
	gender=db.Column(db.String(120),nullable=True)
	mobile=db.Column(db.Integer,nullable=False)
	def __init__(self, username, first_name, last_name, email, mobile, month, date, year, country, gender,password):
		self.name=first_name+" "+last_name
		self.email=email
		self.username=username
		self.mobile=mobile
		self.gender=gender
		self.country=country
		self.password=password
		self.dob=date+'-'+month+'-'+year

	def __repr__(self):
		return '<User %r>' % self.name

@app.route("/addUser", methods=['POST'])
def add_user():
	first_name = request.form["first_name"]
	last_name = request.form["last_name"]
	password = request.form["password"]
	username = request.form["username"]
	gender = request.form["gender"]
	country = request.form["country"]
	mobile= request.form["mobile"]
	email = request.form["email"]
	date = request.form["date"]
	month = request.form["month"]
	year = request.form["year"]
	user=User(username,first_name,last_name,email,mobile,month,date,year,country,gender,password)
	db.session.add(user)
	db.session.commit()
	return "You have signed in successfully"

@app.route("/", methods=['GET'])
def home():
	return render_template('home.html')

@app.route("/homepage", methods=['GET'])
def homepage():
	return render_template('homepage.html')

@app.route("/reset", methods=['GET'])
def reset():
	return render_template('reset.html')

@app.route('/resetpassword', methods=['POST'])
def re():
	username=request.form['username']
	newp=request.form['password']
	user=User.query.filter(User.username==username).first()
	user.password=newp
	db.session.commit()
	return redirect('/')

@app.route("/users", methods=['GET'])
def get_users():
	user=User.query.all()
	arr=[]
	for i in user:
		y={}
		y["username"]=i.username
		y["email"]=i.email
		arr.append(y)
	return jsonify(arr)

db.create_all()
if __name__ == "__main__":
    app.run(debug=True)
