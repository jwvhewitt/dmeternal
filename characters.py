
import stats
import random

class Level( object ):
    # Or, as we would say in a PnP RPG, a "class".
    # Keeping as much info as possible in the class attributes, so after pickling
    # a character the values can be changed here and the PC will automatically
    # use the new values.
    def __init__( self, rank=1 ):
        self.rank = 0
        self.hp = 0
        self.mp = 0
        self.advance( rank )
        self.applied_rank = 0
    def get_stat_bonus( self, stat ):
        """Typical stat bonus is base bonus x rank"""
        return self.statline.get( stat , 0 ) * self.rank
    def advance( self, ranks=1 ):
        """Advance this level by the requested number of ranks."""
        for r in range( ranks ):
            self.rank += 1
            if self.rank == 1:
                self.hp = self.HP_DIE
                self.mp = self.MP_DIE
            else:
                self.hp += random.randint( 1, self.HP_DIE )
                self.mp += random.randint( 1, self.MP_DIE )

class Warrior( Level ):
    name = 'Warrior'
    desc = 'Highly trained fighters who can dish out- and take- a whole lot of physical damage.'
    requirements = { stats.STRENGTH: 11 }
    statline = { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 2, stats.MAGIC_DEFENSE: 3, \
        stats.AWARENESS: 3 }
    HP_DIE = 12
    MP_DIE = 4

class Thief( Level ):
    name = 'Thief'
    desc = 'Highly skilled at stealth and disarming traps.'
    requirements = { stats.REFLEXES: 11 }
    statline = { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 4, \
        stats.DISARM_TRAPS: 6, stats.STEALTH: 5, stats.AWARENESS: 5 }
    HP_DIE = 6
    MP_DIE = 6

class Bard( Level ):
    name = 'Bard'
    desc = 'Jacks of all trades, bards know a bit of fighting, thievery, and magic.'
    requirements = { stats.REFLEXES: 13, stats.INTELLIGENCE: 11, stats.CHARISMA: 13 }
    statline = { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 3, \
        stats.DISARM_TRAPS: 4, stats.AWARENESS: 4 }
    HP_DIE = 8
    MP_DIE = 6

class Priest( Level ):
    name = 'Priest'
    desc = 'Priests learn water, solar, and air magic. They can also use a holy sign against undead.'
    requirements = { stats.PIETY: 11 }
    statline = { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 4, \
        stats.HOLY_SIGN: 5, stats.AWARENESS: 3 }
    HP_DIE = 8
    MP_DIE = 8

class Mage( Level ):
    name = 'Mage'
    desc = 'Spellcasters who learn lunar, fire, and air magic.'
    requirements = { stats.INTELLIGENCE: 11 }
    statline = { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 4, \
        stats.AWARENESS: 3 }
    HP_DIE = 4
    MP_DIE = 10

class Druid( Level ):
    name = 'Druid'
    desc = 'A natural spellcaster who learns earth, solar, and fire magic.'
    requirements = { stats.TOUGHNESS: 9, stats.INTELLIGENCE: 11 }
    statline = { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 3, \
        stats.AWARENESS: 4 }
    HP_DIE = 6
    MP_DIE = 10

class Knight( Level ):
    name = 'Knight'
    desc = 'Blessed warrior with limited healing magic.'
    requirements = { stats.STRENGTH: 11, stats.TOUGHNESS: 11, stats.PIETY: 17, stats.CHARISMA: 13 }
    statline = { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 2, stats.MAGIC_DEFENSE: 5, \
        stats.RESIST_LUNAR: 5, stats.AWARENESS: 2 }
    HP_DIE = 10
    MP_DIE = 4

class Ranger( Level ):
    name = 'Ranger'
    desc = 'Stealthy warriors with limited earth magic.'
    requirements = { stats.STRENGTH: 11, stats.REFLEXES: 13, stats.INTELLIGENCE: 11 }
    statline = { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 3, \
        stats.DISARM_TRAPS: 3, stats.STEALTH: 5, stats.AWARENESS: 5 }
    HP_DIE = 8
    MP_DIE = 6

class Necromancer( Level ):
    name = 'Necromancer'
    desc = 'Wizards who explore the secrets of life and death. They learn lunar, earth, and water magic.'
    requirements = { stats.INTELLIGENCE: 13, stats.PIETY: 13 }
    statline = { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 4, \
        stats.AWARENESS: 3 }
    HP_DIE = 4
    MP_DIE = 12

class Samurai( Level ):
    name = 'Samurai'
    desc = "Mystic warriors. They gain lunar magic but can't use heavy armor or missile weapons."
    requirements = { stats.STRENGTH: 15, stats.REFLEXES: 11, stats.INTELLIGENCE: 13, stats.PIETY: 11 }
    statline = { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 3, \
        stats.KUNG_FU: 2, stats.AWARENESS: 3 }
    HP_DIE = 10
    MP_DIE = 6

class Monk( Level ):
    name = 'Monk'
    desc = 'Experts at unarmed fighting.'
    requirements = { stats.TOUGHNESS: 15, stats.REFLEXES: 13, stats.PIETY: 13 }
    statline = { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 4, \
        stats.KUNG_FU: 5, stats.NATURAL_DEFENSE: 4, stats.AWARENESS: 3 }
    HP_DIE = 8
    MP_DIE = 6

class Ninja( Level ):
    name = 'Ninja'
    desc = 'They have a chance to slay living targets in a single hit.'
    requirements = { stats.STRENGTH: 13, stats.TOUGHNESS: 13, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 13, stats.PIETY: 13, stats.CHARISMA: 13 }
    statline = { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 2, stats.MAGIC_DEFENSE: 3, \
        stats.DISARM_TRAPS: 4, stats.STEALTH: 5, \
        stats.NATURAL_DEFENSE: 4, stats.CRITICAL_HIT: 5, stats.AWARENESS: 4 }
    HP_DIE = 8
    MP_DIE = 4


class Character(object):
    def __init__( self ):
        self.statline = dict()
        self.levels = []

    def get_stat( self , stat ):
        # Start with the basic stat value. This will probably be 0.
        it = self.statline.get( stat , 0 )
        # Add bonuses from any earned classes...
        for l in self.levels:
            it += l.get_stat_bonus( stat )
        # Add bonuses from any equipment...

        return it

    def rank( self ):
        """Return the total ranks of this character's levels."""
        return sum( l.rank for l in self.levels )

    def max_hp( self ):
        # Bonus is the number of extra points per two levels.
        bonus = self.get_stat( stats.TOUGHNESS ) - 10
        if bonus < 0:
            bonus = 0
        return sum( l.hp for l in self.levels ) + int( bonus * self.rank() / 2 )

    def max_mp( self ):
        # Bonus is the number of extra points per two levels.
        bonus = self.get_stat( stats.PIETY ) - 10
        if bonus < 0:
            bonus = 0
        return sum( l.mp for l in self.levels ) + int( bonus * self.rank() / 2 )

if __name__ == '__main__':
    pc = Character()
    pc.levels.append( Ninja(3) )

    print pc.rank()
    print pc.get_stat( stats.PHYSICAL_ATTACK )

    pc.statline[ stats.TOUGHNESS ] = 17
    print "HP at 17:" , pc.max_hp()
    pc.statline[ stats.TOUGHNESS ] = 10
    print "HP at 10:" , pc.max_hp()


