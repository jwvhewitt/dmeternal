


class Level( object ):
    # Or, as we would say in a PnP RPG, a "class".
    # Keeping as much info as possible in the class attributes, so after pickling
    # a character the values can be changed here and the PC will automatically
    # use the new values.
    def __init__( self, rank ):
        self.rank = rank
    def get_stat_bonus( self, stat ):
        """Typical stat bonus is base bonus x rank"""
        if stat in self.statline:
            return self.statline[ stat ] * self.rank
        else:
            return 0

class Character(object):
    def __init__( self ):
        statline = dict()
        levels = []

    def get_stat( self , stat ):
        # Start with the basic stat value. This will probably be 0.
        it = self.statline.get( stat , 0 )
        # Add bonuses from any earned classes...
        for l in self.levels:
            it += l.get_stat_bonus( stat )
        # Add bonuses from any equipment...

        return it

