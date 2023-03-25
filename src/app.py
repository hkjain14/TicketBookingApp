from flask import Flask, render_template, redirect, request, url_for
from src.models import *

app = Flask(__name__)

db.init_app(app)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabom.sqlite3"

### Root Routes
@app.route('/', methods = ['GET'])
def root():
    return render_template('root_view.html')

@app.route('/', methods = ['POST'])
def postRoot():
    user_type = request.form.get('user_type')
    if user_type == "User Login":
        return redirect('/login/user')
    return redirect('/login/admin')


### Login Routes

@app.route('/register', methods = ['GET'])
def registerUser():
    return render_template('user_register.html')

@app.route('/register', methods = ['POST'])
def registerUserPost():
    username = request.form.get('username')
    password = request.form.get('password')
    users = User.query.filter_by(user_username=username).all()
    if users != []:
        # TODO : Show error that already registered credentials
        return redirect('/register')
    user = User(user_username = username, user_password = password)
    db.session.add(user)
    db.session.commit()
    return redirect('/login/user')

@app.route('/login/user', methods = ['GET'])
def loginUser():
    return render_template('user_login.html')

@app.route('/login/user', methods = ['POST'])
def loginUserPost():
    login_type = request.form.get('login_type')
    if login_type == "Register":
        return redirect('/register')
    username = request.form.get('username')
    password = request.form.get('password')
    users = User.query.filter_by(user_username=username).all()
    if users != [] and users[0].user_password == password:
        return redirect(url_for('.viewUser', username=users[0].user_username))
    # TODO : Show error that wrong credentials
    return redirect('/login/user')

@app.route('/login/admin', methods = ['GET'])
def loginAdmin():
    return render_template('admin_login.html')

@app.route('/login/admin', methods = ['POST'])
def loginAdminPost():
    username = request.form.get('username')
    password = request.form.get('password')
    admin = Admin.query.all()[0]
    if(username == admin.admin_username and password == admin.admin_password):
        return redirect(url_for('.viewAdmin', username=admin.admin_username))
    # TODO: Show error that wrong credentials
    return redirect('/login/admin')


### Admin view
@app.route('/admin', methods = ['GET'])
def viewAdmin():
    return render_template('admin_view.html', admin_username=request.args['username'])

### User view
@app.route('/user', methods = ['GET'])
def viewUser():
    return render_template('user_view.html', user_username=request.args['username'])


if __name__ == "__main__":
    db.create_all()
    admins = Admin.query.all()
    if admins == []:
        admin = Admin(admin_username='ashish', admin_password='gaba')
        db.session.add(admin)
        db.session.commit()
    app.run(debug=False)