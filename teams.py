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
        context.GEN_CHAOS, context.GEN_KINGDOM, context.MTY_MAGE )
    ANTAGONIST_SECONDARY = {
        context.GEN_CHAOS: ( context.DES_EARTH, context.DES_AIR, context.DES_FIRE, context.DES_WATER, context.MTY_FIGHTER, context.MTY_MAGE ),
        context.GEN_DRAGON: ( context.DES_FIRE, context.DES_WATER, context.DES_EARTH, context.DES_AIR ),
        context.GEN_GIANT: ( context.DES_EARTH, context.MTY_FIGHTER ),
        context.GEN_GOBLIN: ( context.MTY_FIGHTER, context.MTY_THIEF, context.DES_FIRE, context.DES_LUNAR ),
        context.GEN_KINGDOM: ( context.MTY_FIGHTER, context.MTY_MAGE, context.MTY_PRIEST ),
        context.GEN_UNDEAD: ( context.DES_LUNAR, context.DES_EARTH, context.DES_AIR ),
        context.MTY_MAGE: ( context.DES_LUNAR, context.DES_FIRE, context.GEN_CHAOS ),
    }
    RANDOM_SECONDARY = (
        context.DES_EARTH, context.DES_FIRE, context.DES_AIR, context.DES_WATER,
        context.DES_SOLAR, context.DES_LUNAR, context.MTY_FIGHTER, context.MTY_MAGE
    )
    ANTAGONIST_ORG = {
        context.GEN_CHAOS: [ "Cabal","Citadel","Cult","Warband" ],
        context.GEN_DRAGON: [ "Dragons","Wings" ],
        context.GEN_GIANT: [ "Clan","Tribe","Marauders","Ogres","Giants" ],
        context.GEN_GOBLIN: [ "Goblins","Orcs","Raiders","Ravagers","Boyz" ],
        context.GEN_KINGDOM: [ "Kingdom", "Lords" ],
        context.GEN_UNDEAD: [ "Spirits","Dead","Ghosts" ],
        context.MTY_FIGHTER: [ "Legion","Army","Warriors" ],
        context.MTY_MAGE: [ "Adepts","Order","Coven","Wizards" ],
        context.MTY_PRIEST: [ "Brotherhood","Order","Sect" ],
        context.MTY_THIEF: [ "Brigands","Pirates","Guild" ],
    }
    ANTAGONIST_ADJECTIVE = {
        context.DES_AIR: [ "Blue","Sky" ],
        context.DES_FIRE: [ "Fiery","Red" ],
        context.DES_EARTH: [ "Stone","Deep","Grim" ],
        context.DES_LUNAR: [ "Dark","Dreadful","Unholy" ],
        context.DES_SOLAR: [ "Bright","Silver","Holy" ],
        context.DES_WATER: [ "Blue","Sea" ],
        context.GEN_CHAOS: [ "Chaotic", "Twisted", "Corrupted", "Warped" ],
        context.GEN_DRAGON: [ "Golden","Ancient","Proud" ],
        context.GEN_GIANT: [ "Savage","Brutal" ],
        context.GEN_GOBLIN: [ "Bloody","Hard","Green" ],
        context.GEN_KINGDOM: [ "Royal", "Regal" ],
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
        context.GEN_KINGDOM: [ "Crown", "Tyrant", "King", "Queen" ],
        context.GEN_UNDEAD: [ "Tomb","Crypt" ],
        context.MTY_FIGHTER: [ "Sword", "Blade" ],
        context.MTY_MAGE: [ "Staff", "Tome", "Rune" ],
        context.MTY_PRIEST: [ "Bell", "Book", "Candle", "Word" ],
        context.MTY_THIEF: [ "Dagger", "Coin" ],
    }
    ANTAGONIST_VOICE = {
        context.GEN_GOBLIN: namegen.ORC,
        context.GEN_DRAGON: namegen.DRAGON,
        context.GEN_KINGDOM: namegen.DEFAULT,
    }
    NAME_PATTERN = (
        "{org} of the {adjective} {icon}",
        "{adjective} {org} of {propername}",
        "{adjective} {icon} {org}",
        "{adjective} {org} of the {icon}",
    )
    DUNGEON_PATTERN = (
        "{dungeon} of the {adjective} {org}",
        "{adjective} {dungeon} of {propername}",
        "{adjective} {org} {dungeon}",
        "{dungeon} of the {adjective} {icon}",
        "{adjective} {icon} {dungeon}",
    )
    def __init__( self, primary=None, dungeon_type=None ):
        # Set dungeon_type to a list of dungeon descriptors to make this faction
        #  name a passable dungeon name.
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
        if dungeon_type:
            dtype = ["Dungeon",] + list( dungeon_type ) * 5
            pattern = random.choice( self.DUNGEON_PATTERN )
        else:
            dtype = orgs
            pattern = random.choice( self.NAME_PATTERN )
        self.name = pattern.format( propername=propername, adjective=random.choice(adjectives), org=random.choice(orgs), icon=random.choice(icons), dungeon=random.choice(dtype) )

class PolisFaction( Faction ):
    """A random faction for cities and towns."""
    FRIENDLY_PRIMARY = ( context.GEN_KINGDOM, context.GEN_KINGDOM, context.GEN_NATURE,
        context.GEN_TERRAN, context.GEN_FAERIE, context.GEN_GOBLIN )
    FRIENDLY_SECONDARY = {
        context.GEN_FAERIE: ( context.MTY_MAGE, context.DES_AIR, context.MTY_THIEF,
            ),
        context.GEN_GOBLIN: ( context.MTY_FIGHTER, context.MTY_THIEF, context.DES_FIRE,
            ),
        context.GEN_KINGDOM: ( context.MTY_FIGHTER, context.MTY_MAGE, context.MTY_PRIEST,
            context.DES_SOLAR, context.DES_WATER, context.DES_LUNAR ),
        context.GEN_NATURE: ( context.DES_SOLAR, context.MTY_PRIEST, context.GEN_CHAOS ),
        context.GEN_TERRAN: ( context.DES_EARTH, context.DES_FIRE, context.MTY_FIGHTER,
            ),
    }
    RANDOM_SECONDARY = (
        context.DES_EARTH, context.DES_FIRE, context.DES_AIR, context.DES_WATER,
        context.DES_SOLAR, context.DES_LUNAR, context.MTY_FIGHTER, context.MTY_MAGE
    )
    FRIENDLY_ORG = {
        context.GEN_CHAOS: [ "Coven","Citadel", ],
        context.GEN_DRAGON: [ "Dragons","Wings" ],
        context.GEN_GIANT: [ "Clan","Tribe","Marauders","Ogres","Giants" ],
        context.GEN_GOBLIN: [ "Goblins","Orcs","Raiders","Ravagers","Boyz" ],
        context.GEN_KINGDOM: [ "Kingdom", "Lords" ],
        context.GEN_UNDEAD: [ "Spirits","Dead","Ghosts" ],
        context.MTY_FIGHTER: [ "Legion","Army","Warriors" ],
        context.MTY_MAGE: [ "Adepts","Order","Coven","Wizards" ],
        context.MTY_PRIEST: [ "Brotherhood","Order","Sect" ],
        context.MTY_THIEF: [ "Brigands","Pirates","Guild" ],
        context.DES_SOLAR: ["Knights",],
    }
    FRIENDLY_ADJECTIVE = {
        context.DES_AIR: [ "Blue","Sky" ],
        context.DES_FIRE: [ "Fiery","Red" ],
        context.DES_EARTH: [ "Stone","Deep", ],
        context.DES_LUNAR: [ "Dark","Gothic", ],
        context.DES_SOLAR: [ "Blessed","Silver","Holy" ],
        context.DES_WATER: [ "Blue","Sea" ],
        context.GEN_CHAOS: [ "Chaotic", "Free" ],
        context.GEN_DRAGON: [ "Golden","Ancient", ],
        context.GEN_GIANT: [ "Mighty","Huge" ],
        context.GEN_GOBLIN: [ "Green", ],
        context.GEN_KINGDOM: [ "Royal", "Regal" ],
        context.GEN_UNDEAD: [ "Restful","Grateful" ],
        context.MTY_FIGHTER: [ "Mighty", "Iron" ],
        context.MTY_MAGE: [ "Unknown", "Mystic" ],
        context.MTY_PRIEST: [ "Pious", "Sacred" ],
        context.MTY_THIEF: [ "Secret", "Hidden" ],
    }
    FRIENDLY_ICON = {
        context.GEN_CHAOS: [ "Chao", ],
        context.GEN_DRAGON: [ "Claw","Lair" ],
        context.GEN_GIANT: [ "Mountains", ],
        context.GEN_GOBLIN: [ "Tooth","Axe","Skull" ],
        context.GEN_KINGDOM: [ "Crown", "King", "Queen" ],
        context.GEN_UNDEAD: [ "Tomb","Crypt" ],
        context.MTY_FIGHTER: [ "Sword", "Blade" ],
        context.MTY_MAGE: [ "Staff", "Tome", "Rune" ],
        context.MTY_PRIEST: [ "Bell", "Book", "Candle", "Word" ],
        context.MTY_THIEF: [ "Dagger", "Coin" ],
    }
    FRIENDLY_VOICE = {
        context.GEN_FAERIE: namegen.ELF,
        context.GEN_GOBLIN: namegen.ORC,
        context.GEN_DRAGON: namegen.DRAGON,
        context.GEN_KINGDOM: namegen.DEFAULT,
        context.GEN_TERRAN: namegen.DWARF,
    }
    PREFIXES = {
        context.DES_AIR: [ "Blue","Sky","High" ],
        context.DES_FIRE: [ "Pyro","Red" ],
        context.DES_EARTH: [ "Rock","Deep", ],
        context.DES_ICE: ["Hyth","Cold"],
        context.DES_LUNAR: [ "Dark","Moon","Raven","Mord","Shadow" ],
        context.DES_SOLAR: [ "Sun","Good","Ever","Calm" ],
        context.DES_WATER: [ "Blue","Wave" ],
        context.GEN_CHAOS: [ "Ang", "Hodge" ],
        context.GEN_DRAGON: [ "Gold","Claw","Dragon","Wyvern" ],
        context.GEN_FAERIE: [ "Aelf","Gond","Har","Riven" ],
        context.GEN_GIANT: [ "Ur","Big","Crom" ],
        context.GEN_GOBLIN: [ "Grot","Ong","Murg","Mad","Durub","Jug" ],
        context.GEN_KINGDOM: [ "Royal", "Rich","High","Long","North","South",
            "West","East" ],
        context.GEN_NATURE: ["Green","Wyld","Oak","Yew","Skara","Arbor"],
        context.GEN_TERRAN: ["Dwarf","Gnome","Under"],
        context.GEN_UNDEAD: [ "Dead","Skull" ],
        context.MTY_FIGHTER: [ "Battle", "Sword" ],
        context.MTY_MAGE: [ "Wiz", "Spell" ],
        context.MTY_PRIEST: [ "Temple", "Altar" ],
        context.MTY_THIEF: [ "Hide", "Grab" ],
    }
    SUFFIXES = {
        context.DES_AIR: [ "cloud","wind" ],
        context.DES_FIRE: [ "hearth","forge" ],
        context.DES_EARTH: [ "stone","gem","valley","deep" ],
        context.DES_ICE: ["winter","snow"],
        context.DES_LUNAR: [ "loft","heath","mouth","wane" ],
        context.DES_SOLAR: [ "shrine","glory","shire" ],
        context.DES_WATER: [ "cove","sea","point","pier","bay","port" ],
        context.GEN_CHAOS: [ "band", "podge" ],
        context.GEN_DRAGON: [ "lair","fire","nest","weyr" ],
        context.GEN_FAERIE: ["dell","aroth","vale"],
        context.GEN_GIANT: [ "cave","lund" ],
        context.GEN_GOBLIN: [ "bitz","lam","ronk","baur","votar","kul","lug","utot","fashat" ],
        context.GEN_KINGDOM: [ "field", "wall","home","heim","land","side","ville","eros" ],
        context.GEN_NATURE: ["brae","glen","dale","hunt"],
        context.GEN_TERRAN: ["mine","gost","rond"],
        context.GEN_UNDEAD: [ "rest","grave" ],
        context.MTY_FIGHTER: [ "hall","hold","castle","war","hawk","shield","guard" ],
        context.MTY_MAGE: [ "tome", "warts","school","topia" ],
        context.MTY_PRIEST: [ "abbey","gard" ],
        context.MTY_THIEF: [ "hole", "hoard", "vault" ],
    }

    NAME_PATTERN = (
        "{org} of the {adjective} {icon}",
        "{adjective} {org} of {propername}",
        "{adjective} {icon} {org}",
        "{adjective} {org} of the {icon}",
    )
    DUNGEON_PATTERN = (
        "{dungeon} of {psname}",
    )
    def __init__( self, primary=None, dungeon_type=None ):
        # Set dungeon_type to a list of dungeon descriptors to make this faction
        #  name a passable dungeon name.
        super(PolisFaction, self).__init__(reaction=0)
        self.primary = primary or random.choice( self.FRIENDLY_PRIMARY )
        if self.primary in self.FRIENDLY_SECONDARY.keys():
            self.secondary = random.choice( self.FRIENDLY_SECONDARY[ self.primary ] )
        else:
            self.secondary = random.choice( self.RANDOM_SECONDARY )
        orgs = ["Land",] + self.FRIENDLY_ORG.get( self.primary, [] ) * 5 + self.FRIENDLY_ORG.get( self.secondary, [] ) * 2
        adjectives = ["Nice",] + self.FRIENDLY_ADJECTIVE.get( self.primary, [] ) * 2 + self.FRIENDLY_ADJECTIVE.get( self.secondary, [] ) * 2
        icons = ["Peace",] + self.FRIENDLY_ICON.get( self.primary, [] ) * 3 + self.FRIENDLY_ICON.get( self.secondary, [] ) * 2

        if self.primary in self.FRIENDLY_VOICE.keys():
            propername = self.FRIENDLY_VOICE[ self.primary ].gen_word()
        elif self.secondary in self.FRIENDLY_VOICE.keys():
            propername = self.FRIENDLY_VOICE[ self.secondary ].gen_word()
        else:
            propername = namegen.random_style_name()

        # Make a portmanteau name based on the two attributes.
        atts = [self.primary,self.secondary]
        random.shuffle( atts )
        if atts[0] in self.PREFIXES and atts[1] in self.SUFFIXES:
            psname = random.choice(self.PREFIXES[atts[0]])+random.choice(self.SUFFIXES[atts[1]])
        else:
            psname = propername

        if dungeon_type:
            dtype = ["City",] + list( dungeon_type ) * 5
            pattern = random.choice( self.DUNGEON_PATTERN )
        else:
            dtype = orgs
            pattern = random.choice( self.NAME_PATTERN )
        self.name = pattern.format( propername=propername, adjective=random.choice(adjectives), org=random.choice(orgs), icon=random.choice(icons), dungeon=random.choice(dtype), psname=psname )


class Team( object ):
    def __init__( self, default_reaction = 0, home=None, rank=1, strength=100,
     habitat=None, respawn=True, fac=None, hodgepodge=False, boss=None ):
        self.default_reaction = default_reaction
        self.charm_roll = None
        self.home = home
        self.rank = rank
        self.strength = strength
        self.habitat = habitat
        self.respawn = respawn
        self.fac = fac
        self.hodgepodge = hodgepodge
        self.boss = boss

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

    def encounter_points( self, max_rank, mon_rank, xp_value ):
        """Return the encounter points per monster for this mclass."""
        rel_level = max( max_rank + 1 - mon_rank , 1 )
        m_pts = 200 / ( rel_level ** 2 / 12 + rel_level )

        # Scale the points based on the xp value of the monster, assuming
        # a normal rate of 100xp per rank.
        if mon_rank == 0:
            print "ERROR: {} is the boss {}".format( self.boss, self.boss.ENC_LEVEL )
            if hasattr( self.boss, "monster_name" ):
                print self.boss.monster_name
            else:
                print "Apparently an NPC boss..."
            print self.boss.desc()
        m_pts = ( m_pts * xp_value ) // ( min( max_rank, mon_rank) * 100 )
        return m_pts

    def build_encounter( self, gb ):
        min_rank = min( int( self.rank * 0.7 ), self.rank - 2 )
        max_rank = self.rank + 2
        horde = list()

        myhab = self.habitat.copy()
        if self.fac:
            self.fac.alter_monster_request( myhab )

        # Determine how many points of monster to generate.
        pts = max( ( random.randint(175,225) * self.strength ) // 100, 1 )

        # If we've been given a boss, remove points for that first.
        if self.boss:
            pts -= self.encounter_points( max_rank, self.boss.ENC_LEVEL, self.boss.xp_value() )

        # We really don't want generation to fail. If no faction members can
        # be found, attempt to load without faction... or just anything.
        mclass = gb.choose_monster( min_rank, max_rank, myhab )
        if self.fac and not mclass:
            mclass = gb.choose_monster( min_rank, max_rank, self.habitat )
        if not mclass:
            mclass = gb.choose_monster( min_rank, max_rank, {context.SET_EVERY: True} )

        while pts > 0 and mclass:
            m_pts = self.encounter_points( max_rank, mclass.ENC_LEVEL, mclass().xp_value() )

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
                max_n,left_n = divmod( pts, m_pts )
                if max_n > 1:
                    n = random.randint( 1, max_n )
                else:
                    n = max_n
                # If the next monster in a hodgepodge is too big,
                # just end with this monster.
                if self.hodgepodge and left_n > 0 and self.encounter_points( max_rank, nextmon.ENC_LEVEL, nextmon().xp_value() ) > ( left_n + 25 ):
                    n = max_n + 1
                    nextmon = 0
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

    def members_in_play( self, gb ):
        """Return list of team members on this map."""
        my_members = list()
        for m in gb.contents:
            if isinstance( m , characters.Character ) and hasattr( m, "team" ) and m.team is self:
                my_members.append( m )
        return my_members

if __name__=="__main__":
    names = list()
    for t in range( 100 ):
        adv = AntagonistFaction()
        names.append( adv.name )
    print ", ".join( names )


