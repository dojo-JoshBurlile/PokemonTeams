from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import team_model

db = "pokemon_teams_schema"
class Pokemon:

    def __init__(self, data) -> None:
        self.id = data['id']
        self.team_id = data['team_id']
        self.pokemon_name = data['pokemon_name']
        self.pokemon_level = data['pokemon_level']
        self.pokemon_species = data['pokemon_species']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_pokemon(cls, data):
        query = "INSERT INTO pokemon (pokemon_name, pokemon_level,pokemon_species, notes, team_id) VALUES (%(pokemon_name)s, %(pokemon_level)s, %(pokemon_species)s, %(notes)s, %(team_id)s);"
        return connectToMySQL(db).query_db(query,data)