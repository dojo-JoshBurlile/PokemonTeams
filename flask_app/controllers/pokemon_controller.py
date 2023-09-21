from flask_app import app
from flask_app.controllers import user_controller, team_controller
from flask import render_template, redirect, request, session, flash
from flask_app.models import team_model, pokemon_model, user_model
import requests

@app.route('/add_pokemon')
def add_pokemon():
    # Adding session check for a logged in user
    if 'user_id' not in session:
        return redirect('/')
    all_teams = team_model.Team.get_all_teams()
    # Define the API endpoint URL
    names_list_url = 'https://pokeapi.co/api/v2/pokemon/?limit=151'

    # Send an HTTP GET request to the API endpoint
    response = requests.get(names_list_url)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print(data)
        # Access the "results" key to get the list of Pokémon dictionaries
        pokemon_list = data['results']
        # Create an empty list to store all the names of the pokemon we need
        form_list = []
        # Iterate through the results list to find the keys that contain Pokemon names
        for pokemon in pokemon_list:
            print(pokemon['name'])
            # Append all those names to a list we can use in Jinja
            form_list.append(pokemon['name'])
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    # pokemon_name = pokemon_list['name']
    # , pokemon_list['sprites']['front_default']
    #  pokemon_name = pokemon_name
    return render_template('add_pokemon.html', teams = all_teams, pokemon_names=form_list)

@app.route('/create_pokemon',methods=['POST'])
def create_pokemon():
    # Adding session check for a logged in user
    if 'user_id' not in session:
        return redirect('/')
    
    pokemon_model.Pokemon.save_pokemon(request.form)
    return redirect('/add_pokemon')