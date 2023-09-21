from flask_app import app
from flask_app.controllers import user_controller, pokemon_controller
from flask import render_template, redirect, request, session, jsonify
from flask_app.models import team_model, pokemon_model, user_model
import requests

@app.route('/new_team')
def new_team():
    # Adding session check for a logged in user
    if 'user_id' not in session:
        return redirect('/')

    # teams = team_model.Team.get_all_teams()
    teams = team_model.Team.get_all_teams_with_users_and_pokemon()
    print(teams)
    return render_template('new_team.html', all_teams = teams)

@app.route('/create_team', methods = ['POST'])
def create_team():
    # Adding session check for a logged in user
    if 'user_id' not in session:
        return redirect('/')
    # Adding a data dictionary to allow for passing the user_id
    data = {
        'user_id': session['user_id'],
        'team_name': request.form['team_name']
    }
    team_model.Team.save_team(data)
    return redirect('/add_pokemon')

@app.route('/my_teams')
def view_my_teams():
    # Adding session check for a logged in user
    if 'user_id' not in session:
        return redirect('/')
    teams = team_model.Team.get_all_teams_with_users_and_pokemon()
    return render_template('my_teams.html', my_teams = teams)

@app.route('/team/<int:id>')
def view_one_team():
    # Adding session check for a logged in user
    if 'user_id' not in session:
        return redirect('/')
    one_team = team_model.Team.get_one_with_pokemon()
    return render_template('my_teams.html', team = one_team)

@app.route('/get_data')
def get_data():

    return jsonify(message="Hello World")
