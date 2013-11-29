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

class SingStat( object ):
    # A singleton stat class; use these objects as tokens for whatever.
    # Also includes misc information related to the stat in question.
    def __init__( self, ident, name, default_bonus = None, cost_mod = 25, element_name="" ):
        # ident should be the module-level name of this stat.
        self.ident = ident
        self.name = name
        self.default_bonus = default_bonus
        self.cost_mod = cost_mod
        self.element_name = element_name
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
RESIST_SLASHING = SingStat( "RESIST_SLASHING", "Slash Resistance", cost_mod = 10, element_name="Slashing" )
RESIST_PIERCING = SingStat( "RESIST_PIERCING", "Piercing Resistance", cost_mod = 10, element_name="Piercing" )
RESIST_CRUSHING = SingStat( "RESIST_CRUSHING", "Crush Resistance", cost_mod = 10, element_name="Crushing" )
RESIST_FIRE = SingStat( "RESIST_FIRE", "Fire Resistance", cost_mod = 5, element_name="Fire" )

RESIST_COLD = SingStat( "RESIST_COLD", "Cold Resistance", cost_mod = 5, element_name="Frost" )
RESIST_LIGHTNING = SingStat( "RESIST_LIGHTNING", "Lightning Resistance", cost_mod = 5, element_name="Lightning" )
RESIST_ACID = SingStat( "RESIST_ACID", "Acid Resistance", cost_mod = 5, element_name="Acid" )
RESIST_LUNAR = SingStat( "RESIST_LUNAR", "Dark Resistance", cost_mod = 20, element_name="Dark" )
RESIST_SOLAR = SingStat( "RESIST_SOLAR", "Holy Resistance", cost_mod = 20, element_name="Holy" )

RESIST_WIND = SingStat( "RESIST_WIND", "Wind Resistance", cost_mod = 15, element_name="Wind" )
RESIST_WATER = SingStat( "RESIST_WATER", "Water Resistance", cost_mod = 15, element_name="Water" )
RESIST_ATOMIC = SingStat( "RESIST_ATOMIC", "Atomic Resistance", cost_mod = 30, element_name="Atomic" )
RESIST_POISON = SingStat( "RESIST_POISON", "Poison Resistance", cost_mod = 15, element_name="Poison" )
HOLY_SIGN = SingStat( "HOLY_SIGN", "Holy Sign", default_bonus = CHARISMA, cost_mod = 25 )

KUNG_FU = SingStat( "KUNG_FU", "Kung Fu", cost_mod = 25 )
NATURAL_DEFENSE = SingStat( "NATURAL_DEFENSE", "Natural Defense", default_bonus = REFLEXES, cost_mod = 25 )
CRITICAL_HIT = SingStat( "CRITICAL_HIT", "Critical Hit", cost_mod = 35 )
AWARENESS = SingStat( "AWARENESS", "Awareness", default_bonus = INTELLIGENCE, cost_mod = 15 )

PRIMARY_STATS = ( STRENGTH, TOUGHNESS, REFLEXES, INTELLIGENCE, PIETY, CHARISMA )


# Gender tags
FEMALE, MALE, NEUTER = range( 3 )
GENDER = ( "Female", "Male", "Neuter" )



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



