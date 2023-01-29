class Pawn:
    def __init__(self, player):
        self.owner = player
        self.powerups = None #object Powerup
        self.collected_powerups = dict()
        self.attributes = set()

    def __repr__(self):
        return 'PAWN'

    def set_powerups(self, powerup_object):
        self.powerups = powerup_object
        self.collect_powerup('raise') #Temp for testing

    def collect_powerup(self, powerup):
        if powerup in self.collected_powerups :
            self.collected_powerups.update({powerup : self.collected_powerups.get(powerup)+1})
        else : self.collected_powerups.update({powerup : 1})
    def remove_powerup(self,powerup):
        if self.collected_powerups[powerup] == 1: self.collected_powerups.pop(powerup)
        else :self.collected_powerups.update({powerup : self.collected_powerups.get(powerup)-1})


class Tile:
    def __init__(self):
        self.height = 0
        self.state = 'normal'
    def __repr__(self):
        if self.state == 'normal':return 'TILE:' + str(self.height)
        elif self.state == 'destroyed':return 'DESTROYED' #+ self.height
        elif self.state == 'teleport':return 'TELEPORT ([Insert player color])'
        else :return 'ERROR'
    def add_height(self):
        if self.height < 2 : self.height += 1
    def remove_height(self):
        if self.height > -2 : self.height -= 1