import stats
import image
import inspect

# Enumerated constants for the item slots.
# Note that these are defined in the order in which they're applied to avatar.
NOSLOT, BACK, FEET, BODY, HANDS, HAND2, HAND1, HEAD = range( 100, 108 )

class SingType( object ):
    # A singleton itemtype class; use these objects as tokens to indicate
    # the type of items.
    # Also includes misc information related to the itemtype in question.
    def __init__( self, ident, name, slot = NOSLOT ):
        # ident should be the module-level name of this object.
        self.ident = ident
        self.name = name
        self.slot = slot
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
SHIELD = SingType( "SHIELD", "Shield", slot = HAND2 )
SLING = SingType( "SLING", "Sling", slot = HAND1 )
BULLET = SingType( "BULLET", "Bullet", slot = HAND2 )
CLOTHES = SingType( "CLOTHES", "Clothes", slot = BODY )
LIGHT_ARMOR = SingType( "LIGHT_ARMOR", "Light Armor", slot = BODY )
HEAVY_ARMOR = SingType( "HEAVY_ARMOR", "Heavy Armor", slot = BODY )
HAT = SingType( "HAT", "Hat", slot = HEAD )
HELM = SingType( "HELM", "Helm", slot = HEAD )
GLOVE = SingType( "GLOVE", "Gloves", slot = HANDS )
GAUNTLET = SingType( "GAUNTLET", "Gauntlets", slot = HANDS )
SANDALS = SingType( "SANDALS", "Sandals", slot = FEET )
SHOES = SingType( "SHOES", "Shoes", slot = FEET )
BOOTS = SingType( "BOOTS", "Boots", slot = FEET )
CLOAK = SingType( "CLOAK", "Cloak", slot = BACK )
HOLYSYMBOL = SingType( "HOLYSYMBOL", "Symbol", slot = HAND2 )

class Attack( object ):
    REACH_MODIFIER = 2
    def __init__( self, damage = (1,6,0), skill_mod = stats.STRENGTH, damage_mod = stats.STRENGTH, \
         double_handed = False, element = stats.RESIST_SLASHING, reach = 1 ):
        self.damage = damage
        self.skill_mod = skill_mod
        self.damage_mod = damage_mod
        self.double_handed = double_handed
        self.element = element
        self.reach = reach
    def cost( self ):
        """Return the GP value of this attack."""
        # Calculate the maximum damage that can be rolled.
        D = self.damage[0] * self.damage[1] + self.damage[2]
        # Base price is this amount squared, plus number of dice squared.
        it = D ** 2 + self.damage[0] ** 2
        # Modify for range; each point increases cost by a third.
        if self.reach > 1:
            it = ( it * self.reach + 3 ) * self.REACH_MODIFIER // 6
        return it
    def stat_desc( self ):
        """Return a string describing this attack."""
        it = "{0}d{1}{2:+} {3} damage".format(self.damage[0],self.damage[1],self.damage[2], self.element.element_name )
        if self.double_handed:
            it = "2H " + it
        if self.reach > 1:
            it = it + ", Range:{0}".format( self.reach )
        return it

class Item( object ):
    true_name = "Item"
    true_desc = ""
    statline = stats.StatMod()
    itemtype = GENERIC
    identified = False
    attackdata = None
    quantity = 0
    avatar_image = None
    avatar_frame = 0
    mass = 1
    equipped = False
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
    def __cmp__( self, other ):
        """Item comparisons based on monetary value."""
        if not other:
            return 1
        else:
            return self.cost() - other.cost()
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

    @property
    def slot( self ):
        return self.itemtype.slot

class NormalCloak( Item ):
    true_name = "Cloak"
    true_desc = "A warm grey cloak."
    itemtype = CLOAK
    avatar_image = "avatar_cloak.png"
    avatar_frame = 0
    mass = 10
    statline = stats.StatMod({ stats.RESIST_COLD: 5 })

class ThiefCloak( NormalCloak ):
    true_name = "Thief Cloak"
    true_desc = "A dark cloak to help you hide in shadows."
    avatar_frame = 4
    statline = stats.StatMod({ stats.STEALTH: 5, stats.RESIST_COLD: 5 })

class NormalClothes( Item ):
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

class PeasantGarb( NormalClothes ):
    true_name = "Peasant Garb"
    true_desc = ""
    avatar_frame = 0
    pants_frame = 8
    male_pants = 18
    mass = 20

class MerchantGarb( NormalClothes ):
    true_name = "Merchant Garb"
    true_desc = ""
    avatar_frame = 2
    male_frame = 1
    pants_frame = 6
    mass = 20

class MageRobe( NormalClothes ):
    true_name = "Mage Robe"
    true_desc = ""
    avatar_frame = 12
    male_frame = 4
    pants_image = None
    mass = 20

class DruidRobe( NormalClothes ):
    true_name = "Druid Robe"
    true_desc = ""
    avatar_frame = 5
    male_frame = 6
    pants_image = None
    mass = 20

class NecromancerRobe( NormalClothes ):
    true_name = "Necromancer Robe"
    true_desc = ""
    avatar_frame = 13
    male_frame = 7
    pants_image = None
    mass = 20

class MonkRobe( NormalClothes ):
    true_name = "Monk Robe"
    true_desc = ""
    avatar_frame = 8
    pants_image = None
    mass = 20

class NinjaGear( NormalClothes ):
    true_name = "Ninja Garb"
    true_desc = ""
    avatar_frame = 9
    pants_frame = 3
    mass = 20

class AnimalSkin( NormalClothes ):
    true_name = "Animal Skin"
    true_desc = ""
    avatar_frame = 10
    pants_image = None
    mass = 50

class LeatherJacket( NormalClothes ):
    true_name = "Leather Jacket"
    true_desc = ""
    avatar_frame = 11
    pants_frame = 3
    mass = 25


class LeatherArmor( NormalClothes ):
    true_name = "Leather Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 1
    pants_frame = 5
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 90

class GladiatorArmor( NormalClothes ):
    true_name = "Gladiator Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 4
    male_frame = 3
    pants_frame = 2
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 86

class RangerArmor( NormalClothes ):
    true_name = "Ranger Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 5
    pants_frame = 6
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 90

class PaddedArmor( NormalClothes ):
    true_name = "Padded Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 6
    pants_frame = 3
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 80

class BrigandineArmor( NormalClothes ):
    true_name = "Brigandine Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 7
    pants_frame = 6
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 95

class LeatherCuirass( NormalClothes ):
    true_name = "Leather Cuirass"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 8
    pants_frame = 5
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 100

class PaddedRobe( NormalClothes ):
    true_name = "Padded Robe"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 9
    pants_sprite = None
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 85

class HideArmor( NormalClothes ):
    true_name = "Hide Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 0
    pants_frame = 5
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 15 })
    mass = 95


class ChainmailArmor( NormalClothes ):
    true_name = "Chainmail Armor"
    true_desc = ""
    itemtype = HEAVY_ARMOR
    avatar_image = "avatar_cloak.png"
    avatar_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 20, stats.MAGIC_ATTACK: -20, stats.STEALTH: -10 })
    mass = 250

class Shortsword( Item ):
    true_name = "Shortsword"
    true_desc = ""
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 0
    mass = 15
    attackdata = Attack( (1,6,0) )

class Rapier( Item ):
    true_name = "Rapier"
    true_desc = ""
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 28
    mass = 12
    attackdata = Attack( (1,6,0), element = stats.RESIST_PIERCING )

class Longsword( Item ):
    true_name = "Longsword"
    true_desc = ""
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 1
    mass = 40
    attackdata = Attack( (1,8,0) )

class Broadsword( Longsword ):
    true_name = "Broadsword"
    true_desc = ""
    avatar_frame = 2
    mass = 45

class Wakizashi( Longsword ):
    true_name = "Wakizashi"
    true_desc = ""
    avatar_frame = 18
    mass = 35

class HandAxe( Item ):
    true_name = "Hand Axe"
    true_desc = ""
    itemtype = AXE
    avatar_image = "avatar_axe.png"
    avatar_frame = 1
    mass = 50
    attackdata = Attack( (1,6,0) )

class WarAxe( Item ):
    true_name = "War Axe"
    true_desc = "A sturdy single-handed axe."
    itemtype = AXE
    avatar_image = "avatar_axe.png"
    avatar_frame = 4
    mass = 70
    attackdata = Attack( (1,8,0) )

class BattleAxe( Item ):
    true_name = "Battle Axe"
    true_desc = "A sturdy double-handed axe."
    itemtype = AXE
    avatar_image = "avatar_axe.png"
    avatar_frame = 7
    mass = 110
    attackdata = Attack( (1,8,0), double_handed = True )

class Pickaxe( Item ):
    true_name = "Pickaxe"
    true_desc = "Generally used for mining, this tool can also be used as a weapon."
    itemtype = AXE
    avatar_image = "avatar_axe.png"
    avatar_frame = 8
    mass = 60
    attackdata = Attack( (1,6,1) )

class FlangedMace( Item ):
    true_name = "Flanged Mace"
    true_desc = ""
    itemtype = MACE
    avatar_image = "avatar_mace.png"
    avatar_frame = 8
    mass = 40
    attackdata = Attack( (1,6,0), element = stats.RESIST_CRUSHING )

class Club( Item ):
    true_name = "Club"
    true_desc = "A big piece of wood."
    itemtype = MACE
    avatar_image = "avatar_mace.png"
    avatar_frame = 0
    mass = 30
    attackdata = Attack( (1,6,0), element = stats.RESIST_CRUSHING )

class Warhammer( Item ):
    true_name = "Warhammer"
    true_desc = ""
    itemtype = MACE
    avatar_image = "avatar_mace.png"
    avatar_frame = 7
    mass = 80
    attackdata = Attack( (1,8,0), element = stats.RESIST_CRUSHING )

class Morningstar( Item ):
    true_name = "Morningstar"
    true_desc = ""
    itemtype = MACE
    avatar_image = "avatar_mace.png"
    avatar_frame = 12
    mass = 70
    attackdata = Attack( (1,8,0), element = stats.RESIST_CRUSHING )


class Dagger( Item ):
    true_name = "Dagger"
    true_desc = ""
    itemtype = DAGGER
    avatar_image = "avatar_dagger.png"
    avatar_frame = 0
    mass = 12
    attackdata = Attack( (1,4,0), element = stats.RESIST_PIERCING )

class Sickle( Dagger ):
    true_name = "Sickle"
    true_desc = ""
    avatar_frame = 4
    mass = 15
    attackdata = Attack( (1,6,0) )

class Quarterstaff( Item ):
    true_name = "Quarterstaff"
    true_desc = ""
    itemtype = STAFF
    avatar_image = "avatar_staff.png"
    avatar_frame = 0
    attackdata = Attack( (1,4,0), double_handed = True, element = stats.RESIST_CRUSHING )
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })
    mass = 20

class Spear( Item ):
    true_name = "Spear"
    true_desc = ""
    itemtype = POLEARM
    avatar_image = "avatar_polearm.png"
    avatar_frame = 0
    attackdata = Attack( (1,8,0), double_handed = True, element = stats.RESIST_PIERCING )
    mass = 90


class MageHat( Item ):
    true_name = "Mage Hat"
    true_desc = ""
    itemtype = HAT
    avatar_image = "avatar_hat.png"
    avatar_frame = 0
    mass = 6

class NecromancerHat( MageHat ):
    true_name = "Necromancer Hat"
    true_desc = ""
    avatar_frame = 1

class NinjaMask( Item ):
    true_name = "Ninja Mask"
    true_desc = ""
    itemtype = HAT
    avatar_image = "avatar_hat.png"
    avatar_frame = 2
    mass = 1

class Headband( NinjaMask ):
    true_name = "Headband"
    true_desc = ""
    avatar_frame = 3

class Bandana( NinjaMask ):
    true_name = "Bandana"
    true_desc = ""
    avatar_frame = 4

class JauntyHat( MageHat ):
    true_name = "Jaunty Hat"
    true_desc = ""
    avatar_frame = 5

class WoodsmansHat( MageHat ):
    true_name = "Woodsman's Hat"
    true_desc = ""
    avatar_frame = 6

class GnomeHat( MageHat ):
    true_name = "Pointy Hat"
    true_desc = "What all the fashionable gnomes are wearing this year."
    avatar_frame = 7


class NormalShoes( Item ):
    true_name = "Shoes"
    true_desc = "Sturdy leather shoes."
    itemtype = SHOES
    avatar_image = "avatar_boot.png"
    avatar_frame = 2
    mass = 4

class NormalBoots( NormalShoes ):
    true_name = "Boots"
    true_desc = "Sturdy leather boots."
    itemtype = BOOTS
    avatar_frame = 8
    mass = 7

class NormalSandals( NormalShoes ):
    true_name = "Sandals"
    true_desc = "Plain sandals."
    itemtype = SANDALS
    avatar_frame = 16
    mass = 3

class WoodSymbol( Item ):
    true_name = "Wooden Holy Symbol"
    true_desc = ""
    itemtype = HOLYSYMBOL
    avatar_image = "avatar_tool.png"
    avatar_frame = 0
    statline = stats.StatMod({ stats.HOLY_SIGN: 5 })
    mass = 7

class SilverSymbol( Item ):
    true_name = "Silver Holy Symbol"
    true_desc = ""
    itemtype = HOLYSYMBOL
    avatar_image = "avatar_tool.png"
    avatar_frame = 3
    statline = stats.StatMod({ stats.HOLY_SIGN: 10, stats.MAGIC_ATTACK: 5, stats.RESIST_LUNAR: 10 })
    mass = 14

class GoldSymbol( Item ):
    true_name = "Gold Holy Symbol"
    true_desc = ""
    itemtype = HOLYSYMBOL
    avatar_image = "avatar_tool.png"
    avatar_frame = 4
    statline = stats.StatMod({ stats.HOLY_SIGN: 15, stats.MAGIC_ATTACK: 10, stats.MAGIC_DEFENSE: 10, stats.RESIST_LUNAR: 25 })
    mass = 21

# Compile the items into a useful list.
ITEM_LIST = []
g = globals()
for name in dir():
    o = g[ name ]
    if inspect.isclass( o ) and issubclass( o , Item ) and o is not Item:
        ITEM_LIST.append( o )


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



if __name__ == '__main__':
    ws = HandAxe()
    ss = Pickaxe()
    gs = WarAxe()

    print ws.cost()
    print ss.cost()
    print gs.cost()

    print hasattr( ws, "statline" )



