
import stats
import spells
import random
import image
import items
import dialogue
import effects
import animobs
import aibrain
import collections
import util
import cPickle
import context

# Reaction score constants
FRIENDLY_THRESHOLD = 25
ENEMY_THRESHOLD = -25
SAFELY_FRIENDLY = 500
SAFELY_ENEMY = -500


class Level( object ):
    # Or, as we would say in a PnP RPG, a "class".
    # Keeping as much info as possible in the class attributes, so after pickling
    # a character the values can be changed here and the PC will automatically
    # use the new values.
    starting_equipment = ()
    name = "???"
    spell_circles = ()
    LEVELS_PER_GEM = 1
    GEMS_PER_AWARD = 1
    legal_equipment = ()
    XP_VALUE = 150
    MIN_RANK = 0
    FULL_HP_AT_FIRST = True
    FRIENDMOD = dict()
    TAGS = ()

    def __init__( self, rank=0, pc=None ):
        self.rank = 0
        self.hp = 0
        self.mp = 0
        self.spell_gems = dict()
        if rank > 0:
            self.advance( rank , pc )
    def get_stat( self, stat ):
        """Typical stat bonus is base bonus x rank"""
        return self.statline.get( stat , 0 ) * self.rank
    def pick_gems( self, n=1 ):
        """Award this character some spell gems."""
        awards = list()
        for t in range( n ):
            candidates = []
            for color in self.spell_circles:
                if color not in awards:
                    if self.spell_gems[color] < 5:
                        candidates += [color,] * ( 6 - self.spell_gems[color] ) ** 2
                    else:
                        candidates.append( color )
            gem = random.choice( candidates )
            self.spell_gems[ gem ] += 1
            awards.append( gem )

    def advance( self, ranks=1, pc=None ):
        """Advance this level by the requested number of ranks."""
        for r in range( ranks ):
            self.rank += 1
            if self.rank == 1:
                if self.FULL_HP_AT_FIRST:
                    self.hp = self.HP_DIE
                    self.mp = self.MP_DIE
                else:
                    self.hp = max( random.randint( 1, self.HP_DIE ) , random.randint( 1, self.HP_DIE ) )
                    self.mp = max( random.randint( 1, self.MP_DIE ) , random.randint( 1, self.MP_DIE ) )
                for c in self.spell_circles:
                    self.spell_gems[ c ] = 1
            else:
                self.hp += max( random.randint( 1, self.HP_DIE ) , random.randint( 1, self.HP_DIE ) )
                self.mp += max( random.randint( 1, self.MP_DIE ) , random.randint( 1, self.MP_DIE ) )
                if self.spell_circles and ( self.LEVELS_PER_GEM > 0 ) and ( self.rank % self.LEVELS_PER_GEM == 0 ):
                    # When adding a random spell gem, favor the colors with low ranks.
                    self.pick_gems( self.GEMS_PER_AWARD )
        if pc:
            # If we've been passed a character, record the most recent level.
            pc.mr_level = self

    @classmethod
    def can_take_level( self, pc ):
        is_legal = pc.rank() >= self.MIN_RANK
        for k,v in self.requirements.iteritems():
            if pc.get_stat( k, include_extras=False ) < v:
                is_legal = False
        return is_legal

    def __str__( self ):
        return self.name

    @classmethod
    def stat_desc( self ):
        """Return a text description of this level's stat modifiers."""
        smod = list()
        smod.append( "HP: 1d{0}".format( self.HP_DIE ) )
        smod.append( "MP: 1d{0}".format( self.MP_DIE ) )

        for k,v in self.statline.iteritems():
            smod.append( str(k) + ":" + "{0:+}".format( v ) )
        return ", ".join( smod )

    def give_stat_advances( self, pc ):
        candidates = list()
        for s in stats.PRIMARY_STATS:
            s_weight = self.requirements.get( s, 0 ) + 10
            candidates += (s,) * s_weight
        stat_to_advance = random.choice( candidates )
        pc.statline[ stat_to_advance ] += 1
        return stat_to_advance



class Warrior( Level ):
    name = 'Warrior'
    desc = 'Highly trained fighters who can dish out- and take- a whole lot of physical damage.'
    requirements = { stats.STRENGTH: 11, stats.TOUGHNESS: 5, stats.REFLEXES: 2 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 3, \
        stats.AWARENESS: 4, stats.COUNTER_ATTACK: 3 } )
    HP_DIE = 12
    MP_DIE = 4
    LEVELS_PER_GEM = 0
    legal_equipment = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF, \
        items.BOW, items.POLEARM, items.ARROW, items.SHIELD, items.SLING, \
        items.BULLET, items.CLOTHES, items.LIGHT_ARMOR, items.HEAVY_ARMOR, items.HAT, \
        items.HELM, items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.FARMTOOL, items.LANCE )
    starting_equipment = ( items.lightarmor.GladiatorArmor, items.swords.Broadsword, items.shoes.NormalBoots )
    TAGS = (context.MTY_FIGHTER,)

class Thief( Level ):
    name = 'Thief'
    desc = 'Highly skilled at stealth and disarming traps.'
    requirements = { stats.REFLEXES: 11, stats.INTELLIGENCE: 3 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 5, \
        stats.DISARM_TRAPS: 6, stats.STEALTH: 5, stats.AWARENESS: 4, stats.LOOTING: 5 } )
    spell_circles = ()
    HP_DIE = 6
    MP_DIE = 4
    LEVELS_PER_GEM = 0
    legal_equipment = ( items.SWORD, items.DAGGER, items.STAFF, \
        items.BOW, items.ARROW, items.SLING, \
        items.BULLET, items.CLOTHES, items.LIGHT_ARMOR, \
        items.HAT, items.GLOVE, items.SANDALS, \
        items.SHOES, items.BOOTS, items.CLOAK, items.WAND )
    starting_equipment = ( items.hats.Bandana, items.daggers.Stiletto, items.lightarmor.PaddedArmor, items.cloaks.ThiefCloak )
    TAGS = (context.MTY_THIEF,)

class Bard( Level ):
    name = 'Bard'
    desc = 'Jacks of all trades, bards know a bit of fighting, thievery, and air magic.'
    requirements = { stats.REFLEXES: 13, stats.INTELLIGENCE: 11, stats.CHARISMA: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 4, \
        stats.DISARM_TRAPS: 4, stats.AWARENESS: 4 } )
    spell_circles = ( spells.AIR, )
    HP_DIE = 8
    MP_DIE = 8
    LEVELS_PER_GEM = 2
    legal_equipment = ( items.SWORD, items.MACE, items.DAGGER, items.STAFF, \
        items.BOW, items.ARROW, items.SLING, \
        items.BULLET, items.CLOTHES, items.LIGHT_ARMOR, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.WAND )
    starting_equipment = ( items.swords.Rapier, items.hats.JauntyHat, items.lightarmor.LeatherArmor )
    TAGS = (context.DES_AIR,context.GEN_KINGDOM)

class Priest( Level ):
    name = 'Priest'
    desc = 'Priests learn water, solar, and air magic. They can also use a holy sign against undead.'
    requirements = { stats.PIETY: 11, stats.INTELLIGENCE: 3, stats.CHARISMA: 3 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 4, \
        stats.HOLY_SIGN: 5, stats.AWARENESS: 3 } )
    spell_circles = ( spells.WATER, spells.SOLAR, spells.AIR )
    HP_DIE = 6
    MP_DIE = 10
    LEVELS_PER_GEM = 1
    GEMS_PER_AWARD = 2
    legal_equipment = ( items.MACE, items.STAFF, \
        items.SHIELD, items.SLING, \
        items.BULLET, items.CLOTHES, items.LIGHT_ARMOR, items.HAT, \
        items.HELM, items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.HOLYSYMBOL )
    starting_equipment = ( items.maces.FlangedMace, items.lightarmor.PaddedRobe, items.shoes.NormalBoots, items.holysymbols.WoodSymbol )
    TAGS = ( context.MTY_PRIEST, context.GEN_KINGDOM,context.DES_SOLAR,
     context.DES_AIR,context.DES_WATER )

class Mage( Level ):
    name = 'Mage'
    desc = 'Spellcasters who learn lunar, fire, and air magic.'
    requirements = { stats.INTELLIGENCE: 11, stats.PIETY: 3 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 5, \
        stats.AWARENESS: 3 } )
    spell_circles = ( spells.LUNAR, spells.FIRE, spells.AIR )
    HP_DIE = 4
    MP_DIE = 12
    LEVELS_PER_GEM = 1
    GEMS_PER_AWARD = 2
    legal_equipment = ( items.DAGGER, items.STAFF, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.WAND )
    starting_equipment = ( items.staves.Quarterstaff, items.clothes.MageRobe, items.hats.MageHat )
    TAGS = ( context.MTY_MAGE, context.GEN_KINGDOM,context.DES_LUNAR,
     context.DES_AIR,context.DES_FIRE )

class Druid( Level ):
    name = 'Druid'
    desc = 'A natural spellcaster who learns earth, solar, and fire magic.'
    requirements = { stats.TOUGHNESS: 9, stats.INTELLIGENCE: 3, stats.PIETY: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 4, \
        stats.AWARENESS: 4 } )
    spell_circles = ( spells.EARTH, spells.SOLAR, spells.FIRE )
    HP_DIE = 6
    MP_DIE = 12
    LEVELS_PER_GEM = 1
    GEMS_PER_AWARD = 2
    legal_equipment = ( items.DAGGER, items.STAFF, \
        items.BOW, items.POLEARM, items.ARROW, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.FARMTOOL )
    starting_equipment = ( items.farmtools.Sickle, items.clothes.DruidRobe, items.cloaks.NormalCloak )
    TAGS = ( context.MTY_PRIEST, context.GEN_NATURE,context.DES_SOLAR,
     context.DES_FIRE,context.DES_EARTH )

class Knight( Level ):
    name = 'Knight'
    desc = 'Blessed warrior with limited solar magic.'
    requirements = { stats.STRENGTH: 11, stats.TOUGHNESS: 11, stats.PIETY: 17, stats.CHARISMA: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 5, \
        stats.RESIST_LUNAR: 3, stats.AWARENESS: 2 } )
    spell_circles = ( spells.SOLAR, )
    HP_DIE = 10
    MP_DIE = 4
    LEVELS_PER_GEM = 3
    legal_equipment = ( items.SWORD, items.MACE, \
        items.SHIELD, \
        items.CLOTHES, items.LIGHT_ARMOR, items.HEAVY_ARMOR, items.HAT, \
        items.HELM, items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.LANCE )
    starting_equipment = ( items.swords.Longsword, items.lightarmor.BrigandineArmor, items.shoes.NormalBoots )
    TAGS = ( context.MTY_FIGHTER, context.GEN_KINGDOM,context.DES_SOLAR )

class Ranger( Level ):
    name = 'Ranger'
    desc = 'Stealthy warriors with limited earth magic.'
    requirements = { stats.STRENGTH: 11, stats.REFLEXES: 13, stats.INTELLIGENCE: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 3, \
        stats.DISARM_TRAPS: 3, stats.STEALTH: 4, stats.AWARENESS: 5 } )
    spell_circles = ( spells.EARTH, )
    HP_DIE = 8
    MP_DIE = 6
    LEVELS_PER_GEM = 3
    legal_equipment = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF, \
        items.BOW, items.POLEARM, items.ARROW, items.SHIELD, items.SLING, \
        items.BULLET, items.CLOTHES, items.LIGHT_ARMOR, items.HAT, \
        items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.FARMTOOL )
    starting_equipment = ( items.axes.HandAxe, items.lightarmor.RangerArmor, items.hats.WoodsmansHat, items.shoes.NormalBoots )
    TAGS = ( context.MTY_FIGHTER, context.GEN_NATURE,context.DES_EARTH )

class Necromancer( Level ):
    name = 'Necromancer'
    desc = 'Wizards who explore the secrets of life and death. They learn lunar, earth, and water magic.'
    requirements = { stats.INTELLIGENCE: 13, stats.PIETY: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 5, \
        stats.AWARENESS: 3 } )
    spell_circles = ( spells.LUNAR, spells.EARTH, spells.WATER )
    HP_DIE = 4
    MP_DIE = 14
    LEVELS_PER_GEM = 1
    GEMS_PER_AWARD = 2
    legal_equipment = ( items.DAGGER, items.STAFF, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.WAND, items.FARMTOOL )
    starting_equipment = ( items.staves.Quarterstaff, items.clothes.NecromancerRobe, items.hats.NecromancerHat )
    TAGS = ( context.MTY_MAGE, context.GEN_UNDEAD,context.DES_LUNAR,
     context.DES_EARTH,context.DES_WATER )

class Samurai( Level ):
    name = 'Samurai'
    desc = "Mystic warriors. They gain fire magic but can't use heavy armor or missile weapons."
    requirements = { stats.STRENGTH: 15, stats.REFLEXES: 11, stats.INTELLIGENCE: 13, stats.PIETY: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 4, \
        stats.KUNG_FU: 2, stats.AWARENESS: 3 } )
    spell_circles = ( spells.FIRE, )
    HP_DIE = 10
    MP_DIE = 6
    LEVELS_PER_GEM = 2
    legal_equipment = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF, \
        items.POLEARM, items.SHIELD, \
        items.CLOTHES, items.LIGHT_ARMOR, items.HAT, \
        items.HELM, items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK )
    starting_equipment = ( items.swords.Wakizashi, items.lightarmor.LeatherCuirass, items.shoes.NormalBoots )
    TAGS = ( context.MTY_FIGHTER,context.DES_FIRE )

class Monk( Level ):
    name = 'Monk'
    desc = 'Experts at unarmed fighting.'
    requirements = { stats.STRENGTH: 10, stats.TOUGHNESS: 15, stats.REFLEXES: 13, stats.PIETY: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 4, \
        stats.KUNG_FU: 5, stats.NATURAL_DEFENSE: 4, stats.AWARENESS: 4 } )
    spell_circles = ()
    HP_DIE = 8
    MP_DIE = 6
    LEVELS_PER_GEM = 0
    legal_equipment = ( items.DAGGER, items.STAFF, \
        items.BOW, items.ARROW, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK )
    starting_equipment = (items.clothes.MonkRobe, items.hats.Headband, items.staves.Quarterstaff, items.shoes.NormalSandals)
    TAGS = ( context.MTY_PRIEST, )

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
    legal_equipment = ( items.SWORD, items.DAGGER, items.STAFF, \
        items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK )
    starting_equipment = (items.clothes.NinjaGear,items.swords.Wakizashi,items.hats.NinjaMask)
    TAGS = ( context.MTY_THIEF, )

PC_CLASSES = (Warrior,Thief,Bard,Priest,Mage,Druid,Knight,Ranger,Necromancer,Samurai,Monk,Ninja)

# Basic Species Type

class SentientSpecies( object ):
    name = "Sentient"
    sprite_name = "avatar_base.png"
    NUM_COLORS = 3
    FIRST_IMAGE = 0
    HAS_HAIR = True
    HAIRSTYLE = { stats.MALE: (0,1,3,4,5,6,7,9, 15,16,24,26,27,30,31,34,36,38,42,43,44,45,46,47,48,49,51,52,53), \
        stats.FEMALE: (1,2,3,5,8,9, 10,11,12,13, 14,15,17,18,19,20,21,22,23,25,26,28,29,31,32,33,34,35,36,37,38,39,40,41,42,43,45,46,47), \
        stats.NEUTER: (0,1,2,3,4,5,6,7,8,9, 10,11,12,13, 14,15,16,17,18,19, 20,21,22,23,24,25,26,27,28,29, 30,31,32,33,34,35,36,37,38,39, 40,41,42,43,44,45,46,47,48,49, 51,52,53 ) }
    skin_color = 0
    statline = {}
    slots = ( items.BACK, items.FEET, items.BODY, items.HANDS, items.HAND1, items.HAND2, items.HEAD )
    starting_equipment = ()
    MOVE_POINTS = 10
    TEMPLATES = ()
    FRIENDMOD = dict()
    TAGS = ()

    def __init__( self ):
        self.skin_color = random.randint( 0 , self.NUM_COLORS - 1 )

    def get_sprite( self , gender = stats.NEUTER ):
        """Return a tuple with the image, framenum for this species."""
        img = image.Image( self.sprite_name , 54 , 54 )
        return img, self.FIRST_IMAGE + self.skin_color + self.NUM_COLORS * min( gender , 1 )

    def alter_skin_color( self ):
        """Change to the next possible skin color."""
        self.skin_color = ( self.skin_color + 1 ) % self.NUM_COLORS

    def __str__( self ):
        return self.name

    @classmethod
    def stat_desc( self ):
        """Return a text description of this species's stat modifiers."""
        smod = list()
        for k,v in self.statline.iteritems():
            smod.append( str(k) + ":" + "{0:+}".format( v ) )
        return ", ".join( smod )


# Player Character Species
class Human( SentientSpecies ):
    name = "Human"
    desc = "I will assume that you know what a human is. They have no particular strengths or weaknesses."
    TAGS = (context.GEN_KINGDOM,context.GEN_NATURE,context.GEN_CHAOS)

class Dwarf( SentientSpecies ):
    name = "Dwarf"
    desc = "They are tough, but lack reflexes"
    statline = { stats.TOUGHNESS: 2, stats.REFLEXES: -2, stats.DISARM_TRAPS: 5, stats.STEALTH: -5 }
    starting_equipment = ( items.maces.Warhammer, items.axes.WarAxe )
    VOICE = dialogue.voice.DWARVEN
    HAIRSTYLE = { stats.MALE: (0,1,3,4,5,6,7,9, 15,16,24,26,27,30,31,34,36,38,42,43,44,45,46,47,48,49,51,52,53), \
        stats.FEMALE: (1,2,3,5,8,9, 14,15,17,18,19,20,21,22,23,25,26,28,29,31,32,33,34,35,36,37,38,39,40,41,42,43,45,46,47,48,49), \
        stats.NEUTER: (0,1,2,3,4,5,6,7,8,9, 10,11,12,13, 14,15,16,17,18,19, 20,21,22,23,24,25,26,27,28,29, 30,31,32,33,34,35,36,37,38,39, 40,41,42,43,44,45,46,47,48,49, 51,52,53 ) }
    TAGS = (context.GEN_KINGDOM,context.GEN_TERRAN,context.DES_EARTH,)

class Elf( SentientSpecies ):
    name = "Elf"
    desc = "They are graceful and intelligent, but somewhat frail."
    statline = { stats.STRENGTH: -1, stats.TOUGHNESS: -1, stats.REFLEXES: 1, \
        stats.INTELLIGENCE: 1, stats.CHARISMA: 1 }
    FIRST_IMAGE = 6
    starting_equipment = ( items.swords.Longsword, )
    VOICE = dialogue.voice.ELVEN
    HAIRSTYLE = { stats.MALE: (0,1,3,4,5,6,7,9, 10,11,12,13, 16,24,26,30,31,34,36,38,42,43,44,45,46,51,52,53), \
        stats.FEMALE: (1,2,3,5,8,9, 10,11,12,13, 14,17,18,19,20,21,22,23,25,26,28,29,31,32,33,34,35,36,37,38,39,40,41,42,43,45,46), \
        stats.NEUTER: (0,1,2,3,4,5,6,7,8,9, 10,11,12,13, 14,16,17,18,19, 20,21,22,23,24,25,26,28,29, 30,31,32,33,34,35,36,37,38,39, 40,41,42,43,44,45,46, 51,52,53 ) }
    TAGS = (context.GEN_KINGDOM,context.GEN_NATURE,context.GEN_FAERIE,)

class Gnome( SentientSpecies ):
    name = "Gnome"
    desc = "They are very pious but lack physical strength."
    statline = { stats.STRENGTH: -2, stats.PIETY: 2, stats.STEALTH: 5 }
    starting_equipment = ( items.hats.GnomeHat, items.axes.Pickaxe )
    VOICE = dialogue.voice.GNOMIC
    TAGS = (context.GEN_TERRAN,context.DES_EARTH,context.MTY_THIEF)

class Orc( SentientSpecies ):
    name = "Orc"
    desc = "They are very strong, but lack intelligence."
    statline = { stats.STRENGTH: 2, stats.INTELLIGENCE: -2 }
    FIRST_IMAGE = 12
    starting_equipment = ( items.maces.Morningstar, items.axes.BattleAxe )
    VOICE = dialogue.voice.ORCISH
    HAIRSTYLE = { stats.MALE: (0,1,3,4,5,6,7,9, 15,16,24,26,27,30,31,34,36,38,42,43,44,45,46,47,48,49,51,52,53), \
        stats.FEMALE: (1,2,3,5,8,9, 14,15,17,18,19,20,21,22,23,25,26,28,29,31,32,33,34,35,36,37,38,39,40,41,42,43,45,46,47), \
        stats.NEUTER: (0,1,2,3,4,5,6,7,8,9, 10,11,12,13, 14,15,16,17,18,19, 20,21,22,23,24,25,26,27,28,29, 30,31,32,33,34,35,36,37,38,39, 40,41,42,43,44,45,46,47,48,49, 51,52,53 ) }
    TAGS = (context.GEN_GOBLIN,context.MTY_FIGHTER)

class Hurthling( SentientSpecies ):
    name = "Hurthling"
    desc = "Hurthlings are small humanoids who live in burrows. They have good reflexes and luck, but aren't very strong or tough."
    statline = { stats.STRENGTH: -3, stats.TOUGHNESS: -2, stats.REFLEXES: 4, \
        stats.STEALTH: 10 }
    VOICE = dialogue.voice.HURTHISH
    TAGS = (context.GEN_KINGDOM,context.GEN_FAERIE,context.MTY_THIEF)


class Fuzzy( SentientSpecies ):
    name = "Fuzzy"
    desc = "Fuzzies are humanoids with animal features. They are known for their exceptional luck."
    statline = { stats.INTELLIGENCE: -1, stats.PIETY: -1, stats.CHARISMA: 2 }
    FIRST_IMAGE = 18
    VOICE = dialogue.voice.KITTEH
    TAGS = (context.GEN_CHAOS,)

class Reptal( SentientSpecies ):
    name = "Reptal"
    desc = "Reptals are an ancient race of lizard people. They are extremely strong and tough, but quite limited in all other respects."
    statline = { stats.STRENGTH: 4, stats.TOUGHNESS: 3, stats.REFLEXES: -2, \
        stats.INTELLIGENCE: -4, stats.PIETY: -3, stats.CHARISMA: -3 }
    FIRST_IMAGE = 24
    NUM_COLORS = 6
    HAS_HAIR = False
    starting_equipment = ( items.maces.Club, items.clothes.AnimalSkin )
    VOICE = dialogue.voice.DRACONIAN
    TEMPLATES = (stats.REPTILE,)
    TAGS = (context.GEN_DRAGON,context.MTY_FIGHTER)

class Centaur( SentientSpecies ):
    name = "Centaur"
    desc = "Centaurs resemble humans above the waist and horses below the neck. They can move fast in combat but cannot wear shoes."
    statline = { stats.STRENGTH: 1, stats.PIETY: -1, stats.STEALTH: -10 }
    FIRST_IMAGE = 36
    slots = ( items.BACK, items.BODY, items.HANDS, items.HAND1, items.HAND2, items.HEAD )
    starting_equipment = ( items.polearms.Spear, items.clothes.LeatherJacket )
    VOICE = dialogue.voice.GREEK
    MOVE_POINTS = 12
    TAGS = (context.GEN_CHAOS,context.GEN_NATURE,)

PC_SPECIES = (Human, Dwarf, Elf, Gnome, Orc, Hurthling, Fuzzy, Reptal, Centaur )

# Set FRIENDMODs for jobs + species now that everything's defined.
Thief.FRIENDMOD = { Priest: -5, Knight: -5 }
Priest.FRIENDMOD = { Thief: -3, Necromancer: -5, Ninja: -3 }
Druid.FRIENDMOD = { Necromancer: -5 }
Knight.FRIENDMOD = { Thief: -5, Necromancer: -5, Ninja: -3 }
Ranger.FRIENDMOD = { Necromancer: -3, }
Necromancer.FRIENDMOD = { Necromancer: 3, Priest: -5, Druid: -5, Knight: -5, Ranger: -5 }
Samurai.FRIENDMOD = { Ninja: -5 }
Ninja.FRIENDMOD = { Samurai: -5 }
Human.FRIENDMOD = { Orc: -5, Reptal: -5, }
Dwarf.FRIENDMOD = { Warrior: 3, Orc: -5, Elf: -3 }
Orc.FRIENDMOD = { Dwarf: -3, Elf: -5, Human: -5 }
Elf.FRIENDMOD = { Druid: 3, Orc: -3, Dwarf: -5, Reptal: -3 }
Gnome.FRIENDMOD = { Mage: 3, Necromancer: 3 }
Hurthling.FRIENDMOD = { Hurthling: 3, Orc: -3, Reptal: -5, Centaur: -3 }
Fuzzy.FRIENDMOD = { Fuzzy: 5, }
Reptal.FRIENDMOD = { Reptal: 3, Human: -5, Dwarf: -3, Elf: -3, Hurthling: -3, Gnome: -3 }


class CappedModifierList( list ):
    """Stat bonus from list items capped to max positive - max negative"""
    def get_stat( self , stat ):
        p_max,n_max = 0,0
        for thing in self:
            if hasattr( thing, "statline" ):
                v = thing.statline.get( stat, 0 )
                if v > 0:
                    p_max = max( v , p_max )
                elif v < 0:
                    n_max = min( v , n_max )
        return p_max + n_max
    def tidy( self, dispel_this ):
        for thing in self[:]:
            if hasattr( thing, "dispel" ) and dispel_this in thing.dispel:
                self.remove( thing )
    def has_enchantment_of_type( self, find_this ):
        for thing in self:
            if hasattr( thing, "dispel" ) and find_this in thing.dispel:
                return True


class Character( stats.PhysicalThing ):
    FRAME = 0
    TEMPLATES = ()
    team = None
    hidden = False
    holy_signs_used = 0
    COMBAT_AI = aibrain.BasicAI()

    def __init__( self, name = "", species = None, gender = stats.NEUTER, statline=None ):
        self.name = name
        if not statline:
            statline = dict()
        self.statline = statline
        self.levels = []
        self.mr_level = Level()
        self.species = species
        self.gender = gender
        if species and species.HAS_HAIR:
            self.hair = random.choice( species.HAIRSTYLE[gender] )
        else:
            self.hair = -1
        self.contents = items.Backpack(owner=self)
        self.xp = 0
        self.beard = 0
        self.hp_damage = 0
        self.mp_damage = 0
        self.stat_damage = collections.defaultdict(int)
        self.techniques = CappedModifierList()
        self.condition = CappedModifierList()
        self.tags = list()

    def get_stat( self , stat, include_extras=True ):
        if stat == None:
            return 0

        # Start with the basic stat value. This will probably be 0.
        it = self.statline.get( stat , 0 )
        # Add bonus from species...
        if self.species != None:
            it += self.species.statline.get( stat , 0 )
            for l in self.species.TEMPLATES:
                it += l.bonuses.get( stat, 0 )

        # Add bonuses from any templates...
        for l in self.TEMPLATES:
            it += l.bonuses.get( stat, 0 )

        if include_extras:
            # Add bonuses from any earned classes...
            for l in self.levels:
                it += l.get_stat( stat )


            # Add bonuses from any equipment...
            for item in self.contents:
                if item.equipped:
                    it += item.get_stat( stat )

            # Add penalties from stat damage.
            it -= self.stat_damage.get( stat , 0 )

            # Add bonuses/penalties from conditions.
            it += self.condition.get_stat( stat )

            # Add bonuses from currently prepared techniques.
            it += self.techniques.get_stat( stat )

        return it

    def get_encumberance_ceilings( self ):
        """Return ceilings for light, medium, heavy encumberance."""
        strength = self.get_stat( stats.STRENGTH )
        return ( strength * 30, strength * 60, strength * 100 )

    def encumberance_level( self ):
        """Return value from 0 to 2 denoting severity of encumberance."""
        mass = sum( i.mass for i in self.contents )
        ec = self.get_encumberance_ceilings()
        if mass < ec[0]:
            return 0
        elif mass < ec[1]:
            return 1
        else:
            return 2

    def can_take_item( self, thing ):
        """Return True if this character can take this item."""
        mass = sum( i.mass for i in self.contents )
        return ( mass + thing.mass ) <= self.get_encumberance_ceilings()[2]

    def can_use_stealth( self ):
        """Return True if this character can hide in combat."""
        return self.get_stat( stats.STEALTH, False ) > 0 or sum( l.get_stat( stats.STEALTH ) for l in self.levels ) > 0

    def can_use_holy_sign( self ):
        """Return True if this character can use holy sign in combat."""
        return sum( l.get_stat( stats.HOLY_SIGN ) for l in self.levels ) > 0

    def get_stat_bonus( self , stat ):
        if stat == None:
            return 0

        statval = max( self.get_stat( stat ) , 1 )
        return ( statval - 12 ) * 2

    def get_defense( self ):
        """Return higher of physical, natural defense plus reflexes bonus"""
        statval = max( self.get_stat( stats.PHYSICAL_DEFENSE ) , self.get_stat( stats.NATURAL_DEFENSE ) )
        return statval + self.get_stat_bonus( stats.REFLEXES )

    def rank( self ):
        """Return the total ranks of this character's levels."""
        return sum( l.rank for l in self.levels )

    def max_hp( self ):
        # Bonus is the number of extra points per two levels.
        bonus = self.get_stat( stats.TOUGHNESS ) - 10
        if bonus < 0:
            bonus = 0
        return sum( l.hp for l in self.levels ) + int( bonus * self.rank() / 2 )

    def current_hp( self ):
        return self.max_hp() - self.hp_damage

    def is_alright( self ):
        return self.current_hp() > 0

    def is_dead( self ):
        return self.current_hp() <= -10

    def max_mp( self ):
        # Bonus is the number of extra points per two levels.
        bonus = self.get_stat( stats.PIETY ) - 10
        if bonus < 0:
            bonus = 0
        return sum( l.mp for l in self.levels ) + int( bonus * self.rank() / 2 )

    def current_mp( self ):
        return self.max_mp() - self.mp_damage

    def xp_for_next_level( self ):
        """Return the XP needed for next level."""
        cr = self.rank()
        return cr * ( cr + 1 ) * 500

    def eligible_for_next_level( self ):
        return self.xp > self.xp_for_next_level()

    def get_move( self ):
        if self.species:
            base = self.species.MOVE_POINTS
        elif hasattr( self, "MOVE_POINTS" ):
            base = self.MOVE_POINTS
        else:
            base = 10
        return max( 0, base - 2 * self.encumberance_level() )


    def generate_avatar( self ):
        if not self.is_alright() and self.levels:
            return image.Image( "avatar_tombstone.png", 54, 54 )

        # Generate an image for this character.
        avatar = image.Image( frame_width = 54, frame_height = 54 )
        # Add each layer in turn.
        item = self.contents.get_equip( items.BACK )
        if item:
            item.stamp_avatar( avatar , self )

        if self.species:
            # Add the species layer.
            img,frame = self.species.get_sprite( gender = self.gender )
            img.render( avatar.bitmap , frame = frame )

        # Add the equipment layers in order, feet to just before head.
        for es in range( items.FEET, items.HEAD ):
            item = self.contents.get_equip( es )
            if item:
                item.stamp_avatar( avatar , self )

        # Add hair and beard.
        if self.hair >= 0:
            img = image.Image( "avatar_hair.png" , 54, 54 )
            img.render( avatar.bitmap , frame = self.hair )
        if self.beard:
            img = image.Image( "avatar_beard.png" , 54, 54 )
            img.render( avatar.bitmap , frame = self.beard - 1 )

        # Now finally add the head equipment.
        item = self.contents.get_equip( items.HEAD )
        if item:
            item.stamp_avatar( avatar , self )

        return avatar

    def can_equip( self , item ):
        """Check if the provided item can be equipped by this character."""
        if self.mr_level and self.species:
            return ( item.itemtype in self.mr_level.legal_equipment ) and ( item.slot in self.species.slots )
        else:
            return False

    def roll_stats( self ):
        for stat in stats.PRIMARY_STATS:
            self.statline[ stat ] = 0
        #    while self.statline[ stat ] < 5:
        #        # Roll 4d6, throw away the smallest, and sum the rest.
        #        rolls = [ random.randint( 1 , 6 ) for x in range( 4 ) ]
        #        rolls.sort()
        #        del rolls[0]
        #        self.statline[ stat ] = sum( rolls )
        points = 13 * 6 + 3
        eligible_stats = list(stats.PRIMARY_STATS)
        while points > 0:
            stat_to_improve = random.choice( eligible_stats )
            if self.statline[ stat_to_improve ] > 15:
                stat_to_improve = random.choice( eligible_stats )
            self.statline[ stat_to_improve ] += 1
            points -= 1
            if self.statline[ stat_to_improve ] >= 18:
                eligible_stats.remove( stat_to_improve )

    def advance( self, level_class ):
        """Give this character one level in the provided class, return improved stat."""
        # Try to find any previous training...
        level = None
        for l in self.levels:
            if isinstance( l , level_class ):
                level = l
        if not level:
            level = level_class()
            self.levels.append( level )

        # If advancing same level, get stat bonus.
        stat_to_advance = None
        if level is self.mr_level:
            stat_to_advance = level.give_stat_advances( self )
        else:
            # If adding a new level, unequip items.
            self.mr_level = level
            for i in self.contents:
                if not self.can_equip( i ):
                    self.contents.unequip( i )

        level.advance( pc = self )
        return( stat_to_advance )

    def alter_hair( self ):
        try:
            n = self.species.HAIRSTYLE[self.gender].index(self.hair)
        except ValueError:
            n = 0
        self.hair = self.species.HAIRSTYLE[self.gender][ ( n + 1 ) % len( self.species.HAIRSTYLE[self.gender] ) ]

    def alter_beard( self ):
        self.beard = ( self.beard + 1 ) % 10

    def __str__( self ):
        return self.name

    def desc( self ):
        if self.gender == stats.NEUTER:
            return "L"+str( self.rank())+" "+str(self.species)+" "+str(self.mr_level)
        else:
            return "L"+str( self.rank())+" "+stats.GENDER[self.gender]+" "+str(self.species)+" "+str(self.mr_level)

    def get_voice( self ):
        myvoice = set()
        if hasattr( self, "VOICE" ):
            myvoice.add( self.VOICE)
        if self.species and hasattr( self.species, "VOICE" ):
            myvoice.add( self.species.VOICE )
        if self.mr_level and hasattr( self.mr_level, "VOICE" ):
            myvoice.add( self.mr_level.VOICE )
        iq = self.get_stat( stats.INTELLIGENCE )
        if iq < 9:
            myvoice.add( dialogue.voice.STUPID )
        elif iq > 15:
            myvoice.add( dialogue.voice.SMART )
        return myvoice

    def get_reaction( self, camp=None ):
        if self.team:
            if camp:
                return self.team.check_reaction( camp )
            else:
                return self.team.default_reaction
        else:
            return 999

    def get_friendliness( self, camp ):
        # The first time friendliness is queried, start with a random amount.
        if not hasattr( self, "friendliness" ):
            it = random.randint(1,11) - random.randint(1,11)
            self.friendliness = it
        else:
            it = self.friendliness
        if self.team and self.team.fac:
            it += self.team.fac.reaction

        # Modify friendliness by the npc's race and job.
        if self.species:
            for pc in camp.party:
                if pc.species:
                    it += self.species.FRIENDMOD.get( pc.species.__class__, 0 )
                    it += self.mr_level.FRIENDMOD.get( pc.species.__class__, 0 )
                it += self.species.FRIENDMOD.get( pc.mr_level.__class__, 0 )
                it += self.mr_level.FRIENDMOD.get( pc.mr_level.__class__, 0 )

        # Modify friendliness by the party spokesperson's charisma.
        pc = camp.party_spokesperson()
        it += ( pc.get_stat( stats.CHARISMA ) - 13 ) * 4

        return it

    def is_hostile( self, camp ):
        """Return True if this character is hostile to the party."""
        return self.get_reaction( camp ) < ENEMY_THRESHOLD

    def is_enemy( self, camp, other ):
        """Return True if other is an enemy of this model."""
        if other and hasattr( other, "is_hostile" ):
            if self.is_hostile( camp ):
                return not other.is_hostile( camp )
            else:
                return other.is_hostile( camp )

    def is_ally( self, camp, other ):
        """Return True if other is an ally of this model."""
        if other and hasattr( other, "is_hostile" ):
            if self.is_hostile( camp ):
                return other.is_hostile( camp )
            else:
                return not other.is_hostile( camp )

    KUNG_FU_DAMAGE = ( ( 1, 2, 0, 0 ),
        ( 1, 3, 0, 0 ),( 1, 4, 0, 0 ),( 1, 5, 0, 0 ),( 1, 6, 0, 0 ),( 1, 8, 0, 0 ),
        ( 1, 8, 1, 2 ),( 1,10, 1, 2 ),( 1,10, 1, 4 ),( 2, 6, 1, 4 ),( 2, 6, 1, 6 ),
        ( 2, 6, 1, 8 ),( 2, 7, 1, 8 ),( 2, 7, 1, 10 ),( 2, 8, 2, 6 ),( 2, 8, 2, 7 ),
        ( 2, 9, 2, 7 ),( 2, 9, 2, 8 ),( 2,10, 2, 8 ),( 2,10, 2, 9 ),( 2,10, 2,10 ) )

    def critical_hit_effect( self, roll_mod=0 ):
        return effects.TargetIs( effects.ANIMAL, on_true=(
            effects.PercentRoll( roll_skill=stats.CRITICAL_HIT, roll_stat=None, 
            roll_modifier=min(roll_mod*2,0), target_affects=True, on_success=(
                effects.InstaKill( anim=animobs.CriticalHit )
            ,) )
        ,) ) 

    def add_attack_enhancements( self, roll, ench ):
        # Add any attack modifiers attached to this enchantment.
        if hasattr( ench, "ATTACK_ON_HIT" ) and ench.ATTACK_ON_HIT:
            roll.on_success.append( ench.ATTACK_ON_HIT )

    def unarmed_attack_effect( self, roll_mod=0 ):
        """Return the attackdata for this character's unarmed strikes."""
        kungfu = self.get_stat( stats.KUNG_FU ) // 5
        dbonus = 0
        if kungfu > 20:
            dbonus = kungfu - 20
            kungfu = 20
        dice= ( self.KUNG_FU_DAMAGE[kungfu][0], self.KUNG_FU_DAMAGE[kungfu][1], dbonus )

        hit = effects.HealthDamage( att_dice=dice, stat_bonus=stats.STRENGTH, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom )
        miss = effects.NoEffect( anim=animobs.SmallBoom )
        roll = effects.PhysicalAttackRoll( att_stat=stats.STRENGTH, att_modifier=roll_mod, on_success=[hit,], on_failure=[miss,] )

        if self.KUNG_FU_DAMAGE[kungfu][2] > 0:
            dice= ( self.KUNG_FU_DAMAGE[kungfu][2], self.KUNG_FU_DAMAGE[kungfu][3], dbonus )
            hit2 = effects.HealthDamage( att_dice=dice, stat_bonus=stats.PIETY, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
            hit.on_success.append( hit2 )
            hit.on_failure.append( hit2 )

        # If the attacker has critical hit skill, use it.
        if self.get_stat( stats.CRITICAL_HIT ) > 0:
            hit.on_success.append( self.critical_hit_effect( roll_mod ) )

        return roll

    def get_attack_reach( self ):
        """Return the tile distance at which this character can attack."""
        weapon = self.contents.get_equip( items.HAND1 )
        if weapon:
            return weapon.attackdata.reach
        elif hasattr( self, "ATTACK" ):
            return self.ATTACK.reach
        else:
            return 1

    def get_attack_effect( self, roll_mod=0 ):
        """Return the effect for this character's attack."""
        if self.hidden:
            # Sneak attacks get +20% bonus
            roll_mod += 20
        weapon = self.contents.get_equip( items.HAND1 )
        if weapon:
            fx = weapon.attackdata.get_effect( self, roll_mod )
            if weapon.enhancement:
                weapon.enhancement.modify_attack( fx, self )
            if hasattr( weapon, "AMMOTYPE" ):
                ammo = self.contents.get_equip( items.HAND2 )
                if ammo and ammo.enhancement and ammo.itemtype == weapon.AMMOTYPE:
                    self.add_attack_enhancements( fx, ammo.enhancement )
        elif hasattr( self, "ATTACK" ):
            fx = self.ATTACK.get_effect( self, roll_mod )
        else:
            fx = self.unarmed_attack_effect( roll_mod )
        # Add any enchantment bonuses.
        for e in self.condition:
            self.add_attack_enhancements( fx, e )

        if self.hidden:
            # Also, sneak attacks get bonus damage.
            fx.on_success[0].att_dice = (fx.on_success[0].att_dice[0],
                fx.on_success[0].att_dice[1],max(fx.on_success[0].att_dice[2],fx.on_success[0].att_dice[2]*2)
                 + fx.on_success[0].att_dice[0]*fx.on_success[0].att_dice[1])
        return fx

    def get_attack_shot_anim( self ):
        weapon = self.contents.get_equip( items.HAND1 )
        if weapon:
            return weapon.attackdata.shot_anim
        elif hasattr( self, "ATTACK" ):
            fx = self.ATTACK.shot_anim
        else:
            return None

    def can_attack( self ):
        weapon = self.contents.get_equip( items.HAND1 )
        if weapon:
            return weapon.can_attack( self )
        else:
            return True

    def can_attack_of_opportunity( self ):
        """Return True if this character can perform an attack of opportunity."""
        weapon = self.contents.get_equip( items.HAND1 )
        if weapon and weapon.itemtype in (items.BOW, items.SLING, items.WAND ):
            return False
        else:
            return self.can_attack()

    def spend_attack_price( self ):
        weapon = self.contents.get_equip( items.HAND1 )
        if weapon:
            weapon.spend_attack_price( self )

    def series_of_attacks( self ):
        """ Return a list of attack modifiers corresponding to the number of
            attacks this character gets.
        """
        soa = [0,]
        # Unarmed combatants with kung fu get an extra attack at +0.
        if self.get_stat( stats.KUNG_FU ) > 0 and not ( self.contents.get_equip( items.HAND1 ) or self.contents.get_equip( items.HAND2 ) ):
            soa.append( 0 )
        # Extra attacks = unmodified PHYSICAL_ATTACK score divided by 20
        for t in range( sum( l.get_stat( stats.PHYSICAL_ATTACK ) for l in self.levels ) // 20 ):
            soa.append( -(t+1) * 10 )
        return soa

    def holy_signs_per_day( self ):
        # Skill can be used value/25 + 1 times.
        return sum( l.get_stat( stats.HOLY_SIGN ) for l in self.levels ) // 25 + 1

    def xp_value( self ):
        # Sum of the xp values of all held levels.
        it = sum( l.XP_VALUE * l.rank for l in self.levels )
        xp_mod = max( sum( t.xp_mod for t in self.TEMPLATES ) + 100, 50 )
        if hasattr( self, "mitose" ):
            it = int( it * 1.25 )
        if hasattr( self, "ENC_LEVEL" ) and self.ENC_LEVEL > self.rank():
            it += ( self.ENC_LEVEL - self.rank() ) * 75
        it = ( it * xp_mod ) // 100
        return it

    def has_template( self, temp ):
        return ( temp in self.TEMPLATES ) or ( self.species and temp in self.species.TEMPLATES )

    def total_spell_gems( self ):
        """Return the total number of spell gems posessed."""
        sg = sum( sum( l.spell_gems.itervalues() ) for l in self.levels )
        if sg:
            sg += ( self.get_stat( stats.INTELLIGENCE ) * self.rank() + 9 ) // 20
        return sg

    def spell_gems_of_color( self, sgcolor ):
        """Return the total number of spell gems posessed."""
        return sum( l.spell_gems.get(sgcolor,0) for l in self.levels )

    def spell_gems_used( self ):
        sgu = 0
        for s in self.techniques:
            if hasattr( s, "gems_needed" ):
                sgu += s.gems_needed()
        return sgu

    def spell_gems_of_color_used( self, sgcolor ):
        sgu = 0
        for s in self.techniques:
            if hasattr( s, "gems" ):
                sgu += s.gems.get(sgcolor,0)
        return sgu

    def choose_random_spells( self ):
        # Fill this character's spellbook with random stuff.
        while True:
            candidates = [ s for s in spells.SPELL_LIST if ( s.can_be_learned(self) and not any( s.name == t.name for t in self.techniques ) ) ]
            if candidates:
                s = random.choice( candidates )
                self.techniques.append( s )
            else:
                break

    def get_invocations( self, in_combat=False ):
        ilist = list()
        for t in self.techniques:
            if t.can_be_invoked( self, in_combat = in_combat ):
                ilist.append( t )
        for i in self.contents:
            if i.equipped and i.enhancement:
                for t in i.enhancement.TECH:
                    if t.can_be_invoked( self, in_combat = in_combat ):
                        ilist.append( t )
        return ilist

    def save( self ):
        with open( util.user_dir( "c_{}.sav".format(self.name) ) , "wb" ) as f:
            cPickle.dump( self , f, -1 )
    def backup( self ):
        with open( util.user_dir( "c_{}.backup".format(self.name) ) , "wb" ) as f:
            cPickle.dump( self , f, -1 )


    def subject_pronoun( self ):
        return stats.SUBJECT_PRONOUN[ self.gender ]

    def object_pronoun( self ):
        return stats.OBJECT_PRONOUN[ self.gender ]

    def possessive_pronoun( self ):
        return stats.POSSESSIVE_PRONOUN[ self.gender ]

    def drop_everything( self, scene ):
        # Drop everything. Pretty self-explanatory.
        for i in list(self.contents):
            if hasattr( i, "place" ):
                self.contents.remove(i)
                i.equipped = False
                i.place( scene, self.pos )


def roll_initiative( pc ):
    """Convenience function for making initiative rolls."""
    roll = pc.get_stat( stats.REFLEXES ) + random.randint( 1, 20 )
    if pc.hidden:
        roll += 20
    return roll

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

