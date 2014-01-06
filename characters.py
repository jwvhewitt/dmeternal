
import stats
import spells
import random
import image
import items
import dialogue
import teams
import effects
import animobs


class Level( object ):
    # Or, as we would say in a PnP RPG, a "class".
    # Keeping as much info as possible in the class attributes, so after pickling
    # a character the values can be changed here and the PC will automatically
    # use the new values.
    starting_equipment = ()
    name = "???"
    spell_circles = ()
    LEVELS_PER_GEM = 0
    legal_equipment = ()
    XP_VALUE = 75
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
    def advance( self, ranks=1, pc=None ):
        """Advance this level by the requested number of ranks."""
        for r in range( ranks ):
            self.rank += 1
            if self.rank == 1:
                self.hp = self.HP_DIE
                self.mp = self.MP_DIE
                for c in self.spell_circles:
                    self.spell_gems[ c ] = 1
            else:
                self.hp += max( random.randint( 1, self.HP_DIE ) , random.randint( 1, self.HP_DIE ) )
                self.mp += max( random.randint( 1, self.MP_DIE ) , random.randint( 1, self.MP_DIE ) )
                if ( self.LEVELS_PER_GEM > 0 ) and ( self.rank % self.LEVELS_PER_GEM == 0 ) and self.spell_circles:
                    self.spell_gems[ random.choice( self.spell_circles ) ] += 1
        if pc:
            # If we've been passed a character, record the most recent level.
            pc.mr_level = self

    def __str__( self ):
        return self.name

class Warrior( Level ):
    name = 'Warrior'
    desc = 'Highly trained fighters who can dish out- and take- a whole lot of physical damage.'
    requirements = { stats.STRENGTH: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 3, \
        stats.AWARENESS: 4 } )
    HP_DIE = 12
    MP_DIE = 4
    LEVELS_PER_GEM = 0
    legal_equipment = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF, \
        items.BOW, items.POLEARM, items.ARROW, items.SHIELD, items.SLING, \
        items.BULLET, items.CLOTHES, items.LIGHT_ARMOR, items.HEAVY_ARMOR, items.HAT, \
        items.HELM, items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK )
    starting_equipment = ( items.lightarmor.GladiatorArmor, items.swords.Broadsword, items.shoes.NormalBoots )


class Thief( Level ):
    name = 'Thief'
    desc = 'Highly skilled at stealth and disarming traps.'
    requirements = { stats.REFLEXES: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 5, \
        stats.DISARM_TRAPS: 6, stats.STEALTH: 5, stats.AWARENESS: 5 } )
    spell_circles = ()
    HP_DIE = 6
    MP_DIE = 6
    LEVELS_PER_GEM = 0
    legal_equipment = ( items.DAGGER, items.STAFF, \
        items.BOW, items.ARROW, items.SLING, \
        items.BULLET, items.CLOTHES, items.LIGHT_ARMOR, \
        items.HAT, items.GLOVE, items.SANDALS, \
        items.SHOES, items.BOOTS, items.CLOAK, items.WAND )
    starting_equipment = ( items.hats.Bandana, items.daggers.Dagger, items.lightarmor.PaddedArmor, items.cloaks.ThiefCloak )


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
    legal_equipment = ( items.SWORD, items.MACE, items.DAGGER, items.STAFF, \
        items.BOW, items.ARROW, items.SLING, \
        items.BULLET, items.CLOTHES, items.LIGHT_ARMOR, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.WAND )
    starting_equipment = ( items.swords.Rapier, items.hats.JauntyHat, items.lightarmor.LeatherArmor )

class Priest( Level ):
    name = 'Priest'
    desc = 'Priests learn water, solar, and air magic. They can also use a holy sign against undead.'
    requirements = { stats.PIETY: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 4, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 4, \
        stats.HOLY_SIGN: 5, stats.AWARENESS: 3 } )
    spell_circles = ( spells.WATER, spells.SOLAR, spells.AIR )
    HP_DIE = 8
    MP_DIE = 10
    LEVELS_PER_GEM = 1
    legal_equipment = ( items.MACE, items.STAFF, \
        items.SHIELD, items.SLING, \
        items.BULLET, items.CLOTHES, items.LIGHT_ARMOR, items.HEAVY_ARMOR, items.HAT, \
        items.HELM, items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.HOLYSYMBOL )
    starting_equipment = ( items.maces.FlangedMace, items.lightarmor.PaddedRobe, items.shoes.NormalBoots, items.holysymbols.WoodSymbol )

class Mage( Level ):
    name = 'Mage'
    desc = 'Spellcasters who learn lunar, fire, and air magic.'
    requirements = { stats.INTELLIGENCE: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 4, \
        stats.AWARENESS: 3 } )
    spell_circles = ( spells.LUNAR, spells.FIRE, spells.AIR )
    HP_DIE = 4
    MP_DIE = 14
    LEVELS_PER_GEM = 1
    legal_equipment = ( items.DAGGER, items.STAFF, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.WAND )
    starting_equipment = ( items.staves.Quarterstaff, items.clothes.MageRobe, items.hats.MageHat )

class Druid( Level ):
    name = 'Druid'
    desc = 'A natural spellcaster who learns earth, solar, and fire magic.'
    requirements = { stats.TOUGHNESS: 9, stats.INTELLIGENCE: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 3, \
        stats.AWARENESS: 4 } )
    spell_circles = ( spells.EARTH, spells.SOLAR, spells.FIRE )
    HP_DIE = 6
    MP_DIE = 12
    LEVELS_PER_GEM = 1
    legal_equipment = ( items.DAGGER, items.STAFF, \
        items.BOW, items.POLEARM, items.ARROW, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.WAND )
    starting_equipment = ( items.daggers.Sickle, items.clothes.DruidRobe, items.cloaks.NormalCloak )

class Knight( Level ):
    name = 'Knight'
    desc = 'Blessed warrior with limited healing magic.'
    requirements = { stats.STRENGTH: 11, stats.TOUGHNESS: 11, stats.PIETY: 17, stats.CHARISMA: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 5, \
        stats.RESIST_LUNAR: 3, stats.AWARENESS: 2 } )
    spell_circles = ( spells.SOLAR, )
    HP_DIE = 10
    MP_DIE = 4
    LEVELS_PER_GEM = 3
    legal_equipment = ( items.SWORD, items.MACE, \
        items.POLEARM, items.SHIELD, \
        items.CLOTHES, items.LIGHT_ARMOR, items.HEAVY_ARMOR, items.HAT, \
        items.HELM, items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK )
    starting_equipment = ( items.swords.Longsword, items.lightarmor.BrigandineArmor, items.shoes.NormalBoots )

class Ranger( Level ):
    name = 'Ranger'
    desc = 'Stealthy warriors with limited earth magic.'
    requirements = { stats.STRENGTH: 11, stats.REFLEXES: 13, stats.INTELLIGENCE: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 3, stats.MAGIC_DEFENSE: 3, \
        stats.DISARM_TRAPS: 3, stats.STEALTH: 4, stats.AWARENESS: 5 } )
    spell_circles = ( spells.EARTH, )
    HP_DIE = 8
    MP_DIE = 6
    LEVELS_PER_GEM = 3
    legal_equipment = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF, \
        items.BOW, items.POLEARM, items.ARROW, items.SHIELD, items.SLING, \
        items.BULLET, items.CLOTHES, items.LIGHT_ARMOR, items.HAT, \
        items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK )
    starting_equipment = ( items.axes.HandAxe, items.lightarmor.RangerArmor, items.hats.WoodsmansHat, items.shoes.NormalBoots )

class Necromancer( Level ):
    name = 'Necromancer'
    desc = 'Wizards who explore the secrets of life and death. They learn lunar, earth, and water magic.'
    requirements = { stats.INTELLIGENCE: 13, stats.PIETY: 13 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 3, stats.MAGIC_ATTACK: 5, stats.MAGIC_DEFENSE: 4, \
        stats.AWARENESS: 3 } )
    spell_circles = ( spells.LUNAR, spells.EARTH, spells.WATER )
    HP_DIE = 4
    MP_DIE = 14
    LEVELS_PER_GEM = 1
    legal_equipment = ( items.DAGGER, items.STAFF, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK, items.WAND )
    starting_equipment = ( items.staves.Quarterstaff, items.clothes.NecromancerRobe, items.hats.NecromancerHat )

class Samurai( Level ):
    name = 'Samurai'
    desc = "Mystic warriors. They gain fire magic but can't use heavy armor or missile weapons."
    requirements = { stats.STRENGTH: 15, stats.REFLEXES: 11, stats.INTELLIGENCE: 13, stats.PIETY: 11 }
    statline = stats.StatMod( { stats.PHYSICAL_ATTACK: 5, stats.MAGIC_ATTACK: 4, stats.MAGIC_DEFENSE: 3, \
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
    legal_equipment = ( items.DAGGER, items.STAFF, \
        items.BOW, items.ARROW, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK )
    starting_equipment = (items.clothes.MonkRobe, items.hats.Headband, items.staves.Quarterstaff, items.shoes.NormalSandals)

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
        items.BOW, items.ARROW, items.SLING, \
        items.BULLET, items.CLOTHES, items.HAT, \
        items.GLOVE, items.SANDALS, items.SHOES, \
        items.BOOTS, items.CLOAK )
    starting_equipment = (items.clothes.NinjaGear,items.swords.Wakizashi,items.hats.NinjaMask)

PC_CLASSES = (Warrior,Thief,Bard,Priest,Mage,Druid,Knight,Ranger,Necromancer,Samurai,Monk,Ninja)

# Player Character Species
class Human( object ):
    name = "Human"
    desc = "I will assume that you know what a human is. They have no particular strengths or weaknesses."
    sprite_name = "avatar_base.png"
    NUM_COLORS = 3
    FIRST_IMAGE = 0
    HAS_HAIR = True
    skin_color = 0
    statline = {}
    slots = ( items.BACK, items.FEET, items.BODY, items.HANDS, items.HAND1, items.HAND2, items.HEAD )
    starting_equipment = ()
    MOVE_POINTS = 10

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

class Dwarf( Human ):
    name = "Dwarf"
    desc = "They are tough, but lack reflexes"
    statline = { stats.TOUGHNESS: 2, stats.REFLEXES: -2, stats.DISARM_TRAPS: 5, stats.STEALTH: -5 }
    starting_equipment = ( items.maces.Warhammer, items.axes.WarAxe )
    VOICE = dialogue.voice.DWARVEN

class Elf( Human ):
    name = "Elf"
    desc = "They are graceful and intelligent, but somewhat frail."
    statline = { stats.STRENGTH: -1, stats.TOUGHNESS: -1, stats.REFLEXES: 1, \
        stats.INTELLIGENCE: 1 }
    FIRST_IMAGE = 6
    starting_equipment = ( items.swords.Longsword, )
    VOICE = dialogue.voice.ELVEN

class Gnome( Human ):
    name = "Gnome"
    desc = "They are very pious but lack physical strength."
    statline = { stats.STRENGTH: -2, stats.PIETY: 2, stats.STEALTH: 5 }
    starting_equipment = ( items.hats.GnomeHat, items.axes.Pickaxe )
    VOICE = dialogue.voice.GNOMIC

class Orc( Human ):
    name = "Orc"
    desc = "They are very strong, but lack intelligence."
    statline = { stats.STRENGTH: 2, stats.INTELLIGENCE: -2 }
    FIRST_IMAGE = 12
    starting_equipment = ( items.maces.Morningstar, items.axes.BattleAxe )
    VOICE = dialogue.voice.ORCISH

class Hurthling( Human ):
    name = "Hurthling"
    desc = "Hurthlings are small humanoids who live in burrows. They have good reflexes and luck, but aren't very strong or tough."
    statline = { stats.STRENGTH: -3, stats.TOUGHNESS: -2, stats.REFLEXES: 4, \
        stats.STEALTH: 10 }
    VOICE = dialogue.voice.HURTHISH

class Fuzzy( Human ):
    name = "Fuzzy"
    desc = "Fuzzies are humanoids with animal features. They are known for their exceptional luck."
    statline = { stats.INTELLIGENCE: -1, stats.PIETY: -1, stats.CHARISMA: 2 }
    FIRST_IMAGE = 18
    VOICE = dialogue.voice.KITTEH

class Reptal( Human ):
    name = "Reptal"
    desc = "Reptals are an ancient race of lizard people. They are extremely strong and tough, but quite limited in all other respects."
    statline = { stats.STRENGTH: 4, stats.TOUGHNESS: 3, stats.REFLEXES: -2, \
        stats.INTELLIGENCE: -4, stats.PIETY: -3, stats.CHARISMA: -3, \
        stats.RESIST_FIRE: 25, stats.RESIST_COLD: -25 }
    FIRST_IMAGE = 24
    NUM_COLORS = 6
    HAS_HAIR = False
    starting_equipment = ( items.maces.Club, items.clothes.AnimalSkin )
    VOICE = dialogue.voice.DRACONIAN

class Centaur( Human ):
    name = "Centaur"
    desc = "Centaurs resemble humans above the waist and horses below the neck. They can move fast in combat but cannot wear shoes."
    statline = { stats.STRENGTH: 1, stats.PIETY: -1, stats.STEALTH: -10 }
    FIRST_IMAGE = 36
    slots = ( items.BACK, items.BODY, items.HANDS, items.HAND1, items.HAND2, items.HEAD )
    starting_equipment = ( items.polearms.Spear, items.clothes.LeatherJacket )
    VOICE = dialogue.voice.GREEK
    MOVE_POINTS = 12

PC_SPECIES = (Human, Dwarf, Elf, Gnome, Orc, Hurthling, Fuzzy, Reptal, Centaur )

class CappedModifierList( list ):
    """Stat bonus from list items capped to max positive - max negative"""
    def get_stat( self , stat ):
        p_max,n_max = 0,0
        for thing in self:
            if hasattr( thing, "statline" ):
                v = thing.statline.get( stat )
                if v > 0:
                    p_max = max( v , p_max )
                elif v < 0:
                    n_max = min( v , n_max )
        return p_max + n_max

class Character(object):
    FRAME = 0
    TEMPLATES = ()
    team = None
    hidden = False

    def __init__( self, name = "", species = None, gender = stats.NEUTER, statline=None ):
        self.name = name
        if not statline:
            statline = dict()
        self.statline = statline
        self.levels = []
        self.mr_level = Level()
        self.species = species
        if species and species.HAS_HAIR:
            self.hair = random.randint( 0 , 24 )
        else:
            self.hair = 0
        self.gender = gender
        self.inventory = items.Backpack()
        self.xp = 0
        self.beard = 0
        self.hp_damage = 0
        self.mp_damage = 0
        self.stat_damage = dict()
        self.techniques = CappedModifierList()
        self.condition = CappedModifierList()

    def get_stat( self , stat ):
        if stat == None:
            return 0

        # Start with the basic stat value. This will probably be 0.
        it = self.statline.get( stat , 0 )
        # Add bonus from species...
        if self.species != None:
            it += self.species.statline.get( stat , 0 )

        # Add bonuses from any earned classes...
        for l in self.levels:
            it += l.get_stat( stat )

        # Add bonuses from any templates...
        for l in self.TEMPLATES:
            it += l.bonuses.get( stat, 0 )

        # Add bonuses from any equipment...
        for item in self.inventory:
            if item.equipped:
                it += item.statline.get( stat , 0 )

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
        mass = sum( i.mass for i in self.inventory )
        ec = self.get_encumberance_ceilings()
        if mass < ec[0]:
            return 0
        elif mass < ec[1]:
            return 1
        else:
            return 2

    def can_take_item( self, thing ):
        """Return True if this character can take this item."""
        mass = sum( i.mass for i in self.inventory )
        return ( mass + thing.mass ) <= self.get_encumberance_ceilings()[2]

    def can_use_stealth( self ):
        """Return True if this character can hide in combat."""
        return sum( l.get_stat( stats.STEALTH ) for l in self.levels ) > 0

    def can_use_holy_sign( self ):
        """Return True if this character can use holy sign in combat."""
        return sum( l.get_stat( stats.HOLY_SIGN ) for l in self.levels ) > 0

    def get_stat_bonus( self , stat ):
        if stat == None:
            return 0

        statval = max( self.get_stat( stat ) , 1 )
        return statval * 3 - 36

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
        item = self.inventory.get_equip( items.BACK )
        if item:
            item.stamp_avatar( avatar , self )

        if self.species:
            # Add the species layer.
            img,frame = self.species.get_sprite( gender = self.gender )
            img.render( avatar.bitmap , frame = frame )

        # Add the equipment layers in order, feet to just before head.
        for es in range( items.FEET, items.HEAD ):
            item = self.inventory.get_equip( es )
            if item:
                item.stamp_avatar( avatar , self )

        # Add hair and beard.
        if self.hair:
            img = image.Image( "avatar_hair.png" , 54, 54 )
            img.render( avatar.bitmap , frame = self.hair - 1 )
        if self.beard:
            img = image.Image( "avatar_beard.png" , 54, 54 )
            img.render( avatar.bitmap , frame = self.beard - 1 )

        # Now finally add the head equipment.
        item = self.inventory.get_equip( items.HEAD )
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
            while self.statline[ stat ] < 5:
                # Roll 4d6, throw away the smallest, and sum the rest.
                rolls = [ random.randint( 1 , 6 ) for x in range( 4 ) ]
                rolls.sort()
                del rolls[0]
                self.statline[ stat ] = sum( rolls )

    def advance( self, level_class ):
        """Give this character one level in the provided class."""
        # Try to find any previous training...
        level = None
        for l in self.levels:
            if isinstance( l , level_class ):
                level = l
        if not level:
            level = level_class()
            self.levels.append( level )

        # If advancing same level, get stat bonus.
        if level is self.mr_level:
            self.statline[ random.randint( 0,5 ) ] += 1
        else:
            # If adding a new level, unequip items.
            self.mr_level = level
            for i in self.inventory:
                if not self.can_equip( i ):
                    self.inventory.unequip( i )

        level.advance( pc = self )

    def alter_hair( self ):
        self.hair = ( self.hair + 1 ) % 25

    def alter_beard( self ):
        self.beard = ( self.beard + 1 ) % 10

    def __str__( self ):
        return self.name

    def desc( self ):
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

    def get_reaction( self, camp ):
        if self.team:
            return self.team.check_reaction( camp )
        else:
            return 999

    def is_hostile( self, camp ):
        """Return True if this character is hostile to the party."""
        return self.get_reaction( camp ) < teams.ENEMY_THRESHOLD

    def is_enemy( self, camp, other ):
        """Return True if other is an enemy of this model."""
        if self.is_hostile( camp ):
            return not other.is_hostile( camp )
        else:
            return other.is_hostile( camp )

    KUNG_FU_DAMAGE = ( ( 1, 2, 0, 0 ),
        ( 1, 2, 0, 0 ),( 1, 3, 0, 0 ),( 1, 4, 0, 0 ),( 1, 6, 0, 0 ),( 1, 8, 0, 0 ),
        ( 1, 8, 0, 0 ),( 1,10, 0, 0 ),( 1,10, 0, 0 ),( 2, 6, 0, 0 ),( 2, 6, 0, 0 ),
        ( 2, 6, 1, 2 ),( 2, 6, 1, 3 ),( 2, 8, 1, 4 ),( 2, 8, 1, 5 ),( 2, 8, 1, 6 ),
        ( 2, 9, 1, 6 ),( 2, 9, 1, 7 ),( 2,10, 1, 7 ),( 2,10, 1, 8 ),( 2,10, 1,10 ) )

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
            kill = effects.InstaKill( anim=animobs.CriticalHit )
            kill_roll = effects.PercentRoll( roll_skill=stats.CRITICAL_HIT, roll_stat=None, \
              roll_modifier=min(roll_mod*2,0), target_affects=True, on_success=(kill,) )
            kill_check = effects.IsAnimal( on_true=(kill_roll,) )
            hit.on_success.append( kill_check )

        return roll

    def get_attack_reach( self ):
        """Return the tile distance at which this character can attack."""
        weapon = self.inventory.get_equip( items.HAND1 )
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
        weapon = self.inventory.get_equip( items.HAND1 )
        if weapon:
            fx = weapon.attackdata.get_effect( self, roll_mod )
        elif hasattr( self, "ATTACK" ):
            fx = self.ATTACK.get_effect( self, roll_mod )
        else:
            fx = self.unarmed_attack_effect( roll_mod )
        if self.hidden:
            # Also, sneak attacks get double damage dice.
            fx.on_success[0].att_dice = (fx.on_success[0].att_dice[0]*2,fx.on_success[0].att_dice[1],fx.on_success[0].att_dice[2])
        return fx

    def get_attack_shot_anim( self ):
        weapon = self.inventory.get_equip( items.HAND1 )
        if weapon:
            return weapon.shot_anim
        else:
            return None

    def can_attack( self ):
        weapon = self.inventory.get_equip( items.HAND1 )
        if weapon:
            return weapon.can_attack( self )
        else:
            return True

    def spend_attack_price( self ):
        weapon = self.inventory.get_equip( items.HAND1 )
        if weapon:
            weapon.spend_attack_price( self )

    def number_of_attacks( self ):
        # Extra attacks = unmodified PHYSICAL_ATTACK score divided by 20
        return sum( l.get_stat( stats.PHYSICAL_ATTACK ) for l in self.levels ) // 20 + 1

    def xp_value( self ):
        # Extra attacks = unmodified PHYSICAL_ATTACK score divided by 20
        return sum( l.XP_VALUE * l.rank for l in self.levels )

    def has_template( self, temp ):
        return temp in self.TEMPLATES


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

