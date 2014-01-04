import base
import stats
import items
import dialogue

class Goblin( base.Monster ):
    name = "Goblin"    
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 7, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 8, stats.PIETY: 6, stats.CHARISMA: 3 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.ORCISH
    GP_VALUE = 5

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 1, self ) )


