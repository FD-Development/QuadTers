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
online_games = {}
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
        games[session['key']] = Game(request.form.get('player0'), request.form.get('player1'))
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

    if game.victory_check() : return redirect('/winner')
    if action == 'select' :
        #Prevents form going to previous page and selecting piece
        if pos and game.board.gameboard[pos[0]][pos[1]][1].owner == game.current:
            return render_template('game.html', game=game, turn=game.current, movement=game.select(pos), selected=game.board.gameboard[pos[0]][pos[1]][1])
    if game.selected: #if pawn is selected it allows for other actions
        if action == 'move' : game.move(pos) #next turn | deselects pawn
        elif action == 'powerup' : game.activate_power(request.form.get('powerup'))
        elif action == 'deselect' : game.deselect()
    return render_template('game.html', game=game, turn=game.current)

@app.route('/rooms')
def rooms():
    if check(): return redirect('/')
    return render_template('rooms.html', rooms=online_games)
@app.route('/online_setup', methods=['GET','POST'])
def online_setup():
    if check(): return redirect('/')

    if request.method == 'POST':
        players = request.form.getlist('player')

        print(players)

        return new_online_game(players)
    return render_template('online_setup.html')

def new_online_game(players):
    session['game_uuid'] = str(uuid.uuid4()) #room/game session

    print(session['game_uuid'])

    online_games[session['game_uuid']] = players

    print(online_games[session['game_uuid']])

    return redirect('/waitroom/'+ session['game_uuid'])

@app.route('/join/<uuid>', methods=['GET','POST'])
def join(uuid):
    if check(): return redirect('/')

    print(uuid)
    print(session['game_uuid'])
    print(online_games[uuid])

    if request.method == 'POST':
        player = request.form.get('player')
        game_uuid = request.form.get('uuid')
        if is_full(game_uuid) : redirect('/rooms')
        return join_online_game(player,game_uuid)

    return render_template('join.html', game_uuid=uuid)
def join_online_game(player,game_uuid):
    online_games[game_uuid].append(player) #Joining game
    session['game_uuid'] = game_uuid #Saving game session for the joined player
    print(online_games[game_uuid])
    return redirect('/waitroom/'+game_uuid)

def is_full(game_uuid):
    if len(online_games[game_uuid]) > 2: return True
    else: return False
@app.route('/waitroom/<uuid>')
def waitroom(uuid):
    if check(): return redirect('/')
    ready=False
    if type(online_games[uuid]) == type(list()) and len(online_games[uuid])>1: ready=True
    if type(online_games[uuid]) == Game : return redirect('/match')
    return render_template('waitroom.html',uuid=uuid, ready = ready )
@app.route('/start_match/<uuid>')
def start(uuid):
    if check(): return redirect('/')
    players = online_games[uuid].copy()
    online_games[uuid] = Game(players[0],players[1])
    return redirect('/match')

@app.route('/match', methods=['GET','POST'])
def match():
    if check() or session['game_uuid'] not in online_games  : return redirect('/')
    #Conversion to shorter variable names
    match = online_games[session['game_uuid']]
    action = request.form.get('action')
    pos=[request.form.get('y', type=int ),request.form.get('x', type=int)]  #Note. position will always be (y,x)

    if match.victory_check() : return redirect('/winner')
    if action == 'select' :
        #Prevents form going to previous page and selecting piece
        if pos and match.board.gameboard[pos[0]][pos[1]][1].owner == match.current:
            return render_template('match.html', game=match, turn=match.current, movement=match.select(pos), selected=match.board.gameboard[pos[0]][pos[1]][1])
    if match.selected: #if pawn is selected it allows for other actions
        if action == 'move' : match.move(pos) #next turn | deselects pawn
        elif action == 'powerup' : match.activate_power(request.form.get('powerup'))
        elif action == 'deselect' : match.deselect()
    return render_template('match.html', game=match, turn=match.current)
@app.route('/winner')
def winner():
    if check(): return redirect('/')
    return render_template('winner.html', victor=games[session['key']].current.name)

if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5105, debug=True)
