import stats
import random
import effects
import animobs
import inspect
import teams
import context

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

class AlarmTrap( SingleTrap ):
    NAME = "Alarm Trap"
    FX = None
    MIN_RANK = 3
    DIFFICULTY = -10
    ONE_SHOT = False
    def trigger( self, explo, pos ):
        """Handle trap effect, return True if trap disabled."""
        # This trap is triggered. The party must make a DISARM_TRAPS roll or
        # suffer the consequences.
        disarm = max( explo.camp.party_stat( stats.DISARM_TRAPS, stats.DISARM_TRAPS.default_bonus ) - self.DIFFICULTY, 5 )
        if random.randint(1,100) <= disarm:
            explo.alert( "There was a {0}, but you managed to disarm it.".format( self ) )
            return True
        else:
            explo.alert( "You have set off an alarm!" )
            aoe = self.get_area( explo, pos )
            team = teams.Team(default_reaction=-999)
            req = explo.scene.get_encounter_request()
            req[context.MTY_HUMANOID] = context.MAYBE
            req[context.MTY_FIGHTER] = context.MAYBE
            mons = team.build_encounter( explo.scene, self.MIN_RANK-1, 75, req )
            for m in mons:
                if aoe:
                    p = random.choice( aoe )
                    aoe.remove( p )
                else:
                    break
                m.place( explo.scene, p )
            return self.ONE_SHOT
    def get_area( self, explo, pos ):
        aoe = list()
        for x in range( pos[0]-2, pos[0]+3 ):
            for y in range( pos[1]-2, pos[1]+3 ):
                if explo.scene.on_the_map(x,y) and not explo.scene.map[x][y].blocks_walking() and not explo.scene.get_character_at_spot((x,y)):
                    aoe.append( (x,y) )
        return aoe

class AlarmTrap2( AlarmTrap ):
    MIN_RANK = 5
    DIFFICULTY = 0

class AlarmTrap3( AlarmTrap ):
    MIN_RANK = 7
    DIFFICULTY = 10

class AlarmTrap4( AlarmTrap ):
    MIN_RANK = 9
    DIFFICULTY = 20

class AlarmTrap5( AlarmTrap ):
    MIN_RANK = 11
    DIFFICULTY = 30

class AlarmTrap6( AlarmTrap ):
    MIN_RANK = 13
    DIFFICULTY = 40

class AlarmTrap7( AlarmTrap ):
    MIN_RANK = 15
    DIFFICULTY = 50

class BladeTrap( MultiTrap ):
    NAME = "Blade Trap"
    FX = effects.SavingThrow( on_success = ( effects.NoEffect( anim=animobs.SmallBoom ), ),
        on_failure=( effects.HealthDamage((1,6,0), stat_bonus=None, element=stats.RESIST_SLASHING, anim=animobs.RedBoom ), ),
        roll_modifier = 20 )
    MIN_RANK = 6
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



