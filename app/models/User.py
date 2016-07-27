from system.core.model import Model

import re

NAME_REGEX = re.compile(r'^[a-zA-Z]')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASS_REGEX = re.compile(r'^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{6,}$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def registerUser(self, userData):
        hasErrors = False
        if len(userData['email']) < 2:
            hasErrors = True
        elif not EMAIL_REGEX.match(userData['email']):
            hasErrors = True
        elif not NAME_REGEX.match(userData['name']):
            hasErrors = True
        elif not NAME_REGEX.match(userData['alias']):
            hasErrors = True
        elif not PASS_REGEX.match(userData['password']):
            hasErrors = True
        elif userData['password'] != userData['confirm_password']:
            hasErrors = True
        elif userData['dob'] == None:
            hasErrors = True
        elif hasErrors == True:
            return False
        else:
            query = 'INSERT INTO users (name, alias, email, password, dob, poke_history) VALUES (:name, :alias, :email, :password, :dob, :poke_history)'
            data = {
                'name': userData['name'],
                'alias': userData['alias'],
                'email': userData['email'],
                'password': userData['password'],
                'dob': userData['dob'],
                'poke_history': 0,
                }
            return self.db.query_db(query, data)

    def loginUser(self, userData):
        hasErrors = False
        if len(userData['email']) < 2:
            hasErrors = True
        elif not EMAIL_REGEX.match(userData['email']):
            hasErrors = True
        elif hasErrors == False:
            query = "SELECT * FROM users WHERE email = :email AND password = :password"
            data = {'email': userData['email'],'password': userData['password']}
            return self.db.query_db(query, data)
        else:
            return False

    def getPokeable(self, userId):
        query = 'SELECT u.id, u.name, u.alias, u.email, u.poke_history FROM users u WHERE u.id != :userId ORDER BY u.poke_history DESC'
        data = {'userId': userId}
        return self.db.query_db(query, data)

    def pokeEm(self, userId):
        query = 'UPDATE users SET poke_history = poke_history + 1 WHERE id = :userId'
        data = {'userId': userId}
        return self.db.query_db(query, data)

    def addPokey(self, userData):
        query = 'INSERT INTO pokes (users_id, pokey_id) VALUES (:usersId, :pokeyId)'
        data = {'usersId': userData['usersId'], 'pokeyId': userData['pokeyId']}
        self.db.query_db(query, data)

    def getPokedBy(self, userId):
        query = 'SELECT count(pokey_id), pokers.alias AS poker_alias FROM users LEFT JOIN pokes ON pokes.users_id = users.id LEFT JOIN users AS pokers ON pokers.id = pokes.pokey_id WHERE users.id = :userId GROUP BY pokey_id ASC;'
        data = {'userId': userId}
        return self.db.query_db(query, data)
