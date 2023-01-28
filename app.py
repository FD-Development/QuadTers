from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from Powerup import *
from Player import Player



app = Flask(__name__)

class Game:
    def __init__(self, blue, red):
        #Setting players
        self.players = list()
        self.players.append(Player(red))
        self.players.append(Player(blue))
        #Setting powerups
        self.powerups = dict() #Fill out with selected powerups [name : Object]
        #Setting board
        self.board = Board(self.powerups,self.players)

    def select(self, pos):
        #Precautionary measure
        pos[0]=int(pos[0])
        pos[1]=int(pos[1])
        return self.board.move_check(pos)
    def move(self, selected, to):
        #Precautionary measure
        #pos[0]=int(pos[0])
        #pos[1]=int(pos[1])
        #return self.board.move_action(pos)
        pass
class Board:
    def __init__(self, powerups, players):
        '''powerup dictionary, player table'''
        #Generates 8 x 10 array. !!Coordinates are (y,x) (rows,columns)!!
        #The information about contents of a tile in the gameboard are located in gameboard[y][x][0/1/2]
        #Where indexes: 0-Tile obj 1- Pawn obj  2- powerup string (dictionary key)
        self.gameboard = [[ [Tile(),None,None] for i in range(10) ]for j in range(8)]
        #Populates game board with Pawns
        for position_x in range(10):
            self.gameboard[0][position_x].insert(1,Pawn(players[0],powerups))
            self.gameboard[1][position_x].insert(1,Pawn(players[0],powerups))
            self.gameboard[6][position_x].insert(1,Pawn(players[1],powerups))
            self.gameboard[7][position_x].insert(1,Pawn(players[1],powerups))

    def move_check(self, pos):
        '''Checks if a Pawn on a given position can move. RETURNS all the positions to where it can move'''
        # The way this works: 1.Creates a table with all possible move positions
        # 2. For each possible move position if it is accessible. If not then it removes this position from table
        y = pos[0]
        x = pos[1]
        # DOWN UP RIGHT LEFT
        move = [(y+1, x), (y-1,x), (y, x+1), (y, x-1)]
        #Move diagonal powerup
        ##if 'move_diagonal' in self.gameboard[y][x][1].attributte :
        ##    #LOWER-RIGHT LOWER-LEFT UPPER-RIGHT UPPER-LEFT
        ##    move.extend([(y+1,x+1), (y+1,x-1), (y-1,x+1), (y-1,x-1)])
        move_av = move.copy()
        for position in move_av:
        #Prepping the values
            y = position[0]
            x = position[1]

        #Tile existence/board existence
            if y > 7 or y < 0 or x > 9 or x < 0 : move.remove(position)
        #Tile height difference - Tile height > Pawn tile height AND Pawn has no jetpack
            elif self.gameboard[y][x][0].height > self.gameboard[pos[0]][pos[1]][0].height and 'jetpack' not in self.gameboard[pos[0]][pos[1]][1].attributes: move.remove(position)
        #Tile state
            elif self.gameboard[y][x][0].state == 'destroyed' : move.remove(position)
        #If pawn exists on location >> Pawn == friend or (if not friend then enemy) enemy is jump proof
            elif self.gameboard[y][x][1] :
                if self.gameboard[pos[0]][pos[1]][1].owner == self.gameboard[y][x][1].owner or 'jump_proof' in self.gameboard[y][x][1].attributes : move.remove(position)
        #Teleporters --WIP
        return tuple(move)
    def move_action(self, selected, to):
        #Check for action on selected tile
        #Do action
        #Move Pawn
        pass


class Pawn:
    def __init__(self, player,powerups):
        self.owner = player
        self.powerups = powerups
        self.collected_powerups = dict()
        self.attributes = set()

    def __repr__(self):
        return 'PAWN'

class Tile:
    def __init__(self):
        self.height = 0
        self.state = 'normal'
    def __repr__(self):
        if self.state == 'normal':return 'TILE:' + str(self.height)
        elif self.state == 'destroyed':return 'DESTROYED' #+ self.height
        elif self.state == 'teleport':return 'TELEPORT ([Insert player name])'
        else :return 'ERROR'

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/hotseat',  methods=['POST','GET'])
def hotseat_setup():
    if request.method == 'POST':
        global game
        game = Game(request.form.get('blue'), request.form.get('red'))
        return redirect('/game')
    else:
        return render_template('hotseat_setup.html')

@app.route('/game', methods=['GET','POST'])
def game():
    #Conversion to shorter variable names
    action = request.form.get('action')
    pos=[request.form.get('y'),request.form.get('x')]  #Note. position will always be (y,x)

    if action == 'select' : return render_template('game.html', game=game, movement=game.select(pos),selected=pos)
    elif action == 'move' : game.move()
    return render_template('game.html', game=game)

if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5105, debug=True)
