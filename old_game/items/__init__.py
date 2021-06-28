from .. import stats
from .. import image
import inspect
from .. import effects
from .. import animobs
import random
import math
from .. import container

# Enumerated constants for the item slots.
# Note that these are defined in the order in which they're applied to avatar.
NOSLOT, BACK, FEET, BODY, HANDS, HAND2, HAND1, HEAD = list(range( 100, 108))

class SingType( object ):
    # A singleton itemtype class; use these objects as tokens to indicate
    # the type of items.
    # Also includes misc information related to the itemtype in question.
    def __init__( self, ident, name, slot = NOSLOT, cost_adjust=1.0, rank_adjust=1.0 ):
        # ident should be the module-level name of this object.
        self.ident = ident
        self.name = name
        self.slot = slot
        self.cost_adjust = cost_adjust
        self.rank_adjust = rank_adjust
    def __str__( self ):
        return self.name
    def __reduce__( self ):
        return self.ident

GENERIC = SingType( "GENERIC", "Item" )
SWORD = SingType( "SWORD", "Sword", slot = HAND1 )
AXE = SingType( "AXE", "Axe", slot = HAND1 )
MACE = SingType( "MACE", "Mace", slot = HAND1, rank_adjust=1.2 )
DAGGER = SingType( "DAGGER", "Dagger", slot = HAND1, rank_adjust=1.5 )
STAFF = SingType( "STAFF", "Staff", slot = HAND1, rank_adjust=2.0 )
BOW = SingType( "BOW", "Bow", slot = HAND1 )
POLEARM = SingType( "POLEARM", "Polearm", slot = HAND1 )
ARROW = SingType( "ARROW", "Arrow", slot = HAND2 )
SHIELD = SingType( "SHIELD", "Shield", slot = HAND2, cost_adjust=1.75, rank_adjust=0.8 )
SLING = SingType( "SLING", "Sling", slot = HAND1 )
BULLET = SingType( "BULLET", "Bullet", slot = HAND2 )
CLOTHES = SingType( "CLOTHES", "Clothes", slot = BODY, cost_adjust=1.25 )
LIGHT_ARMOR = SingType( "LIGHT_ARMOR", "Light Armor", slot = BODY, rank_adjust=0.90 )
HEAVY_ARMOR = SingType( "HEAVY_ARMOR", "Heavy Armor", slot = BODY, rank_adjust=0.75 )
HAT = SingType( "HAT", "Hat", slot = HEAD, cost_adjust=3.5 )
HELM = SingType( "HELM", "Helm", slot = HEAD, cost_adjust=3.0 )
GLOVE = SingType( "GLOVE", "Gloves", slot = HANDS, cost_adjust=4.0 )
GAUNTLET = SingType( "GAUNTLET", "Gauntlets", slot = HANDS, cost_adjust=3.5 )
SANDALS = SingType( "SANDALS", "Sandals", slot = FEET )
SHOES = SingType( "SHOES", "Shoes", slot = FEET )
BOOTS = SingType( "BOOTS", "Boots", slot = FEET )
CLOAK = SingType( "CLOAK", "Cloak", slot = BACK )
HOLYSYMBOL = SingType( "HOLYSYMBOL", "Symbol", slot = HAND2 )
WAND = SingType( "WAND", "Wand", slot = HAND1, cost_adjust=3.0 )
FARMTOOL = SingType( "FARMTOOL", "Farm Tool", slot = HAND1 )
SCROLL = SingType( "SCROLL", "Scroll" )
POTION = SingType( "POTION", "Potion" )
GEM = SingType( "GEM", "Gem" )
LANCE = SingType( "LANCE", "Lance", slot = HAND1, cost_adjust=1.2 )

class Attack( object ):
    def __init__( self, damage = (1,6,0), skill_mod = stats.STRENGTH, damage_mod = stats.STRENGTH,
         double_handed = False, element = stats.RESIST_SLASHING, reach = 1, hit_anim=animobs.RedBoom,
         shot_anim=None, extra_effect = None ):
        self.damage = damage
        self.skill_mod = skill_mod
        self.damage_mod = damage_mod
        self.double_handed = double_handed
        self.element = element
        self.reach = reach
        self.hit_anim = hit_anim
        self.shot_anim = shot_anim
        self.extra_effect = extra_effect
    def cost( self ):
        """Return the GP value of this attack."""
        # Calculate the maximum damage that can be rolled.
        D = self.damage[0] * self.damage[1] + self.damage[2]
        # Base price is this amount squared, plus number of dice squared.
        it = D ** 2 + self.damage[0] ** 2
        # Increase if double handed.
        if self.double_handed:
            it = ( it * 6 ) // 5
        # Modify for range; each point increases cost by a third.
        if self.reach > 1:
            it = it * ( self.reach + 2 ) // 3
        # If weapon performance unaffected by stats, make it cheaper.
        if not self.skill_mod:
            it = ( it * 4 ) // 5
        if not self.damage_mod:
            it = ( it * 4 ) // 5
        # "extra_effect" is generally used for monster attacks, but if used for
        # a PC weapon we'll guesstimate.
        if self.extra_effect:
            it = int(it * 1.5)
        # Multiply by element cost.
        if self.element:
            it *= self.element.element_cost_mod
        else:
            it *= 5
        return it
    def stat_desc( self ):
        """Return a string describing this attack."""
        it = "{0}d{1}{2:+} {3} damage".format(self.damage[0],self.damage[1],self.damage[2], self.element.element_name )
        if self.double_handed:
            it = "2H " + it
        if self.extra_effect:
            it = it + "+FX"
        if self.reach > 1:
            it = it + ", Range:{0}".format( self.reach )
        return it
    def get_effect( self, user, att_modifier=0, target=None ):
        """Generate an effect tree for this attack."""
        dmg = list( self.damage )
        dmg[2] += user.get_stat( stats.WEAPON_DAMAGE_BONUS )
        hit = effects.HealthDamage( att_dice=dmg, stat_bonus=self.damage_mod, element=self.element, anim=self.hit_anim )
        if self.double_handed:
            hit.stat_mod = 1.5
        miss = effects.NoEffect( anim=animobs.SmallBoom )
        roll = effects.PhysicalAttackRoll( att_stat=self.skill_mod, att_modifier=att_modifier, on_success=[hit,], on_failure=[miss,] )

        if self.extra_effect:
            roll.on_success.append( self.extra_effect )

        # If the attacker has critical hit skill, use it.
        if user.get_stat( stats.CRITICAL_HIT ) > 0:
            hit.on_success.append( user.critical_hit_effect( att_modifier ) )

        return roll


class Item( stats.PhysicalThing ):
    true_name = "Item"
    true_desc = ""
    statline = stats.StatMod()
    itemtype = GENERIC
    identified = True
    attackdata = None
    avatar_image = None
    avatar_frame = 0
    mass = 1
    equipped = False
    enhancement = None
    def cost( self, include_enhancement=True, include_adjust=True ):
        it = 1
        if self.statline:
            it += self.statline.cost()
        if self.attackdata:
            it += self.attackdata.cost()
        if include_adjust:
            it = int( it * self.itemtype.cost_adjust )
        if self.enhancement and include_enhancement:
            it += self.enhancement.cost()
        return it
    def stamp_avatar( self, avatar, pc ):
        """Apply this item's sprite to the avatar."""
        if self.avatar_image:
            img = image.Image( self.avatar_image , 54 , 54 )
            img.render( avatar.bitmap , frame = self.avatar_frame )
    def is_better( self, other ):
        """Check whether self is more expensive than other."""
        if not other:
            return True
        else:
            try:
                return self.cost() >= other.cost()
            except AttributeError:
                # The other is apparently not an item, so this is obviously better.
                return True
    def get_stat( self, stat ):
        it = self.statline.get( stat, 0 )
        if self.enhancement:
            it += self.enhancement.get_stat( stat )
        return it
    def __str__( self ):
        if self.identified:
            if self.enhancement:
                return self.enhancement.get_name( self )
            else:
                return self.true_name
        else:
            return "?{}".format(self.itemtype.name)
    def desc( self ):
        if self.identified:
            msg = self.true_desc
            if self.enhancement:
                msg = self.enhancement.modify_desc( msg )
            return msg
        else:
            return "???"
    def stat_desc( self ):
        """Return descriptions of all stat modifiers provided."""
        smod = []
        if self.attackdata:
            smod.append( self.attackdata.stat_desc() )
        for k in stats.PUBLIC_STATS:
            v = self.get_stat( k )
            if v:
                smod.append( str(k) + ":" + "{0:+}".format( v ) )
        return ", ".join( smod )

    def can_attack( self, user ):
        """Return True if this weapon can be used to attack right now."""
        return True
    def spend_attack_price( self, user ):
        """Spend this weapon's attack price."""
        pass
    def min_rank( self ):
        base_cost = self.cost(include_enhancement=False)
        mr = int( ( -9 + math.sqrt( 81 + 36 * base_cost * self.itemtype.rank_adjust ) ) / 18 )
        if self.enhancement:
            mr += self.enhancement.min_rank()
        return mr

    @property
    def slot( self ):
        return self.itemtype.slot

class MissileWeapon( Item ):
    AMMOTYPE = ARROW
    def cost( self, include_enhancement=True ):
        it = 1
        if self.statline != None:
            it += self.statline.cost()
        if self.attackdata != None:
            # Missile weapons only pay half normal cost for attackdata.
            it += self.attackdata.cost() // 2
        it = int( it * self.itemtype.cost_adjust )
        if self.enhancement and include_enhancement:
            it += self.enhancement.cost()
        return it
    def can_attack( self, user ):
        """Return True if this weapon can be used to attack right now."""
        h2 = user.contents.get_equip( HAND2 )
        return h2 and h2.itemtype == self.AMMOTYPE
    def spend_attack_price( self, user ):
        """Spend this weapon's attack price."""
        h2 = user.contents.get_equip( HAND2 )
        h2.quantity += -1
        if h2.quantity < 1:
            user.contents.remove( h2 )

class Stackable( Item ):
    quantity = 1
    mass_per_q = 1
    cost_per_q = 1
    max_q = 10

    def cost( self, include_enhancement=True ):
        it = self.cost_per_q * self.quantity

        if self.statline != None:
            it += self.statline.cost()
        if self.attackdata != None:
            it += self.attackdata.cost()
        it = int( it * self.itemtype.cost_adjust )
        if self.enhancement and include_enhancement:
            it += ( self.enhancement.cost() * self.quantity ) // 25
        return it

    def can_stack_with( self, other ):
        # Return True if these things can stack.
        return self.__class__ == other.__class__ and not self.enhancement and \
         not other.enhancement and self.identified and other.identified and \
         ( self.quantity + other.quantity ) <= self.max_q

    @property
    def mass( self ):
        return self.quantity * self.mass_per_q

    def __str__( self ):
        if self.identified:
            if self.enhancement:
                msg = self.enhancement.get_name( self )
            else:
                msg = self.true_name
        else:
            msg = "?"+self.itemtype.name
        return "{0} [{1}]".format( msg, self.quantity )

class Consumable( Stackable ):
    itemtype = POTION
    tech = None
    def use( self, user, explo ):
        # The player wants to use this item.
        if self.tech and self.tech.can_be_invoked( user, explo.camp.fight ):
            if explo.camp.fight:
                uzd = explo.pc_use_technique( user, self.tech, self.tech.com_tar )
            else:
                uzd = explo.pc_use_technique( user, self.tech, self.tech.exp_tar )
            if uzd:
                self.quantity += -1
                if self.quantity < 1:
                    user.contents.remove( self )
            return uzd
        else:
            explo.alert( "{0} cannot be used right now.".format( self ) )


class Ammo( Stackable ):
    quantity = 20
    mass_per_q = 1
    itemtype = ARROW
    cost_per_q = 1
    max_q = 60

class ManaWeapon( Item ):
    MP_COST = 1
    def cost( self, include_enhancement=True ):
        it = 1
        if self.statline != None:
            it += self.statline.cost()
        if self.attackdata != None:
            # Mana weapons only pay 3/4 normal cost for attackdata.
            it += ( self.attackdata.cost() * 3 ) // 4
        it = int( it * self.itemtype.cost_adjust )
        if self.enhancement and include_enhancement:
            it += self.enhancement.cost()
        if self.MP_COST > 1:
            #it = it * ( self.MP_COST + 15 ) // ( 4 * self.MP_COST + 12 )
            it = it * 2 // ( self.MP_COST + 1 )
        return it
    def stat_desc( self ):
        """Return descriptions of all stat modifiers provided."""
        smod = []
        if self.attackdata:
            smod.append( self.attackdata.stat_desc() )
            if self.MP_COST:
                smod.append( "{0} MP".format( self.MP_COST ) )
        for k in stats.PUBLIC_STATS:
            v = self.get_stat( k )
            if v:
                smod.append( str(k) + ":" + "{0:+}".format( v ) )
        return ", ".join( smod )
    def can_attack( self, user ):
        """Return True if this weapon can be used to attack right now."""
        return user.current_mp() >= self.MP_COST
    def spend_attack_price( self, user ):
        """Spend this weapon's attack price."""
        user.mp_damage += self.MP_COST

class Clothing( Item ):
    true_name = "Travelers Garb"
    true_desc = ""
    itemtype = CLOTHES
    avatar_image = "avatar_clothing.png"
    avatar_frame = 3
    male_frame = None
    pants_image = "avatar_legs.png"
    pants_frame = 3
    male_pants = None
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })
    mass = 20
    def stamp_avatar( self, avatar, pc ):
        """Apply this item's sprite to the avatar."""
        if self.pants_image and pc.species and ( FEET in pc.species.slots ):
            img = image.Image( self.pants_image , 54 , 54 )
            if ( pc.gender == stats.MALE ) and self.male_pants:
                frame = self.male_pants
            else:
                frame = self.pants_frame
            img.render( avatar.bitmap , frame = frame )
        if self.avatar_image:
            img = image.Image( self.avatar_image , 54 , 54 )
            if ( pc.gender == stats.MALE ) and self.male_frame:
                frame = self.male_frame
            else:
                frame = self.avatar_frame
            img.render( avatar.bitmap , frame = frame )


from . import axes
from . import bows
from . import cloaks
from . import clothes
from . import daggers
from . import farmtools
from . import gauntlets
from . import gloves
from . import hats
from . import heavyarmor
from . import helms
from . import holysymbols
from . import knickknacks
from . import lightarmor
from . import maces
from . import polearms
from . import potions
from . import scrolls
from . import shields
from . import shoes
from . import slings
from . import staves
from . import swords
from . import wands

# Compile the items into a useful list.
ITEM_LIST = []
def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if inspect.isclass( o ) and issubclass( o , Item ) and o not in (Item, MissileWeapon, Ammo, ManaWeapon, Clothing, Stackable, Consumable):
            ITEM_LIST.append( o )

harvest( axes )
harvest( bows )
harvest( cloaks )
harvest( clothes )
harvest( daggers )
harvest( farmtools )
harvest( gauntlets )
harvest( gloves )
harvest( hats )
harvest( heavyarmor )
harvest( helms )
harvest( holysymbols )
harvest( knickknacks )
harvest( lightarmor )
harvest( maces )
harvest( polearms )
harvest( potions )
harvest( scrolls )
harvest( shields )
harvest( shoes )
harvest( slings )
harvest( staves )
harvest( swords )
harvest( wands )

# Test Items
#for ic in ITEM_LIST:
#    i = ic()
#    if i.itemtype in (WAND,POTION,GEM ):
#        print "{0}: {1}/{2}gp".format( i, i.min_rank(), i.cost() )

from . import enhancers
# Compile the enhancements into a useful list.
def harvest_enhancements( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if inspect.isclass( o ) and issubclass( o , enhancers.Enhancer ) and o is not enhancers.Enhancer:
            enhancers.ENHANCEMENT_LIST.append( o )
harvest_enhancements( enhancers )

def choose_item( item_type=None, max_rank=20 ):
    """Return an item of the specified type, of at most max_rank."""
    candidates = []
    for ic in ITEM_LIST:
        i = ic()
        if i.min_rank() <= max_rank and ( i.itemtype == item_type or not item_type ):
            candidates.append( i )
#            candidates += [i,] * ( i.min_rank() + 2 )
    if candidates:
        return random.choice( candidates )

def generate_scroll( target_rank=1 ):
    """Return a spell scroll of rank closest to, but not over, target_rank."""
    best_scroll = None
    best_rank = 0
    for ic in ITEM_LIST:
        if issubclass( ic, scrolls.Rank1Scroll ):
            i = ic()
            if i.min_rank() <= target_rank and i.min_rank() > best_rank:
                best_scroll = i
                best_rank = i.min_rank()
    return best_scroll


def make_item_magic( item_to_enchant, target_rank ):
    pr = target_rank - item_to_enchant.min_rank()
    e = enhancers.select_enhancer( item_to_enchant, pr )
    if e:
        item_to_enchant.enhancement = e(item_to_enchant,points=pr)


WEAPON_TYPES = (SWORD,AXE,MACE,DAGGER,STAFF,BOW,SHIELD,POLEARM,SLING,FARMTOOL,LANCE)

PREMIUM_TYPES = (SWORD,AXE,MACE,DAGGER,STAFF,BOW,ARROW,SHIELD,POLEARM,SLING,BULLET,
    LIGHT_ARMOR,HEAVY_ARMOR,HELM,GAUNTLET,LIGHT_ARMOR,HEAVY_ARMOR,SWORD,AXE,MACE,SHIELD,
    SCROLL,POTION,GEM,LANCE)
MYSTERIOUS_TYPES = (GEM,)
# These types are typically for resale only, so don't decrease gp of horde as much.
CASHSALE_TYPES = (GEM,)

def generate_special_item( item_rank, item_type=None ):
    """Generate an item of a particular type, magic if appropriate."""
    it = choose_item( max_rank=item_rank, item_type=item_type )
    if it and item_rank > it.min_rank():
        make_item_magic( it, item_rank )
        it.identified = False
    return it

# Test Magic Items
#for t in range( 100 ):
#    wep = choose_item( item_type = random.choice( WEAPON_TYPES + (CLOTHES,LIGHT_ARMOR,HEAVY_ARMOR,SHIELD) ), max_rank = 5 )
#    make_item_magic( wep, t % 10 + wep.min_rank() )
#    print "{}.{}: {}".format( t%10+3,wep,wep.desc() )


def generate_hoard( drop_rank, drop_strength, item_types=PREMIUM_TYPES ):
    """Returns a tuple containing gold, list of items."""
    # drop_rank is the rank of the level.
    # drop_strength is a percentile loot adjustment.

    # Start by determining actual size of hoard, in gp
    gp = max( ( drop_rank//2 + random.randint( 1, drop_rank + 1 ) ) * drop_strength + random.randint(1,100) - random.randint(1,100), random.randint(51,150) )
    hoard = list()

    tries = random.randint( 0 , 2 + ( drop_rank + 1 ) // 2 )
    while ( gp > 0 ) and ( tries > 0 ):
        i_rank = drop_rank
        if random.randint(1,20) == 17:
            # Generate an out-of-depth item.
            i_rank += random.randint(1,3)
            it = choose_item( item_type = random.choice( item_types ), max_rank = i_rank )
            tries -= 3
            if it:
                it.identified = False
        elif random.randint(1,3) != 1:
            it = choose_item( item_type = random.choice( item_types ), max_rank = drop_rank )
        else:
            it = choose_item( max_rank = drop_rank )
        if it:
            delta_rank = i_rank - it.min_rank()
            if random.randint(1,6) <= delta_rank:
                if tries > 1 and random.randint(1,6) == 2:
                    i_rank += 1
                    tries += -1
                make_item_magic( it, i_rank )
                it.identified = False
            elif random.randint(1,23) == 5:
                it.identified = False
            if it.itemtype in MYSTERIOUS_TYPES and random.randint(1,10) != 1:
                it.identified = False
            if hasattr( it, "quantity" ) and it.quantity == 1 and random.randint(1,3) != 2:
                it.quantity = random.randint(1,4)
            hoard.append( it )
            if it.itemtype not in CASHSALE_TYPES:
                gp -= max( it.cost()//2 , 1 )
            else:
                gp -= max( it.cost()//5 , 1 )
        tries -= 1

    return (max(gp,0),hoard)

class Backpack( container.ContainerList ):
    def get_equip( self , slot ):
        requested_item = None
        for i in self:
            if i.equipped and ( i.slot == slot ):
                requested_item = i
                break
        return requested_item
    def equip( self, item ):
        if ( item in self ) and ( item.slot != NOSLOT ):
            # Unequip the currently equipped item
            old_item = self.get_equip( item.slot )
            if old_item:
                old_item.equipped = False

            if (item.slot == HAND1) and item.attackdata.double_handed:
                # If dealing with a two handed weapon, unequip whatever's in hand 2.
                old_item = self.get_equip( HAND2 )
                if old_item:
                    old_item.equipped = False
            elif item.slot == HAND2:
                # Likewise, if equipping a hand2 item and hand1 has a two handed weapon,
                #  unequip the contents of hand1.
                old_item = self.get_equip( HAND1 )
                if old_item and old_item.attackdata.double_handed:
                    old_item.equipped = False
            item.equipped = True
    def unequip( self, item ):
        item.equipped = False

    def tidy( self ):
        # Merge any stackable items.
        mystackables = list()
        for i in self[:]:
            if hasattr(i,"can_stack_with"):
                self.remove( i )
                found_stack = False
                for ii in mystackables:
                    if i.can_stack_with( ii ):
                        ii.quantity += i.quantity
                        found_stack = True
                        break
                if not found_stack:
                    mystackables.append( i )
        if mystackables:
            self += mystackables



