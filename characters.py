
import stats

class Level( object ):
    # Or, as we would say in a PnP RPG, a "class".
    # Keeping as much info as possible in the class attributes, so after pickling
    # a character the values can be changed here and the PC will automatically
    # use the new values.
    def __init__( self, rank ):
        self.rank = rank
    def get_stat_bonus( self, stat ):
        """Typical stat bonus is base bonus x rank"""
        return self.statline.get( stat , 0 ) * self.rank

class Warrior( Level ):
    name = 'Warrior'
    desc = 'Highly trained fighters who can dish out- and take- a whole lot of physical damage.'
    requirements = { stats.STRENGTH: 11 }
    statline = { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 2, stats.MAGIC_DEFENSE: 3, \
        stats.AWARENESS: 3 }

class Thief( Level ):
    name = 'Thief'
    desc = 'Highly skilled at stealth and disarming traps.'
    requirements = { stats.REFLEXES: 11 }
    statline = { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 4, \
        stats.DISARM_TRAPS: 6, stats.STEALTH: 5, stats.AWARENESS: 4 }



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

