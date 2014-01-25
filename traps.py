import stats
import random
import effects
import animobs
import inspect

class MultiTrap( object ):
    NAME = "Boring Trap"
    FX = None
    MIN_RANK = 9999
    DIFFICULTY = 0
    ONE_SHOT = True
    def trigger( self, explo, pos ):
        """Handle trap effect, return True if trap disabled."""
        # This trap is triggered. The party must make a DISARM_TRAPS roll or
        # suffer the consequences.
        disarm = max( explo.camp.party_stat( stats.DISARM_TRAPS, stats.DISARM_TRAPS.default_bonus ) - self.DIFFICULTY, 5 )
        if random.randint(1,100) <= disarm:
            explo.alert( "There was a {0}, but you managed to disarm it.".format( self ) )
            return True
        else:
            explo.alert( "There is a {0}!!!".format( self ) )
            aoe = self.get_area( explo, pos )
            explo.invoke_effect( self.FX, None, aoe )
            return self.ONE_SHOT
    def get_area( self, explo, pos ):
        aoe = list()
        for pc in explo.camp.party:
            if pc.is_alright() and explo.scene.distance( pos, pc.pos ) <= 6:
                aoe.append( pc.pos )
        return aoe
    def __str__(self):
        return self.NAME

class SingleTrap( MultiTrap ):
    def get_area( self, explo, pos ):
        candidates = list()
        for pc in explo.camp.party:
            if pc.is_alright() and explo.scene.distance( pos, pc.pos ) <= 6:
                candidates.append( pc.pos )
        aoe = ( random.choice( candidates ), )
        return aoe

class BlockTrap( SingleTrap ):
    NAME = "Stone Block Trap"
    FX = effects.SavingThrow( on_success = ( effects.NoEffect( anim=animobs.SmallBoom ), ),
        on_failure=( effects.HealthDamage((1,6,0), stat_bonus=None, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom ), ),
        roll_modifier = 0 )
    MIN_RANK = 1
    DIFFICULTY = -20
    ONE_SHOT = True

class BladeTrap( MultiTrap ):
    NAME = "Blade Trap"
    FX = effects.SavingThrow( on_success = ( effects.NoEffect( anim=animobs.SmallBoom ), ),
        on_failure=( effects.HealthDamage((1,6,0), stat_bonus=None, element=stats.RESIST_SLASHING, anim=animobs.RedBoom ), ),
        roll_modifier = 20 )
    MIN_RANK = 3
    DIFFICULTY = -20
    ONE_SHOT = True


#  **************************************
#  ***   TRAP  LIST  AND  UTILITIES   ***
#  **************************************

TRAP_LIST = list()
for name in dir():
    o = globals()[ name ]
    if inspect.isclass( o ) and issubclass( o , MultiTrap ) and o not in (MultiTrap,SingleTrap):
        TRAP_LIST.append( o )

def choose_trap( max_rank=5 ):
    """Return a trap of at most max_rank."""
    candidates = []
    for ic in TRAP_LIST:
        if ic.MIN_RANK <= max_rank:
            candidates += [ic,] * ( ic.MIN_RANK + 2 )
    if candidates:
        return random.choice( candidates )()



