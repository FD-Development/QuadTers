from Board_Elements import *
import random
class Board:
    def __init__(self, players):
        ''' player table'''
        #Generates 8 x 10 array. !!Coordinates are (y,x) (rows,columns)!!
        #The information about contents of a tile in the gameboard are located in gameboard[y][x][0/1/2]
        #Where indexes: 0-Tile obj 1- Pawn obj  2- powerup string (dictionary key)
        self.gameboard = [[ [Tile(),None,None] for i in range(10) ]for j in range(8)]
        #Populates game board witsh Pawns
        for position_x in range(10):
            self.gameboard[0][position_x].insert(1,Pawn(players[0]))
            self.gameboard[1][position_x].insert(1,Pawn(players[0]))
            self.gameboard[6][position_x].insert(1,Pawn(players[1]))
            self.gameboard[7][position_x].insert(1,Pawn(players[1]))

    def move_check(self, pos):
        '''Checks if a Pawn on a given position can move. RETURNS all the positions to where it can move'''
        # The way this works: 1.Creates a table with all possible move positions
        # 2. For each possible move position if it is accessible. If not then it removes this position from table
        y = pos[0]
        x = pos[1]
        # DOWN UP RIGHT LEFT
        move = [(y+1, x), (y-1,x), (y, x+1), (y, x-1)]

        if 'move-diagonal' in self.gameboard[y][x][1].attributes :
        ##    #LOWER-RIGHT LOWER-LEFT UPPER-RIGHT UPPER-LEFT
            move.extend([(y+1,x+1), (y+1,x-1), (y-1,x+1), (y-1,x-1)])
        move_av = move.copy()
        for position in move_av:
        #Prepping the values
            y = position[0]
            x = position[1]

        #Tile existence/board existence
            if y > 7 or y < 0 or x > 9 or x < 0 : move.remove(position)
        #Tile height difference - Tile height -1 > Pawn tile height AND Pawn has no jetpack
        #-1 enables you to go up
            elif self.gameboard[y][x][0].height -1 > self.gameboard[pos[0]][pos[1]][0].height and 'climb-tile' not in self.gameboard[pos[0]][pos[1]][1].attributes: move.remove(position)
        #Tile state
            elif self.gameboard[y][x][0].state == 'destroyed' : move.remove(position)
        #If pawn exists on location >> Pawn == friend or (if not friend then enemy) enemy is jump proof
            elif self.gameboard[y][x][1] :
                if self.gameboard[pos[0]][pos[1]][1].owner == self.gameboard[y][x][1].owner or 'jump-proof' in self.gameboard[y][x][1].attributes : move.remove(position)
        #Teleporters --WIP
        return tuple(move)
    def move_action(self, sel, to):
        position_from = self.gameboard[sel[0]][sel[1]]
        position_to = self.gameboard[to[0]][to[1]]
        #If a powerup then pick it up
        if position_to[2] : self.power_pickup(sel,to)
        #Move Pawn (if an enemy pawn is on position_to it automatically deletes it)
        position_to[1] = position_from[1]
        position_from[1] = None
    def power_pickup(self, pawn, powerup):
        self.gameboard[pawn[0]][pawn[1]][1].collect_powerup(self.gameboard[powerup[0]][powerup[1]][2])
        self.gameboard[powerup[0]][powerup[1]][2]=None
    def power_place(self,powerup):
        limit = 100 #This is not an elegant solution, will fix later.
        while limit:
            loc=self.gameboard[random.randint(0,7)][random.randint(0,9)]
            limit -= 1
            # won't place powerup if the tile is destroyed there is a pawn or powerup on tile
            if loc[0].state != 'destroyed' and not loc[1] and not loc[2]:
                loc[2] = powerup
                break