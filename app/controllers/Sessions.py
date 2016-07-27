from system.core.controller import *

class Sessions(Controller):
    def __init__(self, action):
        super(Sessions, self).__init__(action)
        self.load_model('WelcomeModel')
        self.db = self._app.db

    def main(self):
        return self.load_view('index.html')

    def register(self):
        self.load_model('User')
        userArray = self.models['User'].registerUser(request.form)
        if userArray:
            flash(u'Successful registration! Please login to continue.','success')
            return redirect('/main')
        else:
            flash(u'Failed to register. Password must contain at least one letter, at least one number, and be longer than six charaters.','regerror')
            return redirect('/main')

    def login(self):
        self.load_model('User')
        userArray = self.models['User'].loginUser(request.form)
        if userArray:
            session['currentUser'] = userArray[0]
            return redirect('/pokes')
        else:
            flash(u'Failed to login! Please try again.','logerror')
            return redirect('/main')

    def pokes(self):
        self.load_model('User')
        pokeableArray = self.models['User'].getPokeable(session['currentUser']['id'])
        pokedByArray = self.models['User'].getPokedBy(session['currentUser']['id'])
        return self.load_view('pokes.html', pokeableArray=pokeableArray, pokedByArray=pokedByArray)

    def pokeEm(self, id):
        self.load_model('User')
        self.models['User'].pokeEm(id)
        self.models['User'].addPokey(request.form)
        return redirect('/pokes')



    def logout(self):
        session.pop('currentUser', None)
        return redirect('/main')
