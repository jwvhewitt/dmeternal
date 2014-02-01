import random
import stats
import characters
import context

class Team( object ):
    def __init__( self, default_reaction = 0, home=None, rank=1, strength=100, habitat=None ):
        self.default_reaction = default_reaction
        self.charm_roll = None
        self.home = home
        self.rank = rank
        self.strength = strength
        self.habitat = habitat

    def check_reaction( self, camp ):
        if self.charm_roll:
            return self.charm_roll + self.default_reaction
        else:
            pc = camp.party_spokesperson()
            self.charm_roll = random.randint( 1, 50 ) - random.randint( 1, 50 ) + pc.get_stat_bonus( stats.CHARISMA )
            return self.charm_roll + self.default_reaction

    def build_encounter( self, gb, rank, strength, habitat=None ):
        min_rank = min( int( rank * 0.7 ), rank - 2 )
        max_rank = rank + 2
        horde = list()

        # Determine how many points of monster to generate.
        pts = max( ( random.randint(150,250) * strength ) // 100, 1 )

        while pts > 0:
            mclass = gb.choose_monster( min_rank, max_rank, habitat )
            rel_level = max_rank + 1 - mclass.ENC_LEVEL
            m_pts = 200 / ( rel_level ** 2 // 12 + rel_level )

            n,pts = divmod( pts , m_pts )
            if n < 1:
                n = 1
                pts = 0

            for t in range( n ):
                horde.append( mclass(self) )
        return horde

    def predeploy( self, gb, room ):
        self.home = room.area
        room.contents += self.build_encounter( gb, self.rank, self.strength, self.habitat )

    def on_guard( self ):
        """Returns True if monster isn't definitely friendly."""
        if not self.charm_roll:
            return True
        else:
            return ( self.charm_roll + self.default_reaction ) < characters.FRIENDLY_THRESHOLD


