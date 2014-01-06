import base
import stats
import items
import dialogue

class Skeleton( base.Monster ):
    name = "Skeleton"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_undead.png"
    FRAME = 0
    TEMPLATES = (stats.UNDEAD,stats.BONE)
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 5

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

