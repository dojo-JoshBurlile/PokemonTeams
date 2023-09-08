from flask_app import app
from flask_app.controllers import user_controller, pokemon_controller
from flask import render_template, redirect, request, session, flash
from flask_app.models import team_model, pokemon_model, user_model

@app.route('/new_team')
def add_team():
    return render_template('new_team.html')

@app.route('/create_team', methods=['POST'])
def create_team():
    team_model.Team.create_new_team(request.form)
    return redirect('/new_team')