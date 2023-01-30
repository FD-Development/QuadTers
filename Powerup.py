import random
class Powerup:
    def __init__(self,game):
        self.game = game

        #Dict with executable functions and types of executions chosen from [column|row|radius|self|_attribute_]
        #The _attribute_ type should be a string with the name of attribute (same as key)
        self.powerup_dict = {
            'acidic-column':    (self.acidic,'column'),
            'acidic-row':       (self.acidic,'row'),
            'acidic-radial' :   (self.acidic,'radius'),
            'raise':            (self.raise_tile,'self'),
            'lower':            (self.lower_tile,'self'),
            'climb-tile':       (self.give_attribute,'climb-tile'),
            'jump-proof':       (self.give_attribute,'jump-proof'),
            'plifer-column':    (self.plifer,'column'),
            'plifer-row':       (self.plifer,'row'),
            'plifer-radial':    (self.plifer,'radius'),
            'wall-column':      (self.top_height,'column'),
            'wall-row':         (self.top_height, 'column'),
            'plateau':          (self.top_height, 'radius'),
            'trench-column':    (self.bottom_height, 'column'),
            'trench-row':       (self.bottom_height, 'row'),
            'moat':             (self.bottom_height, 'radius'),
            'relocate' :        (self.relocate, 'self'),
        }
        self.description_dict = {'raise' : ('Raise Tile','Raises the tile that the piece using the ability is currently on.'),
                                 'lower': ('Lower Tile', 'Lowers the tile that the piece using the ability is currently on.'),
                                 'acidic-column' : ('Acidic Column','Destroys any enemy pieces in the same column as your piece. Their tiles become completely uninhabitable.'),
                                 'acidic-row' : ('Acidic Row', 'Destroys any enemy pieces in the same row as your piece. Their tiles become completely uninhabitable.'),
                                 'acidic-radial' : ('Acidic Radial', 'Destroys any surrounding enemy pieces. Their tiles become completely uninhabitable.'),
                                 'plifer-column' : ('Plifer Column','Steal all powers from the opponents in your column.'),
                                 'plifer-row': ('Plifer Row', 'Steal all powers from the opponents in your row.'),
                                 'plifer-radial': ('Plifer Radial', 'Steal all powers from the opponents surrounding you.'),
                                 'wall-column' : ('Wall Column', 'Raises every tile to the top in the same column as your piece.'),
                                 'wall-row': ('Wall Row', 'Raises every tile to the top in the same row as your piece.	'),
                                 'plateau': ('Plateau', 'Raises every tile to the top in within a radial of your piece.	'),
                                 'trench-column': ('Trench Column', 'Lowers every tile in the same column as your piece.'),
                                 'trench-row': ('Trench Row', 'Lowers every tile in the same row as your piece.'),
                                 'moat': ('Moat', 'Lowers every tile next to your piece. Creates a moat'),
                                 'climb-tile' : ('Climb Tile', 'The piece is able to move up any tile no matter how high it is.' ),
                                 'jump-proof' : ('Jump Proof', 'This piece can no longer be defeated by being jump on by an enemy piece.'),
                                 'relocate' : ('Relocate', 'Teleports this piece to a random unoccupied location on the board.'),
                                 }

        #All powerups are methods that need the specified type. Note that not all functions use the type variable
        #All methods need to return True or False
    def give_attribute(self,attribute):
        ''' Giving attributes to pawns that don't have them '''
        if attribute in self.game.board.gameboard[self.game.selected[0]][self.game.selected[1]][1].attributes :
            return False
        else :
            self.game.board.gameboard[self.game.selected[0]][self.game.selected[1]][1].attributes.add(attribute)
            return True
    def infliction_method(self,type):
        #Returns all affected tile locations
        #WIP - Check with grow quadradius
        if type == 'row' : return tuple( (self.game.selected[0], x ) for x in range(10) )
        elif type == 'column' : return tuple( ( y ,self.game.selected[1]) for y in range(8) )
        elif type == 'radius' : #1.Creates possible affected positions 2.Deletes positions  non-existent on the map
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
    def lower_tile(self,type):
        if self.game.board.gameboard[ self.game.selected[0] ][ self.game.selected[1] ][0].height > -2 :
            self.game.board.gameboard[ self.game.selected[0] ][ self.game.selected[1] ][0].remove_height()
            return True
        else : return False
    def acidic(self,type):
        area = self.infliction_method(type)
        selected_loc = self.game.board.gameboard[self.game.selected[0]][self.game.selected[1]]
        hit = False
        for pos in area :
            target_loc = self.game.board.gameboard[pos[0]][pos[1]]
            # If there is a pawn and it is an enemy
            if target_loc[1] and target_loc[1].owner != selected_loc[1].owner :
                hit = True
                target_loc[1] = None #Eliminate pawn
                target_loc[0].state = 'destroyed' #Destroy tile

        return hit
    def plifer(self,type):
        area = self.infliction_method(type)
        selected_loc = self.game.board.gameboard[self.game.selected[0]][self.game.selected[1]]
        hit=False
        for pos in area :
            target_loc = self.game.board.gameboard[pos[0]][pos[1]]
            # If there is a pawn and it is an enemy
            if target_loc[1] and target_loc[1].owner != selected_loc[1].owner :
                hit = True
                # Steal every powerup | This can be optimised
                for steal in target_loc[1].collected_powerups.keys():
                    selected_loc[1].collect_powerup(steal) #Give powerup to selected
                    target_loc[1].remove_powerup(steal) #Remove powerup form enemy
        return hit
    def top_height(self,type):
        area = self.infliction_method(type)
        selected_loc = self.game.board.gameboard[self.game.selected[0]][self.game.selected[1]]
        affected = False
        if selected_loc[0].height <2 :
            affected=True
            selected_loc[0].height = 2
        for pos in area :
            target_loc = self.game.board.gameboard[pos[0]][pos[1]]
            if target_loc[0].height < 2:
                affected = True
                target_loc[0].height = 2

        return affected

    def bottom_height(self, type):
        area = self.infliction_method(type)
        selected_loc = self.game.board.gameboard[self.game.selected[0]][self.game.selected[1]]
        affected = False
        #If type is radial then powerup is Moat - all surrounding tiles lower, selected pawn rises
        if type == 'radius' :
            if selected_loc[0].height < 2:
                affected = True
                selected_loc[0].height = 2
        else :
            if selected_loc[0].height > -2:
                affected = True
                selected_loc[0].height = -2
        for pos in area:
            target_loc = self.game.board.gameboard[pos[0]][pos[1]]
            if target_loc[0].height > -2:
                affected = True
                target_loc[0].height = -2

        return affected

    def relocate(self,type):
        #This a special powerup it will always return FALSE beacuse it itself removes the powerup
        selected_loc = self.game.board.gameboard[self.game.selected[0]][self.game.selected[1]]
        limit = 400
        while limit :
            target_loc = self.game.board.gameboard[random.randint(0,7)][random.randint(0,9)]
            limit -= 1
            # won't relocate if the tile is destroyed there is a pawn or powerup on tile
            if target_loc[0].state != 'destroyed' and not target_loc[1] and not target_loc[2] :
                selected_loc[1].remove_powerup('relocate')
                target_loc[1] = selected_loc[1]
                selected_loc[1] = None
                return False
        return False


