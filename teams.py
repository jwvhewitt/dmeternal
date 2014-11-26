import random
import stats
import characters
import context

class Faction( object ):
    def __init__( self, name="Da Fakshun", tags=None, reaction=0 ):
        self.name = name
        if not tags:
            tags = list()
        self.tags = tags
        self.reaction = reaction

class Team( object ):
    def __init__( self, default_reaction = 0, home=None, rank=1, strength=100, habitat=None, respawn=True, fac=None ):
        self.default_reaction = default_reaction
        self.charm_roll = None
        self.home = home
        self.rank = rank
        self.strength = strength
        self.habitat = habitat
        self.respawn = respawn
        self.fac = fac

    def check_reaction( self, camp ):
        if self.charm_roll:
            it = self.charm_roll + self.default_reaction
        else:
            pc = camp.party_spokesperson()
            self.charm_roll = random.randint( 1, 50 ) - random.randint( 1, 50 ) + pc.get_stat_bonus( stats.CHARISMA )
            it = self.charm_roll + self.default_reaction
        if self.fac:
            it += self.fac.reaction
        return it

    def build_encounter( self, gb ):
        min_rank = min( int( self.rank * 0.7 ), self.rank - 2 )
        max_rank = self.rank + 2
        horde = list()

        # Determine how many points of monster to generate.
        pts = max( ( random.randint(150,250) * self.strength ) // 100, 1 )

        mclass = gb.choose_monster( min_rank, max_rank, self.habitat )
        while pts > 0 and mclass:
            rel_level = max_rank + 1 - mclass.ENC_LEVEL
            m_pts = 200 / ( rel_level ** 2 // 12 + rel_level )

            # Determine what companions this monster might get.
            if hasattr( mclass, "COMPANIONS" ):
                candidates = list()
                for c in mclass.COMPANIONS:
                    if c.ENC_LEVEL >= min_rank and c.ENC_LEVEL <= max_rank:
                        candidates += (c,c)
                if candidates:
                    nextmon = random.choice( candidates )
                else:
                    nextmon = None
            else:
                nextmon = None

            # Determine the number of monsters to spawn.
            if hasattr( mclass, "LONER" ) and nextmon:
                n = 1
            elif nextmon:
                # There's another monster coming up.
                max_n = pts//m_pts
                if max_n > 1:
                    n = random.randint( 1, max_n )
                else:
                    n = max_n
            else:
                # This monster type is all we have. Spend all points on it.
                n,pts = divmod( pts , m_pts )
                if random.randint( 0, m_pts ) <= pts:
                    n += 1

            pts -= n * m_pts

            if n < 1:
                n = 1
                pts = 0

            for t in range( n ):
                horde.append( mclass(self) )
            mclass = nextmon
        return horde

    def predeploy( self, gb, room ):
        self.home = room.area
        if self.strength:
            room.contents += self.build_encounter( gb )
        if self.respawn:
            gb.monster_zones.append( room.area )

    def on_guard( self ):
        """Returns True if monster isn't definitely friendly."""
        if not self.charm_roll:
            return True
        else:
            return ( self.charm_roll + self.default_reaction ) < characters.FRIENDLY_THRESHOLD


