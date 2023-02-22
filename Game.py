from Board import Board
from Powerup import Powerup
from Player import Player
import random
class Game:
    def __init__(self, blue, red):
        #Setting players
        self.players = list()
        self.players.append(Player(red))
        self.players.append(Player(blue))
        #Setting board + pawns
        self.board = Board(self.players)
        self.selected = None
        #Setting powerups
        self.powerups = Powerup(self)
        #Linking powerups with pawns
        for position_x in range(10):
            self.board.gameboard[0][position_x][1].set_powerups(self.powerups)
            self.board.gameboard[1][position_x][1].set_powerups(self.powerups)
            self.board.gameboard[6][position_x][1].set_powerups(self.powerups)
            self.board.gameboard[7][position_x][1].set_powerups(self.powerups)
        # Randomizing who is starting
        if random.randint(0,1) : random.shuffle(self.players)
        self.turn = self.next_turn()
        self.current = next(self.turn)

    def select(self, pos):
        self.selected=(pos[0],pos[1])
        return self.board.move_check(pos)
    def deselect(self):
        self.selected=None
    def move(self, pos):
        self.board.move_action(self.selected, pos)
        self.deselect()
        self.current = next(self.turn)
    def activate_power(self, power):
        #1. Activates power - function(type) 2.If activation is successful removes power from inventory
        if self.powerups.powerup_dict[power][0](self.powerups.powerup_dict[power][1]) :
            self.board.gameboard[self.selected[0]][self.selected[1]][1].remove_powerup(power)
    def skip(self):
        self.current = next(self.turn)
    def next_turn(self):
        #Switches player's turn & generates powerups
        powergen=0 #Note that due to self.current in init, this will always be powergen+1 at start
        turn = lambda : random.randint(3, 6)
        generation_turn = turn()
        while True :
            #if this is the last player in the player-list it will start over
            for player in self.players :
                powergen += 1
                if powergen == generation_turn:
                    powergen = 0
                    generation_turn = turn()
                    self.generate()
                yield player
    def generate(self):
        #Generates powerups on the board
        #Generate random amount of powerups (1-4)
        for x in range(1,random.randint(1,4)) :
          self.board.power_place( random.choice(list(self.powerups.powerup_dict.keys())) )

    def victory_check(self):
        #Checks for existent pawns of each player. If there's one left = current (victor). If no one then it's a draw.
        alive_players = []
        for player in self.players:
            if self.victory_condition(player) : alive_players.append(player)

        if   len(alive_players) > 1 :
            return False
        elif len(alive_players) == 1 :
            self.current = alive_players[0]
            return True
        else :
            self.current = None
            return True

    def victory_condition(self, player):
        for y in range(8):
            for x in range(10):
                #If at least one pawn of this player is found
                if self.board.gameboard[y][x][1] and self.board.gameboard[y][x][1].owner == player:
                    return True
        return False