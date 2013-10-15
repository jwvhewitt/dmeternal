
import stats
import spells
import random

# Gender tags
MALE, FEMALE, NEUTER = range( 3 )



class Level( object ):
    # Or, as we would say in a PnP RPG, a "class".
    # Keeping as much info as possible in the class attributes, so after pickling
    # a character the values can be changed here and the PC will automatically
    # use the new values.
    def __init__( self, rank=1 ):
        self.rank = 0
        self.hp = 0
        self.mp = 0
        self.spell_gems = dict()
        self.advance( rank )
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
                for c in self.spell_circles:
                    self.spell_gems[ c ] = 1
            else:
                self.hp += random.randint( 1, self.HP_DIE )
                self.mp += random.randint( 1, self.MP_DIE )
                if ( self.LEVELS_PER_GEM > 0 ) and ( self.rank % self.LEVELS_PER_GEM == 0 ) and self.spell_circles:
                    self.spell_gems[ random.choice( self.spell_circles ) ] += 1

class Warrior( Level ):
    name = 'Warrior'
    desc = 'Highly trained fighters who can dish out- and take- a whole lot of physical damage.'
    requirements = { stats.STRENGTH: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 3, \
        stats.AWARENESS: 4 } )
    spell_circles = ()
    HP_DIE = 12
    MP_DIE = 4
    LEVELS_PER_GEM = 0

class Thief( Level ):
    name = 'Thief'
    desc = 'Highly skilled at stealth and disarming traps.'
    requirements = { stats.REFLEXES: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 4, \
        stats.DISARM_TRAPS: 6, stats.STEALTH: 5, stats.AWARENESS: 5 } )
    spell_circles = ()
    HP_DIE = 6
    MP_DIE = 6
    LEVELS_PER_GEM = 0

class Bard( Level ):
    name = 'Bard'
    desc = 'Jacks of all trades, bards know a bit of fighting, thievery, and magic.'
    requirements = { stats.REFLEXES: 13, stats.INTELLIGENCE: 11, stats.CHARISMA: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 3, \
        stats.DISARM_TRAPS: 4, stats.AWARENESS: 4 } )
    spell_circles = ( spells.AIR, )
    HP_DIE = 8
    MP_DIE = 6
    LEVELS_PER_GEM = 2

class Priest( Level ):
    name = 'Priest'
    desc = 'Priests learn water, solar, and air magic. They can also use a holy sign against undead.'
    requirements = { stats.PIETY: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 4, \
        stats.HOLY_SIGN: 5, stats.AWARENESS: 3 } )
    spell_circles = ( spells.WATER, spells.SOLAR, spells.AIR )
    HP_DIE = 8
    MP_DIE = 8
    LEVELS_PER_GEM = 1

class Mage( Level ):
    name = 'Mage'
    desc = 'Spellcasters who learn lunar, fire, and air magic.'
    requirements = { stats.INTELLIGENCE: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 4, \
        stats.AWARENESS: 3 } )
    spell_circles = ( spells.LUNAR, spells.FIRE, spells.AIR )
    HP_DIE = 4
    MP_DIE = 10
    LEVELS_PER_GEM = 1

class Druid( Level ):
    name = 'Druid'
    desc = 'A natural spellcaster who learns earth, solar, and fire magic.'
    requirements = { stats.TOUGHNESS: 9, stats.INTELLIGENCE: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 3, \
        stats.AWARENESS: 4 } )
    spell_circles = ( spells.EARTH, spells.SOLAR, spells.FIRE )
    HP_DIE = 6
    MP_DIE = 10
    LEVELS_PER_GEM = 1

class Knight( Level ):
    name = 'Knight'
    desc = 'Blessed warrior with limited healing magic.'
    requirements = { stats.STRENGTH: 11, stats.TOUGHNESS: 11, stats.PIETY: 17, stats.CHARISMA: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 5, \
        stats.RESIST_LUNAR: 5, stats.AWARENESS: 2 } )
    spell_circles = ( spells.SOLAR, )
    HP_DIE = 10
    MP_DIE = 4
    LEVELS_PER_GEM = 3

class Ranger( Level ):
    name = 'Ranger'
    desc = 'Stealthy warriors with limited earth magic.'
    requirements = { stats.STRENGTH: 11, stats.REFLEXES: 13, stats.INTELLIGENCE: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 3, \
        stats.DISARM_TRAPS: 3, stats.STEALTH: 5, stats.AWARENESS: 5 } )
    spell_circles = ( spells.EARTH, )
    HP_DIE = 8
    MP_DIE = 6
    LEVELS_PER_GEM = 3

class Necromancer( Level ):
    name = 'Necromancer'
    desc = 'Wizards who explore the secrets of life and death. They learn lunar, earth, and water magic.'
    requirements = { stats.INTELLIGENCE: 13, stats.PIETY: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 4, \
        stats.AWARENESS: 3 } )
    spell_circles = ( spells.LUNAR, spells.EARTH, spells.WATER )
    HP_DIE = 4
    MP_DIE = 12
    LEVELS_PER_GEM = 1

class Samurai( Level ):
    name = 'Samurai'
    desc = "Mystic warriors. They gain lunar magic but can't use heavy armor or missile weapons."
    requirements = { stats.STRENGTH: 15, stats.REFLEXES: 11, stats.INTELLIGENCE: 13, stats.PIETY: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 3, \
        stats.KUNG_FU: 2, stats.AWARENESS: 3 } )
    spell_circles = ( spells.LUNAR, )
    HP_DIE = 10
    MP_DIE = 6
    LEVELS_PER_GEM = 2

class Monk( Level ):
    name = 'Monk'
    desc = 'Experts at unarmed fighting.'
    requirements = { stats.TOUGHNESS: 15, stats.REFLEXES: 13, stats.PIETY: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 4, \
        stats.KUNG_FU: 5, stats.NATURAL_DEFENSE: 4, stats.AWARENESS: 4 } )
    spell_circles = ()
    HP_DIE = 8
    MP_DIE = 6
    LEVELS_PER_GEM = 0

class Ninja( Level ):
    name = 'Ninja'
    desc = 'They have a chance to slay living targets in a single hit.'
    requirements = { stats.STRENGTH: 13, stats.TOUGHNESS: 13, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 13, stats.PIETY: 13, stats.CHARISMA: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 2, \
        stats.MAGIC_DEFENSE: 3, stats.DISARM_TRAPS: 4, stats.STEALTH: 5, \
        stats.NATURAL_DEFENSE: 4, stats.CRITICAL_HIT: 5, stats.AWARENESS: 4 } )
    spell_circles = ()
    HP_DIE = 8
    MP_DIE = 4
    LEVELS_PER_GEM = 0

PC_CLASSES = (Warrior,Thief,Bard,Priest,Mage,Druid,Knight,Ranger,Necromancer,Samurai,Monk,Ninja)

# Player Character Species
class Human( object ):
    name = "Human"
    desc = "I will assume that you know what a human is. They have no particular strengths or weaknesses."
    statline = {}

class Dwarf( object ):
    name = "Dwarf"
    desc = "They are tough, but lack reflexes"
    statline = { stats.TOUGHNESS: 2, stats.REFLEXES: -2 }

class Elf( object ):
    name = "Elf"
    desc = "They are graceful and intelligent, but somewhat frail."
    statline = { stats.STRENGTH: -1, stats.TOUGHNESS: -1, stats.REFLEXES: 1, \
        stats.INTELLIGENCE: 1 }

class Gnome( object ):
    name = "Gnome"
    desc = "They are very pious but lack physical strength."
    statline = { stats.STRENGTH: -2, stats.PIETY: 2, stats.STEALTH: 5 }

class Orc( object ):
    name = "Orc"
    desc = "They are very strong, but lack intelligence."
    statline = { stats.STRENGTH: 2, stats.INTELLIGENCE: -2 }

class Hurthling( object ):
    name = "Hurthling"
    desc = "Hurthlings are small humanoids who live in burrows. They have good reflexes and luck, but aren't very strong or tough."
    statline = { stats.STRENGTH: -3, stats.TOUGHNESS: -2, stats.REFLEXES: 4, \
        stats.STEALTH: 10 }

class Fuzzy( object ):
    name = "Fuzzy"
    desc = "Fuzzies are humanoids with animal features. They are known for their exceptional luck."
    statline = { stats.INTELLIGENCE: -1, stats.PIETY: -1, stats.CHARISMA: 2 }

class Reptal( object ):
    name = "Reptal"
    desc = "Reptals are an ancient race of lizard people. They are extremely strong and tough, but quite limited in all other respects."
    statline = { stats.STRENGTH: 4, stats.TOUGHNESS: 3, stats.REFLEXES: -2, \
        stats.INTELLIGENCE: -4, stats.PIETY: -3, stats.CHARISMA: -3, \
        stats.RESIST_FIRE: 25, stats.RESIST_COLD: -25 }

class Centaur( object ):
    name = "Centaur"
    desc = "Centaurs resemble humans above the waist and horses below the neck. They can move fast in combat but cannot wear shoes."
    statline = { stats.STRENGTH: 1, stats.PIETY: -1, stats.STEALTH: -10 }


class Character(object):
    def __init__( self, species = None, gender = NEUTER ):
        self.statline = dict()
        self.levels = []
        self.species = species
        self.gender = gender

    def get_stat( self , stat ):
        # Start with the basic stat value. This will probably be 0.
        it = self.statline.get( stat , 0 )
        # Add bonus from species...
        if self.species != None:
            it += self.species.statline.get( stat , 0 )

        # Add bonuses from any earned classes...
        for l in self.levels:
            it += l.get_stat_bonus( stat )
        # Add bonuses from any equipment...

        return it

    def get_stat_bonus( self , stat ):
        statval = max( self.get_stat( stat ) , 1 )
        return statval * 3 - 36

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
    pc.levels.append( Druid(3) )

    print pc.rank()
    print pc.get_stat( stats.PHYSICAL_ATTACK )

    pc.statline[ stats.TOUGHNESS ] = 17
    print "HP at 17:" , pc.max_hp()
    pc.statline[ stats.TOUGHNESS ] = 10
    print "HP at 10:" , pc.max_hp()

    print "\n***Level Stats***"
    for c in PC_CLASSES:
        print c.name + ': ' + str( c.statline.cost() )

