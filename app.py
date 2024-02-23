from flask import Flask, render_template, request, redirect, url_for, flash
from forms import LoginForm, SignupForm
from models import db, User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Initializing Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'generated-secret-key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:%rxUXm*4H3p~80z@localhost/login'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/forecast')
def home():
    if current_user.is_authenticated:
        # User is logged in, display welcome message
        return render_template('forecast.html', username=current_user.username)
    else:
        # User is not logged in, redirect to login page
        flash('Please log in to access the home page.', 'info')
        return redirect(url_for('login'))
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Check if the username is already taken
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'username-taken')
        else:
            # If the username is unique, create a new user
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully. You can now log in!', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
