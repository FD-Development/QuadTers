class Powerup:
    def __init__(self,game):
        self.game = game

        #Dict with executable functions and types of executions chosen from [column|row|radius|self]
        self.powerup_dict = {
            'acidic-column':    (self.acidic,'column'),
            'acidic-row':       (self.acidic,'row'),
            'acidic-radial' :   (self.acidic,'radius'),
            'raise':            (self.raise_tile,'self'),
            #'wall-column':      (self.wall,'column')
        }
        self.description_dict = {'raise' : ('Raise Tile','Raises the tile that the piece using the ability is currently on.'),
                                 'acidic-column' : ('Acidic Column','Destroys any enemy pieces in the same column as your piece. Their tiles become completely uninhabitable.'),
                                 'acidic-row' : ('Acidic Row', 'Destroys any enemy pieces in the same row as your piece. Their tiles become completely uninhabitable.'),
                                 'acidic-radial' : ('Acidic Radial', 'Destroys any surrounding enemy pieces. Their tiles become completely uninhabitable.')
                                 }

        #All powerups are methods that need the specified type. Note that not all functions use the type variable
        #All methods need to return True or False
    def infliction_method(self,type):
        #Returns all affected tile locations
        #WIP - Check with grow quadradius
        if type == 'row' : return tuple( (self.game.selected[0], x ) for x in range(10) )
        elif type == 'column' : return tuple( ( y ,self.game.selected[1]) for y in range(8) )
        elif type == 'radius' :
            radius = list()
            # [x-1+0][x-1+1][x-1+1] = [x-1][x][x+1]
            radius.extend( list((self.game.selected[0]+1,self.game.selected[1]-1+x) for x in range(3)) )
            radius.append((self.game.selected[0],self.game.selected[1]-1))
            radius.append((self.game.selected[0], self.game.selected[1]+1))
            radius.extend( list((self.game.selected[0]-1,self.game.selected[1]-1+x) for x in range(3)) )
            #We cannot give positions that do not exist, this cleanses non-existent pos
            for pos in radius:
                y = pos[0]
                x = pos[1]
                if y > 7 or y < 0 or x > 9 or x < 0: radius.remove(pos)
            return tuple(radius)
    def raise_tile(self,type):
        if self.game.board.gameboard[ self.game.selected[0] ][ self.game.selected[1] ][0].height < 2 :
            self.game.board.gameboard[ self.game.selected[0] ][ self.game.selected[1] ][0].add_height()
            return True
        else : return False
    def acidic(self,type):
        area = self.infliction_method(type)
        hit = False
        for pos in area :
            y=pos[0]
            x=pos[1]
            # If there is a pawn and it is an enemy
            if self.game.board.gameboard[y][x][1] and self.game.board.gameboard[y][x][1].owner != self.game.board.gameboard[self.game.selected[0]][self.game.selected[1]][1].owner :
                hit = True
                self.game.board.gameboard[y][x][1] = None #Eliminate pawn
                self.game.board.gameboard[y][x][0].state = 'destroyed' #Destroy tile

        return hit
    def wall(self,type):
        pass