import base
import stats

class Goblin( base.Monster ):
    name = "Goblin"    
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 7, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 8, stats.PIETY: 6, stats.CHARISMA: 3 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 0
    TEMPLATES = ()

    def init_monster( self ):
        self.levels.append( base.Humanoid( 1, self ) )


