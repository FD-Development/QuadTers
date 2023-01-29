class Powerup:
    def __init__(self,game):
        self.game = game

        self.powerup_dictionary = {
            'acidic-column': self.acidic('column'),
            'acidic-row': self. acidic('row'),
            'acidic-radius': self.acidic('radius'),
            'raise': self.raise_tile(),
            'wall-column': self.wall('column'),
        }
        self.description_dictionary = {'raise' : 'Raises the tile level by +1.' }

        #type chosen from [column|row|radius]

    def raise_tile(self):
        self.game.board.gameboard[ self.game.selected[0] ][ self.game.selected[1] ][0].add_height()
    def acidic(self,type):
        pass
    def wall(self,type):
        pass