from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import team_model, user_model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    all_teams = team_model.Team.get_all_teams()
    return render_template("dashboard.html", teams = all_teams)

@app.route('/register', methods=['POST'])
def register_user():
    if not user_model.User.validate_reg(request.form):
        return redirect('/')
    
    user_id = user_model.User.save_user(request.form)
    session['user_id'] = user_id
    print(session['user_id'])
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login_user():
    user = user_model.User.validate_login(request.form)
    if not user:
        return redirect('/')
    session['user_id'] = user.id
    print(session['user_id'])
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
        return redirect('/')
