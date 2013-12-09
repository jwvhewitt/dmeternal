import characters
import stats
import image

# MONSTER CLASSES

class Humanoid( characters.Level ):
    name = 'Humanoid'
    desc = ''
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.PHYSICAL_DEFENSE: 3,
        stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 3, stats.AWARENESS: 3} )
    HP_DIE = 8
    MP_DIE = 8
    XP_VALUE = 100

class Spellcaster( characters.Level ):
    name = 'Spellcaster'
    desc = ''
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.PHYSICAL_DEFENSE: 3,
        stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 4, stats.AWARENESS: 3} )
    HP_DIE = 6
    MP_DIE = 12
    XP_VALUE = 100

class Beast( characters.Level ):
    name = 'Beast'
    desc = ''
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.PHYSICAL_DEFENSE: 3,
        stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 2, stats.AWARENESS: 4} )
    HP_DIE = 10
    MP_DIE = 6
    XP_VALUE = 115

class Terror( characters.Level ):
    name = 'Terror'
    desc = ''
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.PHYSICAL_DEFENSE: 4,
        stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 4, stats.AWARENESS: 4} )
    HP_DIE = 10
    MP_DIE = 10
    XP_VALUE = 200

class Defender( characters.Level ):
    name = 'Defender'
    desc = ''
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.PHYSICAL_DEFENSE: 4,
        stats.RESIST_FIRE: 4, stats.RESIST_COLD: 4, stats.RESIST_LIGHTNING: 4, stats.RESIST_ACID: 4,
        stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 4, stats.AWARENESS: 3} )
    HP_DIE = 12
    MP_DIE = 6
    XP_VALUE = 150

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

UNDEAD = SingTemp( "UNDEAD", { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 5, \
    stats.RESIST_COLD: 50, stats.RESIST_LUNAR: 50, stats.RESIST_SOLAR: -100, \
    stats.RESIST_POISON: 155 } )
BONE = SingTemp( "BONE", { stats.RESIST_SLASHING: 50, stats.RESIST_PIERCING: 50 } )

CONSTRUCT = SingTemp( "CONSTRUCT", { stats.RESIST_CRUSHING: 25, stats.RESIST_PIERCING: 25, \
    stats.RESIST_SLASHING: 25, stats.RESIST_WATER: -100, stats.RESIST_ATOMIC: -300, \
    stats.RESIST_POISON: 155, stats.AWARENESS: -10 } )
PLANT = SingTemp( "PLANT", { stats.RESIST_FIRE: -100, stats.RESIST_SOLAR: 50, \
    stats.RESIST_WATER: 250, stats.AWARENESS: -10 })
ELEMENTAL = SingTemp( "ELEMENTAL", { stats.PHYSICAL_DEFENSE: 5, stats.MAGIC_DEFENSE: -5, \
    stats.RESIST_ATOMIC: -100, stats.RESIST_POISON: 155 })
DEMON = SingTemp( "DEMON", { stats.MAGIC_DEFENSE: 5, stats.RESIST_FIRE: 75, stats.RESIST_LUNAR: 75, \
    stats.RESIST_SOLAR: -100, stats.RESIST_POISON: 100 })
BUG = SingTemp( "BUG", { stats.PHYSICAL_DEFENSE: 10, stats.MAGIC_DEFENSE: -10, \
    stats.RESIST_SLASHING: 50, stats.RESIST_ACID: -100, stats.RESIST_POISON: -100 })
REPTILE = SingTemp( "REPTILE", { stats.RESIST_FIRE: 50, stats.RESIST_COLD: -50 })
DRAGON = SingTemp( "DRAGON", { stats.PHYSICAL_DEFENSE: 10, stats.MAGIC_DEFENSE: 10, \
    stats.RESIST_FIRE: 50, stats.RESIST_COLD: 50, stats.RESIST_ACID: 50, \
    stats.RESIST_LIGHTNING: 50, stats.RESIST_POISON: 50, stats.RESIST_SLASHING: 33, \
    stats.RESIST_CRUSHING: 33, stats.AWARENESS: 15 })
FIRE = SingTemp( "FIRE", { stats.PHYSICAL_ATTACK: 5, stats.PHYSICAL_DEFENSE: -5, \
    stats.RESIST_FIRE: 100, stats.RESIST_COLD: -100, \
    stats.RESIST_WATER: -100, stats.RESIST_ATOMIC: 50 })
WATER = SingTemp( "WATER", { stats.MAGIC_ATTACK: -5, stats.MAGIC_DEFENSE: 5, \
    stats.RESIST_FIRE: 50, stats.RESIST_COLD: 50, \
    stats.RESIST_LIGHTNING: -100, stats.RESIST_ACID: -100, stats.RESIST_WATER: 50 })
EARTH = SingTemp( "EARTH", { stats.PHYSICAL_ATTACK: -5, stats.PHYSICAL_DEFENSE: 5, \
    stats.RESIST_CRUSHING: -50, stats.RESIST_LIGHTNING: 100, stats.RESIST_ACID: 50, \
    stats.RESIST_WIND: -100, stats.RESIST_WATER: -100 })
AIR = SingTemp( "AIR", { stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: -5, \
    stats.RESIST_SLASHING: -50, stats.RESIST_FIRE: -100, stats.RESIST_ACID: 50, \
    stats.RESIST_WIND: 50 })
ICE = SingTemp( "ICE", { stats.RESIST_PIERCING: -100, stats.RESIST_FIRE: -100, \
    stats.RESIST_COLD: 100, stats.RESIST_WIND: 50, stats.RESIST_WATER: 50 })

# Monster Monster Monster Monster Monster

class Monster( characters.Character ):
    SPRITENAME = "monster_default.png"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12 }
    ATTACK = None

    def __init__( self, team = None ):
        super(Monster, self).__init__( name=self.name, statline=self.statline )
        self.team = team
        self.init_monster()

    def init_monster( self ):
        """Initialize this monster's levels."""
        pass

    def generate_avatar( self ):
        # Generate an image for this character.
        return image.Image( self.SPRITENAME, frame_width = 54, frame_height = 54 )




