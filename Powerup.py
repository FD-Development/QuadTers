class Powerup:
    def __init__(self,game):
        self.game = game

        #Dict with executable functions and types of executions chosen from [column|row|radius|self]
        self.powerup_dict = {
            'acidic-column':    (self.acidic,'column'),
            'acidic-row':       (self.acidic,'row'),
            'acidic-radius' :   (self.acidic,'radius'),
            'raise':            (self.raise_tile,'self'),
            'wall-column':      (self.wall,'column')
        }
        self.description_dict = {'raise' : ['Raise Tile','Raises the tile that the piece using the ability is currently on.'] }

        #All powerups are methods that need the specified type. Note that not all functions use the type variable
        #All methods need to return True or False
    def infiction_method(self,type):
        #Returns all affected tile locations
        #WIP - Check with grow quadradius
        if type == 'column' : return tuple( (self.game.selected[0], x ) for x in range(10) )
        elif type == 'row' : return tuple( ( y ,self.game.selected[1]) for y in range(8) )
        #WIP elif type == 'radius' : return tuple(())
    def raise_tile(self,type):
        if self.game.board.gameboard[ self.game.selected[0] ][ self.game.selected[1] ][0].height < 2 :
            self.game.board.gameboard[ self.game.selected[0] ][ self.game.selected[1] ][0].add_height()
            return True
        else : return False
    def acidic(self,type):
        pass
    def wall(self,type):
        pass