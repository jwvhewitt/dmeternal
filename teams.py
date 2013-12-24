import random
import stats

FRIENDLY_THRESHOLD = 25
ENEMY_THRESHOLD = -25
SAFELY_FRIENDLY = 100
SAFELY_ENEMY = -100

class Team( object ):
    def __init__( self, default_reaction = 0, home=None ):
        self.default_reaction = default_reaction
        self.charm_roll = None
        self.home = home

    def check_reaction( self, camp ):
        if self.charm_roll:
            return self.charm_roll + self.default_reaction
        else
            pc = camp.party_spokesperson()
            self.charm_roll = random.randint( 1, 50 ) - random.randint( 1, 50 ) + pc.get_stat_bonus( stats.CHARISMA )
            return self.charm_roll + self.default_reaction



