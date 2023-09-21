from flask_app.config.mysqlconnection import connectToMySQL
from .pokemon_model import Pokemon
# new
from .user_model import User

db = "pokemon_teams_schema"
class Team:
    
    def __init__(self, data):
        self.id = data['id']
        self.team_name = data['team_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # added trainer and list for each pokemon the trainer has
        self.trainer = None
        self.pokemon = []
        
        if 'trainer' in data and data['trainer'] is not None:
            self.trainer = User(data['trainer'])

        if 'pokemon' in data and isinstance(data['pokemon'], list):
            self.pokemon = [Pokemon(pdata) for pdata in data['pokemon']]

    @classmethod
    def get_all_teams(cls):
        query = "SELECT * FROM teams;"
        results = connectToMySQL(db).query_db(query)
        teams = []
        for team in results:
            teams.append(cls(team))
        return teams
    
    @classmethod
    def save_team(cls, data):
        query= "INSERT INTO teams (team_name, user_id) VALUES (%(team_name)s, %(user_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result
    
    @classmethod
    def get_one_with_pokemon(cls, data):
        query = "SELECT * FROM teams LEFT JOIN pokemon on teams.id = pokemon.team_id WHERE teams.id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        first_row = results[0]
        team = cls(first_row)
        if first_row['pokemon.id'] != None:
            for row in results:
        
                poke = {
                    'id': row['pokemon.id'],
                    'pokemon_name': row['pokemon_name'],
                    'pokemon_level': row['pokemon_level'],
                    'age': row['age'],
                    'sprite_url': row['sprite_url'],
                    'created_at': row['pokemon.created_at'],
                    'updated_at': row['pokemon.updated_at'],
                    'team_id': row['id']
                }
                team.pokemon.append(Pokemon(poke))
        return team
    
    @classmethod
    def get_all_teams_with_pokemon(cls):
        query = "SELECT * FROM teams JOIN pokemon ON teams.id = pokemon.team_id;"
        results = connectToMySQL(db).query_db(query)
        teams = []
        for row in results:
            this_team = cls(row)
            pokemon_data = {
                'id': row['id'],
                'team_id' : row['team_id'],
                'pokemon_name': row['pokemon_name'],
                'pokemon_level': row['pokemon_level'],
                'pokemon_species': row['pokemon_species'],
                'notes': row['notes'],
                'sprite_url': row['sprite_url'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            print(pokemon_data)
            this_team.pokemon = Pokemon(pokemon_data)
            teams.append(cls(this_team))
        return teams
    
    @classmethod
    def get_all_teams_with_users_and_pokemon(cls):
        query = """
        SELECT * FROM teams 
        JOIN users ON teams.user_id = users.id
        LEFT JOIN pokemon ON teams.id = pokemon.team_id;
        """
        results = connectToMySQL(db).query_db(query)
        team_data_dict = {}

        for row in results:
            # for key in row.keys():
            #     print(key)
            
            team_id = row['id']

            if team_id not in team_data_dict:
            # Create a new team dictionary if it doesn't exist
                team_data_dict[team_id] = {
                    'id': team_id,
                    'team_name': row['team_name'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                    'trainer': None,
                    'pokemon': []
                }

            # Add the user data to the team if it doesn't have a trainer yet
            if team_data_dict[team_id]['trainer'] is None:
                team_data_dict[team_id]['trainer'] = {
                    'id': row['users.id'],
                    'email': row['email'],
                    'username': row['username'],
                    'password': '',
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
        
            # Add the Pokémon data to the team's Pokémon list
            if row['pokemon.id'] is not None:
                pokemon_data = {
                    'id': row['pokemon.id'],
                    'team_id': row['team_id'],
                    'pokemon_name': row['pokemon_name'],
                    'pokemon_level': row['pokemon_level'],
                    'pokemon_species': row['pokemon_species'],
                    'notes': row['notes'],
                    'sprite_url': row['sprite_url'],
                    'created_at': row['pokemon.created_at'],
                    'updated_at': row['pokemon.updated_at'],
                }
                team_data_dict[team_id]['pokemon'].append(pokemon_data)

        # Create Team objects and append them to the list
        teams = [cls(data) for data in team_data_dict.values()]

        return teams
            # teams.append(new_team)
        #     # Create Pokemon object and add it to the team
        #     pokemon_data = {
        #         'id': row['pokemon.id'],
        #         'team_id': row['team_id'],
        #         'pokemon_name': row['pokemon_name'],
        #         'pokemon_level': row['pokemon_level'],
        #         'pokemon_species': row['pokemon_species'],
        #         'notes': row['notes'],
        #         'created_at': row['pokemon.created_at'],
        #         'updated_at': row['pokemon.updated_at'],
        #     }
        #     new_team.pokemon.append(Pokemon(pokemon_data))
        #     # Create Trainer object if not already created for the team
        #     if new_team.trainer is None:
        #         user_data = {
        #             'id': row['users.id'],
        #             'email': row['email'],
        #             'username': row['username'],
        #             'password': '',
        #             'created_at': row['users.created_at'],
        #             'updated_at': row['users.updated_at'],
        #         }
        #         new_team.trainer = User(user_data)
            
        # return teams

# this_team = cls(row)
#             pokemon_data = {
#                 'id': row['pokemon.id'],
#                 'team_id' : row['pokemon.team_id'],
#                 'pokemon_name': row['pokemon_name'],
#                 'pokemon_level': row['pokemon_level'],
#                 'pokemon_species': row['pokemon_species'],
#                 'notes': row['notes'],
#                 'created_at': row['pokemon.created_at'],
#                 'updated_at': row['pokemon.updated_at'],
#             }
#             print(pokemon_data)
#             user_data = {
#                 'id': row['users.id'],
#                 'email': row['email'],
#                 'username': row['username'],
#             }
#             this_team.pokemon = Pokemon(pokemon_data)
#             this_team.trainer = User(user_data)
#             teams.append(cls(this_team))