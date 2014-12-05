import random
import stats
import characters
import context
import namegen

class Faction( object ):
    def __init__( self, name="Da Fakshun", primary=context.HAB_EVERY, secondary=None, reaction=0 ):
        self.name = name
        self.primary = primary
        self.secondary = secondary
        self.reaction = reaction
    def alter_monster_request( self, req, force_membership=True ):
        """Add this faction's traits to the monster request."""
        if self.primary:
            if force_membership:
                req[ self.primary ] = True
            elif self.primary not in req.keys():
                req[ self.primary ] = context.MAYBE
        if self.secondary and self.secondary not in req.keys():
            req[ self.secondary ] = context.MAYBE
    def __str__( self ):
        return self.name


class AntagonistFaction( Faction ):
    # A random list of primary contexts for the antagonist faction...
    ANTAGONIST_PRIMARY = ( context.GEN_GIANT, context.GEN_GOBLIN, context.GEN_UNDEAD, context.GEN_DRAGON,
        context.MTY_MAGE )
    ANTAGONIST_SECONDARY = {
        context.GEN_GIANT: ( context.DES_EARTH, context.MTY_FIGHTER ),
        context.GEN_GOBLIN: ( context.MTY_FIGHTER, context.MTY_THIEF, context.DES_FIRE, context.DES_LUNAR ),
        context.GEN_UNDEAD: ( context.DES_LUNAR, context.DES_EARTH, context.DES_AIR ),
        context.GEN_DRAGON: ( context.DES_FIRE, context.DES_WATER, context.DES_EARTH, context.DES_AIR ),
        context.MTY_MAGE: ( context.DES_LUNAR, context.DES_FIRE, context.GEN_CHAOS ),
    }
    RANDOM_SECONDARY = (
        context.DES_EARTH, context.DES_FIRE, context.DES_AIR, context.DES_WATER,
        context.DES_SOLAR, context.DES_LUNAR, context.MTY_FIGHTER, context.MTY_MAGE
    )
    ANTAGONIST_ORG = {
        context.GEN_CHAOS: [ "Cabal","Host","Cult","Warband" ],
        context.GEN_DRAGON: [ "Dragons","Wings" ],
        context.GEN_GIANT: [ "Clan","Tribe","Marauders" ],
        context.GEN_GOBLIN: [ "Goblins","Orcs","Raiders","Ravagers","Boyz" ],
        context.GEN_UNDEAD: [ "Spirits","Dead","Ghosts" ],
        context.MTY_FIGHTER: [ "Legion","Army","Warriors" ],
        context.MTY_MAGE: [ "Adepts","Order","Coven","Wizards" ],
        context.MTY_PRIEST: [ "Brotherhood","Order","Sect" ],
        context.MTY_THIEF: [ "Brigands","Pirates","Guild" ],
    }
    ANTAGONIST_ADJECTIVE = {
        context.DES_AIR: [ "Blue","Sky" ],
        context.DES_FIRE: [ "Burning","Red" ],
        context.DES_EARTH: [ "Stone","Deep" ],
        context.DES_LUNAR: [ "Dark","Dreadful" ],
        context.DES_SOLAR: [ "Bright","Silver" ],
        context.DES_WATER: [ "Blue","Sea" ],
        context.GEN_CHAOS: [ "Chaotic", "Anarchic", "Corrupted", "Warped" ],
        context.GEN_DRAGON: [ "Golden","Ancient","Proud" ],
        context.GEN_GIANT: [ "Savage","Brutal" ],
        context.GEN_GOBLIN: [ "Bloody","Hard","Green" ],
        context.GEN_UNDEAD: [ "Vengeful","Restless" ],
        context.MTY_FIGHTER: [ "Mighty", "Iron" ],
        context.MTY_MAGE: [ "Unknown", "Mystic" ],
        context.MTY_PRIEST: [ "Pious", "Sacred" ],
        context.MTY_THIEF: [ "Secret", "Hidden" ],
    }
    ANTAGONIST_ICON = {
        context.GEN_CHAOS: [ "Wound", "Eye", "Mask", "Beast", "Horror" ],
        context.GEN_DRAGON: [ "Rage","Claw","Lair" ],
        context.GEN_GIANT: [ "Mountains","Fist" ],
        context.GEN_GOBLIN: [ "Tooth","Axe","Skull" ],
        context.GEN_UNDEAD: [ "Tomb","Crypt" ],
        context.MTY_FIGHTER: [ "Sword", "Blade" ],
        context.MTY_MAGE: [ "Staff", "Tome", "Rune" ],
        context.MTY_PRIEST: [ "Bell", "Book", "Candle", "Word" ],
        context.MTY_THIEF: [ "Dagger", "Coin" ],
    }
    ANTAGONIST_VOICE = {
        context.GEN_GOBLIN: namegen.ORC,
        context.GEN_DRAGON: namegen.DRAGON
    }
    NAME_PATTERN = (
        "{org} of the {adjective} {icon}",
        "{adjective} {org} of {propername}",
        "{adjective} {icon} {org}",
        "{adjective} {org} of the {icon}",
    )
    def __init__( self, primary=None ):
        super(AntagonistFaction, self).__init__(reaction=-50)
        self.primary = primary or random.choice( self.ANTAGONIST_PRIMARY )
        if self.primary in self.ANTAGONIST_SECONDARY.keys():
            self.secondary = random.choice( self.ANTAGONIST_SECONDARY[ self.primary ] )
        else:
            self.secondary = random.choice( self.RANDOM_SECONDARY )
        orgs = ["League",] + self.ANTAGONIST_ORG.get( self.primary, [] ) * 5 + self.ANTAGONIST_ORG.get( self.secondary, [] ) * 2
        adjectives = ["Evil",] + self.ANTAGONIST_ADJECTIVE.get( self.primary, [] ) * 2 + self.ANTAGONIST_ADJECTIVE.get( self.secondary, [] ) * 2
        icons = ["Doom",] + self.ANTAGONIST_ICON.get( self.primary, [] ) * 3 + self.ANTAGONIST_ICON.get( self.secondary, [] ) * 2
        if self.primary in self.ANTAGONIST_VOICE.keys():
            propername = self.ANTAGONIST_VOICE[ self.primary ].gen_word()
        elif self.secondary in self.ANTAGONIST_VOICE.keys():
            propername = self.ANTAGONIST_VOICE[ self.secondary ].gen_word()
        else:
            propername = namegen.random_style_name()
        pattern = random.choice( self.NAME_PATTERN )
        self.name = pattern.format( propername=propername, adjective=random.choice(adjectives), org=random.choice(orgs), icon=random.choice(icons) )

class Team( object ):
    def __init__( self, default_reaction = 0, home=None, rank=1, strength=100, habitat=None, respawn=True, fac=None, hodgepodge=False ):
        self.default_reaction = default_reaction
        self.charm_roll = None
        self.home = home
        self.rank = rank
        self.strength = strength
        self.habitat = habitat
        self.respawn = respawn
        self.fac = fac
        self.hodgepodge = hodgepodge

    def check_reaction( self, camp ):
        if self.charm_roll:
            it = self.charm_roll + self.default_reaction
        else:
            pc = camp.party_spokesperson()
            self.charm_roll = random.randint( 1, 50 ) - random.randint( 1, 50 ) + pc.get_stat_bonus( stats.CHARISMA ) * 2
            it = self.charm_roll + self.default_reaction
        if self.fac:
            it += self.fac.reaction
        return it

    def build_encounter( self, gb ):
        min_rank = min( int( self.rank * 0.7 ), self.rank - 2 )
        max_rank = self.rank + 2
        horde = list()

        if self.fac:
            self.fac.alter_monster_request( self.habitat )

        # Determine how many points of monster to generate.
        pts = max( ( random.randint(150,250) * self.strength ) // 100, 1 )

        mclass = gb.choose_monster( min_rank, max_rank, self.habitat )
        while pts > 0 and mclass:
            rel_level = max_rank + 1 - mclass.ENC_LEVEL
            m_pts = 200 / ( rel_level ** 2 // 12 + rel_level )

            # Determine what companions this monster might get.
            if self.hodgepodge:
                nextmon = gb.choose_monster( min_rank, max_rank, self.habitat )
            elif hasattr( mclass, "COMPANIONS" ):
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

if __name__=="__main__":
    names = list()
    for t in range( 100 ):
        adv = AntagonistFaction()
        names.append( adv.name )
    print ", ".join( names )


