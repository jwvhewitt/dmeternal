import stats
import image
import inspect
import effects
import animobs
import random

# Enumerated constants for the item slots.
# Note that these are defined in the order in which they're applied to avatar.
NOSLOT, BACK, FEET, BODY, HANDS, HAND2, HAND1, HEAD = range( 100, 108 )

class SingType( object ):
    # A singleton itemtype class; use these objects as tokens to indicate
    # the type of items.
    # Also includes misc information related to the itemtype in question.
    def __init__( self, ident, name, slot = NOSLOT, gp_per_level=50 ):
        # ident should be the module-level name of this object.
        self.ident = ident
        self.name = name
        self.slot = slot
        self.gp_per_level = gp_per_level
    def __str__( self ):
        return self.name
    def __reduce__( self ):
        return self.ident

GENERIC = SingType( "GENERIC", "Item" )
SWORD = SingType( "SWORD", "Sword", slot = HAND1 )
AXE = SingType( "AXE", "Axe", slot = HAND1 )
MACE = SingType( "MACE", "Mace", slot = HAND1 )
DAGGER = SingType( "DAGGER", "Dagger", slot = HAND1 )
STAFF = SingType( "STAFF", "Staff", slot = HAND1 )
BOW = SingType( "BOW", "Bow", slot = HAND1 )
POLEARM = SingType( "POLEARM", "Polearm", slot = HAND1 )
ARROW = SingType( "ARROW", "Arrow", slot = HAND2 )
SHIELD = SingType( "SHIELD", "Shield", slot = HAND2, gp_per_level=85 )
SLING = SingType( "SLING", "Sling", slot = HAND1 )
BULLET = SingType( "BULLET", "Bullet", slot = HAND2 )
CLOTHES = SingType( "CLOTHES", "Clothes", slot = BODY, gp_per_level=65 )
LIGHT_ARMOR = SingType( "LIGHT_ARMOR", "Light Armor", slot = BODY, gp_per_level=90 )
HEAVY_ARMOR = SingType( "HEAVY_ARMOR", "Heavy Armor", slot = BODY, gp_per_level=125 )
HAT = SingType( "HAT", "Hat", slot = HEAD, gp_per_level=20 )
HELM = SingType( "HELM", "Helm", slot = HEAD, gp_per_level=30 )
GLOVE = SingType( "GLOVE", "Gloves", slot = HANDS, gp_per_level=20 )
GAUNTLET = SingType( "GAUNTLET", "Gauntlets", slot = HANDS, gp_per_level=30 )
SANDALS = SingType( "SANDALS", "Sandals", slot = FEET, gp_per_level=20 )
SHOES = SingType( "SHOES", "Shoes", slot = FEET, gp_per_level=20 )
BOOTS = SingType( "BOOTS", "Boots", slot = FEET, gp_per_level=20 )
CLOAK = SingType( "CLOAK", "Cloak", slot = BACK, gp_per_level=30 )
HOLYSYMBOL = SingType( "HOLYSYMBOL", "Symbol", slot = HAND2, gp_per_level=75 )
WAND = SingType( "WAND", "Wand", slot = HAND1 )
FARMTOOL = SingType( "FARMTOOL", "Farm Tool", slot = HAND1 )

class Attack( object ):
    def __init__( self, damage = (1,6,0), skill_mod = stats.STRENGTH, damage_mod = stats.STRENGTH, \
         double_handed = False, element = stats.RESIST_SLASHING, reach = 1, hit_anim=animobs.RedBoom ):
        self.damage = damage
        self.skill_mod = skill_mod
        self.damage_mod = damage_mod
        self.double_handed = double_handed
        self.element = element
        self.reach = reach
        self.hit_anim = hit_anim
    def cost( self ):
        """Return the GP value of this attack."""
        # Calculate the maximum damage that can be rolled.
        D = self.damage[0] * self.damage[1] + self.damage[2]
        # Base price is this amount squared, plus number of dice squared.
        it = D ** 2 + self.damage[0] ** 2
        # Modify for range; each point increases cost by a third.
        if self.reach > 1:
            it = it * ( self.reach + 2 ) // 3
        # If weapon performance unaffected by stats, make it cheaper.
        if not self.skill_mod:
            it = ( it * 4 ) // 5
        if not self.damage_mod:
            it = ( it * 4 ) // 5
        # Multiply by element cost.
        it *= self.element.element_cost_mod
        return it
    def stat_desc( self ):
        """Return a string describing this attack."""
        it = "{0}d{1}{2:+} {3} damage".format(self.damage[0],self.damage[1],self.damage[2], self.element.element_name )
        if self.double_handed:
            it = "2H " + it
        if self.reach > 1:
            it = it + ", Range:{0}".format( self.reach )
        return it
    def get_effect( self, user, att_modifier=0, target=None ):
        """Generate an effect tree for this attack."""
        hit = effects.HealthDamage( att_dice=self.damage, stat_bonus=self.damage_mod, element=self.element, anim=self.hit_anim )
        if self.double_handed:
            hit.stat_mod = 1.5
        miss = effects.NoEffect( anim=animobs.SmallBoom )
        roll = effects.PhysicalAttackRoll( att_stat=self.skill_mod, att_modifier=att_modifier, on_success=[hit,], on_failure=[miss,] )

        # If the attacker has critical hit skill, use it.
        if user.get_stat( stats.CRITICAL_HIT ) > 0:
            hit.on_success.append( user.critical_hit_effect( att_modifier ) )

        # Add any enchantment bonuses.
        for e in user.condition:
            user.add_attack_enhancements( roll, e )

        return roll

class Item( object ):
    true_name = "Item"
    true_desc = ""
    statline = stats.StatMod()
    itemtype = GENERIC
    identified = False
    attackdata = None
    avatar_image = None
    avatar_frame = 0
    mass = 1
    equipped = False
    shot_anim=None
    def cost( self ):
        it = 1
        if self.statline != None:
            it += self.statline.cost()
        if self.attackdata != None:
            it += self.attackdata.cost()
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
    def __str__( self ):
        return self.true_name

    def stat_desc( self ):
        """Return descriptions of all stat modifiers provided."""
        smod = []
        if self.attackdata:
            smod.append( self.attackdata.stat_desc() )
        for k,v in self.statline.iteritems():
            smod.append( str(k) + ":" + "{0:+}".format( v ) )
        return ", ".join( smod )

    def can_attack( self, user ):
        """Return True if this weapon can be used to attack right now."""
        return True
    def spend_attack_price( self, user ):
        """Spend this weapon's attack price."""
        pass
    def min_rank( self ):
        return min( max( self.cost() // self.itemtype.gp_per_level , 1 ), 20 )

    @property
    def slot( self ):
        return self.itemtype.slot

class MissileWeapon( Item ):
    AMMOTYPE = ARROW
    def cost( self ):
        it = 1
        if self.statline != None:
            it += self.statline.cost()
        if self.attackdata != None:
            # Missile weapons only pay half normal cost for attackdata.
            it += self.attackdata.cost() // 2
        return it
    def can_attack( self, user ):
        """Return True if this weapon can be used to attack right now."""
        h2 = user.inventory.get_equip( HAND2 )
        return h2 and h2.itemtype == self.AMMOTYPE
    def spend_attack_price( self, user ):
        """Spend this weapon's attack price."""
        h2 = user.inventory.get_equip( HAND2 )
        h2.quantity += -1
        if h2.quantity < 1:
            user.inventory.remove( h2 )

class Ammo( Item ):
    quantity = 20
    mass_per_shot = 1
    itemtype = ARROW
    cost_per_shot = 1

    def cost( self ):
        it = self.cost_per_shot * self.quantity
        if self.statline != None:
            it += self.statline.cost()
        if self.attackdata != None:
            it += self.attackdata.cost()
        return it

    def __str__( self ):
        return "{0} [{1}]".format( self.true_name, self.quantity )

    @property
    def mass( self ):
        return self.quantity * self.mass_per_shot

class ManaWeapon( Item ):
    MP_COST = 1
    def cost( self ):
        it = 1
        if self.statline != None:
            it += self.statline.cost()
        if self.attackdata != None:
            # Mana weapons only pay 3/4 normal cost for attackdata.
            it += ( self.attackdata.cost() * 3 ) // 4
        return it
    def stat_desc( self ):
        """Return descriptions of all stat modifiers provided."""
        smod = []
        if self.attackdata:
            smod.append( self.attackdata.stat_desc() )
            if self.MP_COST:
                smod.append( "{0} MP".format( self.MP_COST ) )
        for k,v in self.statline.iteritems():
            smod.append( "{0}:{1:+}".format( str(k) , v ) )
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


import axes
import bows
import cloaks
import clothes
import daggers
import farmtools
import gauntlets
import gloves
import hats
import heavyarmor
import helms
import holysymbols
import lightarmor
import maces
import polearms
import shields
import shoes
import slings
import staves
import swords
import wands

# Compile the items into a useful list.
ITEM_LIST = []
def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if inspect.isclass( o ) and issubclass( o , Item ) and o not in (Item, MissileWeapon, Ammo, ManaWeapon, Clothing):
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
harvest( lightarmor )
harvest( maces )
harvest( polearms )
harvest( shields )
harvest( shoes )
harvest( slings )
harvest( staves )
harvest( swords )
harvest( wands )

def choose_item( item_type=None, max_rank=20 ):
    """Return an item of the specified type, of at most max_rank."""
    candidates = []
    for ic in ITEM_LIST:
        i = ic()
        if i.min_rank() <= max_rank and ( i.itemtype == item_type or not item_type ):
            candidates += [i,] * i.min_rank()
    if candidates:
        return random.choice( candidates )


class Backpack( list ):
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




