#
# They say there should only be one obvious way to do something in Python...
# Well this is obvious to me and #@#! anyone who says otherwise.
#
# Using the range function to generate constants for all the stats that need
# keeping track of.
#

NUM_STATS = 30

STRENGTH, TOUGHNESS, REFLEXES, INTELLIGENCE, PIETY, CHARISMA, \
    PHYSICAL_ATTACK, PHYSICAL_DEFENSE, MAGIC_ATTACK, MAGIC_DEFENSE, DISARM_TRAPS, \
    STEALTH, RESIST_SLASHING, RESIST_PIERCING, RESIST_CRUSHING, RESIST_FIRE, \
    RESIST_COLD, RESIST_LIGHTNING, RESIST_ACID, RESIST_LUNAR, RESIST_SOLAR, \
    RESIST_WIND, RESIST_WATER, RESIST_ATOMIC, RESIST_POISON, HOLY_SIGN, \
    KUNG_FU, NATURAL_DEFENSE, CRITICAL_HIT, AWARENESS = range(NUM_STATS)

NAMES = ( "Strength", "Toughness", "Reflexes", "Intelligence", "Piety", "Charisma", \
    "Attack", "Defense", "Magic", "Aura", "Disarm Traps", \
    "Stealth", "Slash Resistance", "Piercing Resistance", "Crush Resistance", "Fire Resistance", \
    "Cold Resistance", "Lightning Resistance", "Acid Resistance", "Dark Resistance", "Holy Resistance", \
    "Wind Resistance", "Water Resistance", "Atomic Resistance", "Poison Resistance", "Holy Sign", \
    "Kung Fu", "Natural Defense", "Critical Hit", "Awareness" )


class StatMod( dict ):
    """A dictionary of stat bonuses, with cost() method for items, etc"""
    COM_SCORE_COST_MOD = ( 1500, 1500, 1500, 1500, 1500, 1500, \
        25, 7, 25, 15, 20, \
        25, 10, 10, 10, 5, \
        5, 5, 20, 20, 20, \
        15, 15, 30, 15, 25, \
        25, 25, 50, 10 )
    def cost( self ):
        """Return the gp cost of these stat bonuses."""
        it = 0
        for stat in range( NUM_STATS ):
            if stat in self:
                if self[ stat ] > 0:
                    it += int( self[stat] * ( self[stat] + 1 ) * self.COM_SCORE_COST_MOD[ stat ] / 10 )
                elif self[ stat ] < 0:
                    it -= int( self[stat] * ( self[stat] + 1 ) * self.COM_SCORE_COST_MOD[ stat ] / 25 )
        return it


if __name__ == '__main__':

    armor = StatMod()
    armor[ STRENGTH ] = 2
    armor[ PHYSICAL_DEFENSE ] = 40

    print armor.cost()
