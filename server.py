from forms import LoginForm, RegisterForm
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from model import User, db, connect_to_db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, redirect, flash, session, request, url_for


app = Flask(__name__)
app.secret_key = 'dev'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def home():
    return render_template("home.html")


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('home'))


@app.route('/saltlakecityparks')
@login_required
def slcparks():
    return render_template('salt_lake_city_parks.html')

@app.route('/dog_parks')
@login_required
def dogparks():
    return render_template('dog_parks.html')


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.check_password(form.password.data) == True:
            login_user(user)
            flash('Welcome! Your Login was a success!!!')
            print("Correct Username and Password")
            return redirect(url_for('home'))

        else:
            print("Incorrect password")
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('home')
            return redirect(next)

    return render_template('login.html',form=form)


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("We appreciate your registration!")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)



if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)