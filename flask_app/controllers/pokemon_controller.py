from flask_app import app
from flask_app.controllers import user_controller, team_controller
from flask import render_template, redirect, request, session, flash
from flask_app.models import team_model, pokemon_model, user_model

@app.route('/add_pokemon')
def add_pokemon():
    all_teams = team_model.Team.get_all_teams()
    return render_template('add_pokemon.html', teams = all_teams)

@app.route('/create_pokemon', methods=['POST'])
def create_pokemon():
    pokemon_model.Pokemon.save_pokemon(request.form)
    return redirect('/add_pokemon')