import characters
import stats
import image
import items

# NPC CLASSES

class Peasant( characters.Level ):
    name = 'Peasant'
    desc = ''
    requirements = {}
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.NATURAL_DEFENSE: 3,
        stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 3, stats.AWARENESS: 4} )
    HP_DIE = 6
    MP_DIE = 4
    XP_VALUE = 50
    legal_equipment = ( items.MACE, items.DAGGER, items.STAFF, \
        items.BOW, items.ARROW, items.SHIELD, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, items.BOOTS, items.CLOAK )
    starting_equipment = (items.clothes.PeasantGarb,items.maces.Club)

class Merchant( characters.Level ):
    name = 'Merchant'
    desc = ''
    requirements = { stats.INTELLIGENCE: 7, stats.CHARISMA: 7 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.NATURAL_DEFENSE: 4,
        stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 4, stats.AWARENESS: 4} )
    HP_DIE = 8
    MP_DIE = 4
    XP_VALUE = 100
    legal_equipment = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF, \
        items.BOW, items.ARROW, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.WAND )
    starting_equipment = (items.clothes.MerchantGarb,items.daggers.Dirk)


# MONSTER CLASSES

class Humanoid( characters.Level ):
    name = 'Humanoid'
    desc = ''
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.NATURAL_DEFENSE: 3,
        stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 3, stats.AWARENESS: 3} )
    HP_DIE = 8
    MP_DIE = 8
    XP_VALUE = 100

class Spellcaster( characters.Level ):
    name = 'Spellcaster'
    desc = ''
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.NATURAL_DEFENSE: 3,
        stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 4, stats.AWARENESS: 3} )
    HP_DIE = 6
    MP_DIE = 12
    XP_VALUE = 100

class Beast( characters.Level ):
    name = 'Beast'
    desc = ''
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.NATURAL_DEFENSE: 3,
        stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 2, stats.AWARENESS: 4} )
    HP_DIE = 10
    MP_DIE = 6
    XP_VALUE = 115

class Terror( characters.Level ):
    name = 'Terror'
    desc = ''
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.NATURAL_DEFENSE: 4,
        stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 4, stats.AWARENESS: 4} )
    HP_DIE = 10
    MP_DIE = 10
    XP_VALUE = 200

class Defender( characters.Level ):
    name = 'Defender'
    desc = ''
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.NATURAL_DEFENSE: 4,
        stats.RESIST_FIRE: 4, stats.RESIST_COLD: 4, stats.RESIST_LIGHTNING: 4, stats.RESIST_ACID: 4,
        stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 4, stats.AWARENESS: 3} )
    HP_DIE = 12
    MP_DIE = 6
    XP_VALUE = 150


# Monster Monster Monster Monster Monster

class Monster( characters.Character ):
    SPRITENAME = "monster_default.png"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 12 }
    ATTACK = None
    MOVE_POINTS = 10
    ENC_LEVEL = 1

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

    def desc( self ):
        return "L"+str( self.rank())+" "+stats.GENDER[self.gender]+" "+str(self.mr_level)

    def get_move( self ):
        return self.MOVE_POINTS


