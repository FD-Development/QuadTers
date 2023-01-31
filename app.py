from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from Game import Game
import uuid



app = Flask(__name__)
app.secret_key = '1221'

games = {}
def check():
    if 'key' not in session or 'games' not in globals():
        return True
    return False


@app.route('/')
def index():
    if 'key' not in session:
        session['key'] = uuid.uuid4()
    return render_template('index.html')

@app.route('/hotseat',  methods=['POST','GET'])
def hotseat_setup():
    if check() : return redirect('/')
    if request.method == 'POST':
        games[session['key']] = Game(request.form.get('blue'), request.form.get('red'))
        return redirect('/game')
    else:
        return render_template('hotseat_setup.html')

@app.route('/game', methods=['GET','POST'])
def game():
    if check() or session['key'] not in games  : return redirect('/')
    #Conversion to shorter variable names
    game = games[session['key']]
    action = request.form.get('action')
    pos=[request.form.get('y', type=int ),request.form.get('x', type=int)]  #Note. position will always be (y,x)

    # game.victory_check() : redirect('/game/winner')
    if action == 'select' :
        #Prevents form going to previous page and selecting piece
        if pos and game.board.gameboard[pos[0]][pos[1]][1].owner == game.current:
            return render_template('game.html', game=game, turn=game.current, movement=game.select(pos), selected=game.board.gameboard[pos[0]][pos[1]][1])
    if game.selected: #if pawn is selected it allows for other actions
        if action == 'move' : game.move(pos) #next turn | deselects pawn
        elif action == 'powerup' : game.activate_power(request.form.get('powerup'))
        elif action == 'deselect' : game.deselect()
    return render_template('game.html', game=game, turn=game.current)

if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5105, debug=True)
