from flask_app.config.mysqlconnection import connectToMySQL

db = "pokemon_teams_schema"
class Team:
    
    def __init__(self, data):
        self.id = data['id']
        self.team_name = data['team_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pokemon = []

    @classmethod
    def get_all_teams(cls):
        query = "SELECT * FROM teams;"
        results = connectToMySQL(db).query_db(query)
        teams = []
        for team in results:
            teams.append(cls(team))
        return teams
    
    @classmethod
    def create_new_team(cls, data):
        query = "INSERT INTO teams (team_name, user_id) VALUES (%(team_name)s, 1)"
        result = connectToMySQL(db).query_db(query, data)
        return result