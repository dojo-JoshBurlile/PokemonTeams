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
        self.sprite_url = data['sprite_url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.trainer = None

    @classmethod
    def save_pokemon(cls,data):
        query = "INSERT INTO pokemon (pokemon_name, pokemon_level,pokemon_species, notes, sprite_url, team_id) VALUES (%(pokemon_name)s, %(pokemon_level)s, %(pokemon_species)s, %(notes)s, %(sprite_url)s, %(team_id)s);"
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def get_one_by_id(cls, pokemon_id):
        # query for a pokemon
        query = """SELECT * from pokemon
        WHERE id = %(team_id)s"""
        data = {
            "pokemon_id": pokemon_id
        }
        # make a pokemon object... BUT must have the team id
        result_list = connectToMySQL(db).query_db(query, data)
        pokemon = cls(result_list[0])
        return pokemon
    
    @classmethod
    def delete_by_id(cls, pokemon_id):
        query = """DELETE from pokemon
        WHERE id = %(pokemon_id)s;"""

        data = {
            "pokemon_id": pokemon_id
        }
        connectToMySQL(db).query_db(query, data)
        return pokemon_id
    
    @classmethod
    def update_pokemon(cls, data):
        query = """UPDATE pokemon
        SET pokemon_name = %(pokemon_name)s, pokemon_level = %(pokemon_level)s, pokemon_species = %(pokemon_species)s, notes = %(notes)s"""

        connectToMySQL('dojo_ninjas').query_db(query, data)
        return