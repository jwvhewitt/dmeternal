import stats
import random
import effects
import animobs

class Trap( object ):
    NAME = "Boring Trap"
    FX = None
    MIN_RANK = 9999
    DIFFICULTY = 0
    ONE_SHOT = True
    def trigger( self, explo ):
        """Handle trap effect, return True if trap disabled."""
        # This trap is triggered. The party must make a DISARM_TRAPS roll or
        # suffer the consequences.
        disarm = max( explo.camp.party_stat( stats.DISARM_TRAPS, stats.DISARM_TRAPS.default_bonus ) - self.DIFFICULTY, 5 )
        if random.randint(1,100) <= disarm:
            explo.alert( "There was a {0}, but you managed to disarm it.".format( self ) )
            return True
        else:
            explo.alert( "There is a {0}!!!".format( self ) )
            aoe = self.get_area( explo )
            explo.invoke_effect( self.FX, None, aoe )
            return self.ONE_SHOT
    def get_area( self, explo ):
        aoe = list()
        for pc in explo.camp.party:
            if pc.is_alright():
                aoe.append( pc.pos )
        return aoe
    def __str__(self):
        return self.NAME

class BladeTrap( Trap ):
    NAME = "Blade Trap"
    FX = effects.HealthDamage((1,6,0), stat_bonus=None, element=stats.RESIST_SLASHING, anim=animobs.RedBoom )
    MIN_RANK = 1
    DIFFICULTY = -20
    ONE_SHOT = True


