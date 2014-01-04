import base
import stats
import items
import dialogue

class Ogre( base.Monster ):
    name = "Ogre"    
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 16, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 6, stats.PIETY: 8, stats.CHARISMA: 5 }
    SPRITENAME = "monster_giants.png"
    FRAME = 1
    TEMPLATES = ()
    MOVE_POINTS = 10
    GP_VALUE = 60

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )

