from flask import Flask, render_template, flash, redirect, url_for, \
	request, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, \
	validators, RadioField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from passlib.hash import sha256_crypt
from flask_script import Manager
from functools import wraps
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

username = 'tania'
password = '123456'
database = 'gymdb'

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@localhost:5432/{database}"
db = SQLAlchemy(app)


class Info(db.Model):
  __tablename__ = 'info'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), unique=True, nullable=False)
  name = db.Column(db.String(120), nullable=False)
  prof = db.Column(db.Integer, nullable=False)
  street = db.Column(db.String(100), nullable=True)
  city = db.Column(db.String(100), nullable=True)
  phone = db.Column(db.String(100), nullable=True)

  @staticmethod
  def to_json_info(data):
	  return {
		  'username': data.username,
		  'password': data.password,
		  'name': data.name,
		  'prof': data.prof,
		  'street': data.street,
		  'city': data.city,
		  'phone': data.phone,
	  }

  @classmethod
  def return_by_username(cls,username):
	  return list(map(lambda x: cls.to_json_info(x), Info.query.filter_by(username=username).all()))

  @classmethod
  def find_by_username(cls, username):
	  return cls.query.filter_by(username=username).first()

  def __init__(self, username, password,name,prof,street,city,phone):
    self.username = username
    self.password = password
    self.name = name
    self.prof = prof
    self.street = street
    self.city = city
    self.phone = phone


class Plan(db.Model):
  __tablename__ = 'plans'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  exercise = db.Column(db.String(120), nullable=False)
  reps = db.Column(db.String(120), nullable=False)
  sets = db.Column(db.String(120), nullable=False)

  @staticmethod
  def to_json_plan(data):
	  return {
		  'name': data.name,

	  }

  @classmethod
  def return_values_by_name(cls, name):
	  return list(map(lambda x: cls.to_json_plan(x),
					  Plan.query.with_entities(Plan.exercise, Plan.reps, Plan.sets).filter_by(name=name).all()))

  @classmethod
  def return_plans(cls, name, exercise):
	  return list(map(lambda x: cls.to_json_plan(x), Plan.query.with_entities(Plan.name, Plan.exercise).filter_by(name=name, exercise= exercise).all()))

  @classmethod
  def find_by_name(cls, name):
	  return cls.query.Info.query.with_entities(Plan.exercise, Plan.reps, Plan.sets).filter_by(name=name).first()

  @classmethod
  def return_all(cls):
	  return list(map(lambda x: cls.to_json_plan(x), Plan.query.with_entities(Plan.name).all()))

  def __init__(self, name, exercise, reps, sets):
	  self.name = name,
	  self.exercise = exercise,
	  self.reps = reps,
	  self.sets = sets

class Recep(db.Model):
  __tablename__ = 'receps'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(120), nullable=False)
  plan = db.Column(db.String(120), nullable=False)
  trainor = db.Column(db.String(120), nullable=False)

  @staticmethod
  def to_json_recap(data):
	  return {
		  'username': data.username,
		  'plan': data.plan,
		  'trainor': data.trainor
	  }

  @classmethod
  def return_all(cls):
	  return list(map(lambda x: cls.to_json_recap(x), Recep.query.with_entities(Recep.username).all()))

  def __init__(self, username,plan,trainor):
	  self.username = username,
	  self.plan = plan,
	  self.trainor = trainor



class Trainor(db.Model):
  __tablename__ = 'trainors'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(120), nullable=False)
  @staticmethod
  def to_json_trainer(data):
	  return {
		  'username': data.username,
	  }

  @classmethod
  def return_all(cls):
	  return list(map(lambda x: cls.to_json_trainer(x), Trainor.query.with_entities(Trainor.username).all()))

  def __init__(self, username):
    self.username = username

class Equipment(db.Model):
  __tablename__ = 'equip'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  count = db.Column(db.String(120), nullable=False)

  @staticmethod
  def to_json_equip(data):
	  return {
		  'name': data.name,
		  'count' : data.count
	  }

  @classmethod
  def find_by_name_count(cls):
	  return list(map(lambda x: cls.to_json_equip(x), Equipment.query.with_entities(Equipment.name,Equipment.count).all()))

  @classmethod
  def find_by_name(cls, name):
	  return cls.query.filter_by(name=name).first()

  @classmethod
  def return_all(cls):
	  return list(map(lambda x: cls.to_json_equip(x), Equipment.query.with_entities(Equipment.name).all()))

  def __init__(self, name, count):
    self.name = name
    self.count = count


class Member(db.Model):
  __tablename__ = 'members'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(120), nullable=False)
  plan = db.Column(db.String(120), nullable=False)
  trainor = db.Column(db.String(120), nullable=False)

  @staticmethod
  def to_json_member(data):
	  return {
		  'username': data.username,
		  'plan': data.plan,
		  'trainor': data.trainor,
	  }

  @classmethod
  def find_plan_by_username(cls, username):
	  data = cls.query.with_entities(Member.plan).filter_by(username=username).first()
	  return cls.to_json_member(data)

  @classmethod
  def find_by_trainor(cls, username):
	  return list(map(lambda x: cls.to_json_member(x), Member.query.with_entities(Member.username).filter_by(trainor=username).all()))

  @classmethod
  def return_all(cls):
	  return list(map(lambda x: cls.to_json_member(x), Member.query.with_entities(Member.username).all()))

  def __init__(self, username,plan,trainor):
    self.username = username
    self.plan = plan
    self.trainor = trainor

class Progress(db.Model):
  __tablename__ = 'progress'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(120), nullable=False)
  date = db.Column(db.String(120), nullable=False)
  daily_result = db.Column(db.String(120), nullable=False)

  @staticmethod
  def to_json_progress(data):
	  return {
		  'username': data.username,
		  'date': data.date,
		  'daily_result': data.daily_result,
	  }

  @classmethod
  def find_vlaues_by_username(cls, username):
	  return list(map(lambda x: cls.to_json_member(x),
					  Member.query.with_entities(Progress.date,Progress.daily_result,Progress.rate).filter_by(username=username).order_by(desc(Progress.date)).all()))

  @classmethod
  def find_by_username(cls, username):
	  return list(map(lambda x: cls.to_json_member(x),
					  Member.query.with_entities(Progress.date).filter_by(username=username).all()))

  @classmethod
  def return_all(cls):
	  return list(map(lambda x: cls.to_json_progress(x), Progress.query.with_entities(Progress.username).all()))

  def __init__(self, username,date,daily_result):
    self.username = username
    self.date = date
    self.daily_result = daily_result

db.create_all()



def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Nice try, Tricks don\'t work, bud!! Please Login :)', 'danger')
			return redirect(url_for('login'))
	return wrap

def is_trainor(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['prof'] == 3:
			return f(*args, **kwargs)
		else:
			flash('You are probably not a trainor!!, Are you?', 'danger')
			return redirect(url_for('login'))
	return wrap

def is_admin(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['prof'] == 1:
			return f(*args, **kwargs)
		else:
			flash('You are probably not an admin!!, Are you?', 'danger')
			return redirect(url_for('login'))
	return wrap

def is_recep_level(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['prof'] <= 2:
			return f(*args, **kwargs)
		else:
			flash('You are probably not an authorised to view that page!!', 'danger')
			return redirect(url_for('login'))
	return wrap


@app.route('/')
def index():
	return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password_candidate = request.form['password']


		result = Info.query.filter_by(username=username).first()
		print(sha256_crypt.encrypt(str(password_candidate))) # for get the encript password get
		if result:

			if sha256_crypt.verify(password_candidate, result.password):
				session['logged_in'] = True
				session['username'] = username
				session['prof'] = result.prof
				#session['hash'] = sha256_crypt.encrypt(username)
				flash('You are logged in', 'success')
				if session['prof'] == 1:
					return redirect(url_for('adminDash'))
				if session['prof'] == 3:
					return redirect(url_for('trainorDash'))
				if session['prof'] == 2:
					return redirect(url_for('recepDash'))
				#s = 'memberDash/%s', (username)
				return redirect(url_for('memberDash', username = username))
			else:
				error = 'Invalid login'
				return render_template('login.html', error = error)

		else:
			error = 'Username NOT FOUND'
			return render_template('login.html', error = error)

	return render_template('login.html')


class ChangePasswordForm(Form):
	old_password = PasswordField('Existing Password')
	new_password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message = 'Passwords aren\'t matching pal!, check \'em')
	])
	confirm = PasswordField('Confirm Password')


@app.route('/update_password/<string:username>', methods = ['GET', 'POST'])
def update_password(username):
	form = ChangePasswordForm(request.form)
	if request.method == 'POST' and form.validate():
		new = form.new_password.data
		entered = form.old_password.data
		cur = mysql.connection.cursor()
		cur.execute("SELECT password FROM info WHERE username = %s", [username])
		old = (cur.fetchone())['password']
		if sha256_crypt.verify(entered, old):
			cur.execute("UPDATE info SET password = %s WHERE username = %s", (sha256_crypt.encrypt(new), username))
			mysql.connection.commit()
			cur.close()
			flash('New password will be in effect from next login!!', 'info')
			return redirect(url_for('memberDash', username = session['username']))
		cur.close()
		flash('Old password you entered is wrong!!, try again', 'warning')
	return render_template('updatePassword.html', form = form)

@app.route('/adminDash')
@is_logged_in
@is_admin
def adminDash():
	return render_template('adminDash.html')

values = []
choices = []

class AddTrainorForm(Form):
	name = StringField('Name', [validators.Length(min = 1, max = 100)])
	username = StringField('Username', [validators.InputRequired(), validators.NoneOf(values = values, message = "Username already taken, Please try another")])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message = 'Passwords aren\'t matching pal!, check \'em')
	])
	confirm = PasswordField('Confirm Password')
	street = StringField('Street', [validators.Length(min = 1, max = 100)])
	city = StringField('City', [validators.Length(min = 1, max = 100)])
	prof = 2
	phone = StringField('Phone', [validators.Length(min = 1, max = 100)])


@app.route('/addTrainor', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def addTrainor():
	values.clear()
	# cur = mysql.connection.cursor()
	# q = cur.execute("SELECT username FROM info")
	# b = cur.fetchall()
	# for i in range(q):
	# 	values.append(b[i]['username'])
	#app.logger.info(b[0]['username'])
	#res = values.fetchall()
	#app.logger.info(res)
	#cur.close()
	form = AddTrainorForm(request.form)
	if request.method == 'POST' and form.validate():
		#app.logger.info("setzdgxfhcgjvkhbjlkn")
		name = form.name.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		street = form.street.data
		city = form.city.data
		prof = 2
		phone = form.phone.data
		
		info = Info(username=username,
		 password=password,
		 name=name,
		 prof=prof,
		 street=street,
		 city=city,
		 phone=phone)
		db.session.add(info)
		trainor = Trainor(username=username)
		db.session.add(trainor)
		db.session.commit()
		flash('You recruited a new Trainor!!', 'success')
		return redirect(url_for('adminDash'))
	return render_template('addTrainor.html', form=form)



class DeleteRecepForm(Form):
	username = SelectField(u'Choose which one you wanted to delete', choices=choices)



@app.route('/deleteTrainor', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def deleteTrainor():
	choices.clear()
	trainers = Trainor.return_all()
	for i in trainers:
		tup = (i['username'],i['username'])
		choices.append(tup)
	form = DeleteRecepForm(request.form)
	if len(choices)==1:
		flash('You cannot remove your only Trainor!!', 'danger')
		return redirect(url_for('adminDash'))
	if request.method == 'POST':
		#app.logger.info(form.username.data)
		username = form.username.data
		q = db.engine.execute("SELECT username FROM trainors WHERE username != %s", [username])
		b = q.all()
		new = b[0]['username']
		db.engine.execute("UPDATE members SET trainor = %s WHERE trainor = %s", (new, username))
		db.engine.execute("DELETE FROM trainors WHERE username = %s", [username])
		db.engine.execute("DELETE FROM info WHERE username = %s", [username])
		db.session.commit()
		db.session.close()
		choices.clear()
		flash('You removed your Trainor!!', 'success')
		return redirect(url_for('adminDash'))
	return render_template('deleteRecep.html', form = form)


@app.route('/addRecep', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def addRecep():
	form = AddTrainorForm(request.form)
	if request.method == 'POST' and form.validate():
		#app.logger.info("setzdgxfhcgjvkhbjlkn")
		name = form.name.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		street = form.street.data
		city = form.city.data
		phone = form.phone.data

		info = Info(username=username,
		 password=password,
		 name=name,
		 prof=1,
		 street=street,
		 city=city,
		 phone=phone)
		db.session.add(info)
		trainor = Recep(username=username)
		db.session.add(trainor)
		db.session.commit()

		flash('You recruited a new Receptionist!!', 'success')
		return redirect(url_for('adminDash'))
	return render_template('addRecep.html', form=form)

class DeleteRecepForm(Form):
	username = SelectField(u'Choose which one you wanted to delete', choices=choices)



@app.route('/deleteRecep', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def deleteRecep():
	choices.clear()

	recaps = Recep.return_all()
	for i in recaps:
		tup = (i['username'], i['username'])
		choices.append(tup)
	if len(choices)==1:
		flash('You cannot remove your only receptionist!!', 'danger')
		return redirect(url_for('adminDash'))
	form = DeleteRecepForm(request.form)
	if request.method == 'POST':
		#app.logger.info(form.username.data)
		username = form.username.data
		db.engine.execute("DELETE FROM receps WHERE username = %s", [username])
		db.engine.execute("DELETE FROM info WHERE username = %s", [username])
		db.session.commit()
		db.session.close()
		choices.clear()
		flash('You removed your receptionist!!', 'success')
		return redirect(url_for('adminDash'))
	return render_template('deleteRecep.html', form = form)


class AddEquipForm(Form):
	name = StringField('Name', [validators.Length(min = 1, max = 100)])
	count = IntegerField('Count', [validators.NumberRange(min = 1, max = 25)])


@app.route('/addEquip', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def addEquip():
	form = AddEquipForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		count = form.count.data
		equips = []
		getDatas = Equipment.return_all()
		for i in getDatas:
			tup = (i['name'], i['name'])
			equips.append(tup)
		if name in equips:
			db.engine.execute("UPDATE equip SET count = count+%s WHERE name = %s", (count, name))
		else:
			db.engine.execute("INSERT INTO equip(name, count) VALUES(%s, %s)", (name, count))
		db.session.commit()
		db.session.close()
		flash('You added a new Equipment!!', 'success')
		return redirect(url_for('adminDash'))
	return render_template('addEquip.html', form = form)

class RemoveEquipForm(Form):
	name = RadioField('Name', choices = choices)
	count = IntegerField('Count', [validators.InputRequired()])


@app.route('/removeEquip', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def removeEquip():
	choices.clear()
	getDatas = Equipment.return_all()
	for i in getDatas:
		tup = (i['name'], i['name'])
		choices.append(tup)
	form = RemoveEquipForm(request.form)
	#num = data['count']
	if request.method == 'POST' and form.validate():
		data = Equipment.find_by_name([form.name.data])
		app.logger.info(data['count'])
		num = data['count']
		if num >= form.count.data and form.count.data>0:
			name = form.name.data
			count = form.count.data
			db.engine.execute("UPDATE equip SET count = count-%s WHERE name = %s", (count, name))
			db.session.commit()
			db.session.close()
			choices.clear()
			flash('You successfully removed some of your equipment!!', 'success')
			return redirect(url_for('adminDash'))
		else:
			flash('you must enter valid number', 'danger')
	return render_template('removeEquip.html', form = form)

choices2 = []
plans = []
plansdata = Plan.return_all()
for i in plansdata:
	plans.append(i['name'])


trainordata = Trainor.return_all()
for i in trainordata:
	choices2.append(i['username'])
class AddMemberForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.InputRequired(), validators.NoneOf(values = values, message = "Username already taken, Please try another")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    plan  = RadioField('Select Plan', choices = plans)
    trainor = SelectField('Select Trainor', choices = choices2)
    street = StringField('Street', [validators.Length(min = 1, max = 100)])
    city = StringField('City', [validators.Length(min = 1, max = 100)])
    phone = StringField('Phone', [validators.Length(min = 1, max = 100)])


@app.route('/addMember', methods = ['GET', 'POST'])
@is_logged_in
@is_recep_level
def addMember():

	form = AddMemberForm(request.form)
	if request.method == 'POST' and form.validate():

		name = form.name.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		street = form.street.data
		city = form.city.data
		phone = form.phone.data
		plan = form.plan.data
		trainor = form.trainor.data

		info = Info(username=username,
		 password=password,
		 name=name,
		 prof=1,
		 street=street,
		 city=city,
		 phone=phone)
		db.session.add(info)
		trainor = Recep(username=username,plan=plan,trainor=trainor)
		db.session.add(trainor)
		db.session.commit()
		flash('You added a new member!!', 'success')
		if(session['prof']==1):
			return redirect(url_for('adminDash'))
		return redirect(url_for('recepDash'))
	return render_template('addMember.html', form=form)


@app.route('/deleteMember', methods = ['GET', 'POST'])
@is_logged_in
@is_recep_level
def deleteMember():
	choices.clear()
	member = Member.return_all()
	for i in member:
		tup = (i['username'], i['username'])
		choices.append(tup)
	form = DeleteRecepForm(request.form)
	if request.method == 'POST':
		username = form.username.data
		db.engine.execute("DELETE FROM members WHERE username = %s", [username])
		db.engine.execute("DELETE FROM info WHERE username = %s", [username])
		db.session.commit()
		db.session.close()
		choices.clear()
		flash('You deleted a member from the GYM!!', 'success')
		if(session['prof']==1):
			return redirect(url_for('adminDash'))
		return redirect(url_for('recepDash'))
	return render_template('deleteRecep.html', form = form)

@app.route('/viewDetails')
def viewDetails():
	getDatas = Info.return_by_username(session['username'])

	return render_template('viewDetails.html', result = getDatas)


@app.route('/recepDash')
@is_recep_level
def recepDash():
	return render_template('recepDash.html')

class trainorForm(Form):
	name = RadioField('Select Username', choices = choices)
	date = DateField('Date', format='%Y-%m-%d')
	report = StringField('Report', [validators.InputRequired()])
	rate = RadioField('Result', choices = [('good', 'good'),('average', 'average'),('poor', 'poor') ])


@app.route('/trainorDash', methods = ['GET', 'POST'])
@is_logged_in
@is_trainor
def trainorDash():
	choices.clear()
	equips = Equipment.find_by_name_count()
	#app.logger.info(equips)
	members_under = Member.find_by_trainor(session['username'])

	members = Member.find_by_trainor(session['username'])

	for i in members:
		tup = (i['username'],i['username'])
		choices.append(tup)


	form = trainorForm(request.form)

	if request.method == 'POST':
		date = form.date.data
		username = form.name.data
		report = form.report.data
		rate = form.rate.data
		if rate == 'good':
			rate = 1
		elif rate == 'average':
			rate = 2
		else:
			rate = 3
		#app.logger.info(request.form.input_date)
		#app.logger.info(date)
		if datetime.now().date()<date:
			flash('You cannot predict furture, buoy!!', 'warning')
			choices.clear()
			return redirect(url_for('trainorDash'))

		progresses = Progress.find_by_username([username])
		entered = []
		for i in progresses:
			entered.append(i['date'])
		

		if date in entered:
			db.engine.execute("UPDATE progress SET daily_result = %s, rate = %s WHERE username = %s and date = %s", (report,rate, username, date))
			db.session.commit()
			db.session.close()
			choices.clear()
			flash('Succesfully updated!', 'success')
			return redirect(url_for('trainorDash'))
		

		cur.execute("INSERT INTO progress(username, date, daily_result, rate) VALUES(%s, %s, %s, %s)", (username, date, report, rate))
		mysql.connection.commit()
		cur.close()
		choices.clear()
		flash('Progress updated and Reported', 'info')
		return redirect(url_for('trainorDash'))

	return render_template('trainorDash.html', equips = equips, form = form, members = members_under)


class UpdatePlanForm(Form):
    name = StringField('Plan Name', [validators.Length(min=1, max=50)])
    exercise = StringField('Exercise', [validators.Length(min = 1, max = 100)])
    reps = IntegerField('Reps', [validators.NumberRange(min = 1, max = 20)])
    sets = IntegerField('Sets', [validators.NumberRange(min = 1, max = 20)])


@app.route('/updatePlans', methods = ['GET', 'POST'])
@is_trainor
def updatePlans():
	form = UpdatePlanForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		exercise = form.exercise.data
		reps = form.reps.data
		sets = form.sets.data
		result = Plan.return_plans(name,exercise)
		if len(result)>0:
			db.engine.execute("UPDATE plans SET sets=%s, reps= %s WHERE name = %s and exercise = %s", (sets, reps, name, exercise))
		else:
			db.engine.execute("INSERT INTO plans(name, exercise, sets, reps) VALUES(%s, %s, %s, %s)", (name, exercise, sets, reps))
		db.session.commit()
		db.session.close()
		flash('You have updated the plan schemes', 'success')
		return redirect(url_for('trainorDash'))
	return render_template('addPlan.html', form = form)



@app.route('/memberDash/<string:username>')
@is_logged_in
def memberDash(username):
	if session['prof']==4 and username!=session['username']:
		flash('You aren\'t authorised to view other\'s Dashboards', 'danger')
		return redirect(url_for('memberDash', username = session['username']))
	plan = Member.find_plan_by_username([username])
	scheme = Plan.return_values_by_name([plan])

	progresses = Progress.find_vlaues_by_username([username])
	result = []
	for i in progresses:
		result.append(int(i['rate']))
	good = result.count(1)
	poor = result.count(3)
	average = result.count(2)
	total = good + poor + average
	good = round((good / total) * 100, 2)
	average = round((average / total) * 100, 2)
	poor = round((poor / total) * 100, 2)
	return render_template('memberDash.html',user = username, plan = plan, scheme = scheme, progress = progress, good = good, poor = poor, average = average)


@app.route('/profile/<string:username>')
@is_logged_in
def profile(username):
	if username == session['username'] or session['prof']==1 or session['prof']==2:
		get_data = Info.find_by_username(username)
		print(username)
		result = get_data.to_json_info(get_data)

		return render_template('profile.html', result = result)
	flash('You cannot view other\'s profile', 'warning')
	if session['prof']==3:
		return redirect(url_for('trainorDash'))
	return redirect(url_for('memberDash', username = username))


class EditForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    street = StringField('Street', [validators.Length(min = 1, max = 100)])
    city = StringField('City', [validators.Length(min = 1, max = 100)])
    phone = StringField('Phone', [validators.Length(min = 1, max = 100)])


@app.route('/edit_profile/<string:username>', methods = ['GET', 'POST'])
@is_logged_in
def edit_profile(username):

	if username != session['username']:
		flash('You aren\'t authorised to edit other\'s details', 'warning')
		if session['prof']==4:
			return redirect(url_for('memberDash', username = username))
		if session['prof']==1:
			return redirect(url_for('adminDash'))
		if session['prof']==2:
			return redirect(url_for('recepDash', username = username))
		if session['prof']==3:
			return redirect(url_for('trainorDash', username = username))

	get_data = Info.find_by_username(username)
	result = get_data.to_json_info(get_data)
	form = EditForm(request.form)
	form.name.data = result['name']
	form.street.data = result['street']
	form.city.data = result['city']
	form.phone.data = result['phone']



	if request.method == 'POST' and form.validate():
		#app.logger.info("setzdgxfhcgjvkhbjlkn")
		name = request.form['name']
		street = request.form['street']
		city = request.form['city']
		phone = request.form['phone']
		app.logger.info(name)
		app.logger.info(street)
		app.logger.info(city)
		q = db.engine.execute("UPDATE info SET name = %s, street = %s, city = %s, phone = %s WHERE username = %s", (name, street, city, phone, username))
		app.logger.info(q)
		db.session.commit()
		db.session.close()
		flash('You successfully updated your profile!!', 'success')
		if session['prof']==4:
			return redirect(url_for('memberDash', username = username))
		if session['prof']==1:
			return redirect(url_for('adminDash'))
		if session['prof']==2:
			return redirect(url_for('recepDash', username = username))
		if session['prof']==3:
			return redirect(url_for('trainorDash', username = username))
	return render_template('edit_profile.html', form=form)


@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = '20ed11b879fd7d1f8c08b075d14dfd8b60824539'
    app.run(debug=True)