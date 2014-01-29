import base
import stats
import items
import dialogue
import context
import aibrain

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
    HABITAT = ( context.HAB_EVERY, context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 2

    COMBAT_AI = aibrain.SteadyAI()

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

class Zombie( base.Monster ):
    name = "Zombie"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 15, stats.REFLEXES: 4, \
        stats.INTELLIGENCE: 2, stats.PIETY: 8, stats.CHARISMA: 1, \
        stats.RESIST_CRUSHING: 50, stats.RESIST_FIRE: 50, stats.RESIST_PIERCING: 50 }
    SPRITENAME = "monster_undead.png"
    FRAME = 9
    TEMPLATES = (stats.UNDEAD,)
    MOVE_POINTS = 8
    VOICE = None
    GP_VALUE = 5
    HABITAT = ( context.HAB_EVERY, context.DES_LUNAR, context.GEN_UNDEAD )
    ENC_LEVEL = 3

    COMBAT_AI = aibrain.BrainDeadAI()

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )


