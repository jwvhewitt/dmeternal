#
# They say there should only be one obvious way to do something in Python...
# Well this is obvious to me and #@#! anyone who says otherwise.
#
# Originally used the range function to generate constants for all the stats
# that need keeping track of. Realized that this method is terrible, and instead
# decided to implement a singleton class to serve as stat tokens. Oh, don't give
# me that look... singletons are the proper solution to certain problems and
# as far as I can tell this is one of them. If you have a better idea, let me
# know.
#

class PhysicalThing( object ):
    """A thing that can be placed on the map."""
    def place( self, scene, pos=None ):
        if hasattr( self, "container" ) and self.container:
            self.container.remove( self )
        scene.contents.append( self )
        self.pos = pos

class SingStat( object ):
    # A singleton stat class; use these objects as tokens for whatever.
    # Also includes misc information related to the stat in question.
    def __init__( self, ident, name, default_bonus = None, cost_mod = 25, element_name="", element_cost_mod=1 ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.name = name
        self.default_bonus = default_bonus
        self.cost_mod = cost_mod
        self.element_name = element_name
        self.element_cost_mod = element_cost_mod
    def __str__( self ):
        return self.name
    def __reduce__( self ):
        return self.ident

# Do not modify these singletons! That is not how they are used.
#                       \  / /
#                         (OvO)
#                         -| '|
#                          U-U*

STRENGTH = SingStat( "STRENGTH", "Strength", cost_mod = 1500 )
TOUGHNESS = SingStat( "TOUGHNESS", "Toughness", cost_mod = 1500 )
REFLEXES = SingStat( "REFLEXES", "Reflexes", cost_mod = 1500 )
INTELLIGENCE = SingStat( "INTELLIGENCE", "Intelligence", cost_mod = 1500 )
PIETY = SingStat( "PIETY", "Piety", cost_mod = 1500 )
CHARISMA = SingStat( "CHARISMA", "Charisma", cost_mod = 1500 )

PHYSICAL_ATTACK = SingStat( "PHYSICAL_ATTACK", "Attack", cost_mod = 25 )
PHYSICAL_DEFENSE = SingStat( "PHYSICAL_DEFENSE", "Defense", default_bonus = REFLEXES, cost_mod = 10 )
MAGIC_ATTACK = SingStat( "MAGIC_ATTACK", "Magic", default_bonus = INTELLIGENCE, cost_mod = 25 )
MAGIC_DEFENSE = SingStat( "MAGIC_DEFENSE", "Aura", default_bonus = PIETY, cost_mod = 15 )
DISARM_TRAPS = SingStat( "DISARM_TRAPS", "Disarm Traps", default_bonus = INTELLIGENCE, cost_mod = 20 )

STEALTH = SingStat( "STEALTH", "Stealth", default_bonus = REFLEXES, cost_mod = 25 )
RESIST_SLASHING = SingStat( "RESIST_SLASHING", "Slash Resist", cost_mod = 10, element_name="Slashing" )
RESIST_PIERCING = SingStat( "RESIST_PIERCING", "Piercing Resist", cost_mod = 10, element_name="Piercing" )
RESIST_CRUSHING = SingStat( "RESIST_CRUSHING", "Crush Resist", cost_mod = 10, element_name="Crushing" )
RESIST_FIRE = SingStat( "RESIST_FIRE", "Fire Resist", cost_mod = 5, element_name="Fire" )

RESIST_COLD = SingStat( "RESIST_COLD", "Cold Resist", cost_mod = 5, element_name="Frost" )
RESIST_LIGHTNING = SingStat( "RESIST_LIGHTNING", "Lightning Resist", cost_mod = 5, element_name="Lightning" )
RESIST_ACID = SingStat( "RESIST_ACID", "Acid Resist", cost_mod = 5, element_name="Acid" )
RESIST_LUNAR = SingStat( "RESIST_LUNAR", "Dark Resist", cost_mod = 15, element_name="Dark", element_cost_mod=3 )
RESIST_SOLAR = SingStat( "RESIST_SOLAR", "Holy Resist", cost_mod = 15, element_name="Holy", element_cost_mod=3 )

RESIST_WIND = SingStat( "RESIST_WIND", "Wind Resist", cost_mod = 10, element_name="Wind", element_cost_mod=2 )
RESIST_WATER = SingStat( "RESIST_WATER", "Water Resist", cost_mod = 10, element_name="Water", element_cost_mod=2 )
RESIST_ATOMIC = SingStat( "RESIST_ATOMIC", "Atomic Resist", cost_mod = 20, element_name="Atomic", element_cost_mod=5 )
RESIST_POISON = SingStat( "RESIST_POISON", "Poison Resist", cost_mod = 10, element_name="Poison", element_cost_mod=2 )
HOLY_SIGN = SingStat( "HOLY_SIGN", "Holy Sign", default_bonus = CHARISMA, cost_mod = 25 )

KUNG_FU = SingStat( "KUNG_FU", "Kung Fu", cost_mod = 55 )
NATURAL_DEFENSE = SingStat( "NATURAL_DEFENSE", "Natural Defense", default_bonus = REFLEXES, cost_mod = 35 )
CRITICAL_HIT = SingStat( "CRITICAL_HIT", "Critical Hit", cost_mod = 85 )
AWARENESS = SingStat( "AWARENESS", "Awareness", default_bonus = INTELLIGENCE, cost_mod = 15 )

PRIMARY_STATS = ( STRENGTH, TOUGHNESS, REFLEXES, INTELLIGENCE, PIETY, CHARISMA )


# Gender tags
FEMALE, MALE, NEUTER = range( 3 )
GENDER = ( "Female", "Male", "Neuter" )
SUBJECT_PRONOUN = ( "she", "he", "ze" )
OBJECT_PRONOUN = ( "her", "him", "ze" )
POSSESSIVE_PRONOUN = ( "her", "his", "ze" )



class StatMod( dict ):
    """A dictionary of stat bonuses, with cost() method for items, etc"""
    def cost( self ):
        """Return the gp cost of these stat bonuses."""
        it = 0
        for stat,val in self.iteritems():
            if val > 0:
                it += val * ( val + 1 ) * stat.cost_mod // 10
            elif self[ stat ] < 0:
                it -= val * ( val + 1 ) * stat.cost_mod // 75
        return it


# MONSTER TEMPLATES

class SingTemp( object ):
    # A singleton template class; use these objects as tokens for whatever.
    # Also includes misc information related to the template in question.
    def __init__( self, ident, bonuses = None ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.bonuses = bonuses
    def __str__( self ):
        return self.name
    def __reduce__( self ):
        return self.ident

UNDEAD = SingTemp( "UNDEAD", { PHYSICAL_ATTACK: 5, MAGIC_ATTACK: 5, \
    RESIST_COLD: 50, RESIST_LUNAR: 50, RESIST_SOLAR: -100, \
    RESIST_POISON: 155 } )
BONE = SingTemp( "BONE", { RESIST_SLASHING: 50, RESIST_PIERCING: 50 } )
INCORPOREAL = SingTemp( "INCORPOREAL", { RESIST_SLASHING: 100, RESIST_PIERCING: 100,
    RESIST_CRUSHING: 100, STEALTH: 20, RESIST_ATOMIC: 50  } )

CONSTRUCT = SingTemp( "CONSTRUCT", { RESIST_CRUSHING: 25, RESIST_PIERCING: 25, \
    RESIST_SLASHING: 25, RESIST_WATER: -100, RESIST_ATOMIC: -300, \
    RESIST_POISON: 155, AWARENESS: -10 } )
PLANT = SingTemp( "PLANT", { RESIST_FIRE: -100, RESIST_SOLAR: 100, RESIST_LUNAR: -100, \
    RESIST_WATER: 250, AWARENESS: -10, RESIST_CRUSHING: 50, RESIST_PIERCING: 50 })
ELEMENTAL = SingTemp( "ELEMENTAL", { NATURAL_DEFENSE: 5, MAGIC_DEFENSE: -5, \
    RESIST_CRUSHING: 25, RESIST_PIERCING: 25, RESIST_SLASHING: 25, \
    RESIST_ATOMIC: -100, RESIST_POISON: 155 })
DEMON = SingTemp( "DEMON", { MAGIC_DEFENSE: 5, RESIST_FIRE: 75, RESIST_LUNAR: 75, \
    RESIST_SOLAR: -100, RESIST_POISON: 100 })
BUG = SingTemp( "BUG", { NATURAL_DEFENSE: 10, MAGIC_DEFENSE: -10, \
    RESIST_SLASHING: 50, RESIST_CRUSHING: -50, RESIST_ACID: -100,
    RESIST_POISON: -100 })
REPTILE = SingTemp( "REPTILE", { RESIST_FIRE: 50, RESIST_COLD: -50 })
DRAGON = SingTemp( "DRAGON", { NATURAL_DEFENSE: 10, MAGIC_DEFENSE: 10, \
    RESIST_FIRE: 50, RESIST_COLD: 50, RESIST_ACID: 50, \
    RESIST_LIGHTNING: 50, RESIST_POISON: 50, RESIST_SLASHING: 33, \
    RESIST_CRUSHING: 33, AWARENESS: 15 })
FIRE = SingTemp( "FIRE", { PHYSICAL_ATTACK: 5, NATURAL_DEFENSE: -5, \
    RESIST_FIRE: 100, RESIST_COLD: -100, \
    RESIST_WATER: -100, RESIST_ATOMIC: 50 })
WATER = SingTemp( "WATER", { MAGIC_ATTACK: -5, MAGIC_DEFENSE: 5, \
    RESIST_FIRE: 50, RESIST_COLD: 50, \
    RESIST_LIGHTNING: -100, RESIST_ACID: -50, RESIST_WATER: 255 })
EARTH = SingTemp( "EARTH", { PHYSICAL_ATTACK: -5, NATURAL_DEFENSE: 5, \
    RESIST_LIGHTNING: 100, \
    RESIST_ACID: 50, RESIST_WIND: -100, RESIST_WATER: -100 })
AIR = SingTemp( "AIR", { MAGIC_ATTACK: 5, MAGIC_DEFENSE: -5, \
    RESIST_FIRE: -100, RESIST_ACID: 50, \
    RESIST_WIND: 50 })
ICE = SingTemp( "ICE", { RESIST_PIERCING: -50, RESIST_SLASHING: 50, \
    RESIST_FIRE: -100, RESIST_COLD: 100, RESIST_WIND: 50, RESIST_WATER: 50 })



if __name__ == '__main__':

    import pickle

    armor = StatMod()
    armor[ MAGIC_ATTACK ] = -40
    armor[ STEALTH ] = -40
    armor[ PHYSICAL_DEFENSE ] = 40

    print armor.cost()

    f = open( "test.sav", "wb" )
    pickle.dump( armor , f, -1 )
    f.close()

    f2 = open( "test.sav", "rb" )
    a2 = pickle.load( f2 )
    f2.close()

    print a2.cost()
    print a2[ PHYSICAL_DEFENSE ]



