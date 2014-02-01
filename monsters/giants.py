import base
import stats
import items
import dialogue
import context

class Ogre( base.Monster ):
    name = "Ogre"    
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 16, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 6, stats.PIETY: 8, stats.CHARISMA: 5 }
    SPRITENAME = "monster_giants.png"
    FRAME = 1
    TEMPLATES = ()
    MOVE_POINTS = 10
    GP_VALUE = 35
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST,
     context.SET_EVERY, context.SET_RENFAN,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GIANT )
    ENC_LEVEL = 4

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )

