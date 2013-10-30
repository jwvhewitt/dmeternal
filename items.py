import stats
import image
import characters

# Enumerated constants for the item types.
GENERIC, SWORD, AXE, MACE, DAGGER, STAFF, BOW, POLEARM, ARROW, SHIELD, SLING, \
    BULLET, CLOTHES, LIGHT_ARMOR, HEAVY_ARMOR, HAT, HELM, GLOVE, GAUNTLET, \
    SANDALS, SHOES, BOOTS, CLOAK = range( 23 )

# Enumerated constants for the item slots.
# Note that these are defined in the order in which they're applied to avatar.
NOSLOT, BACK, FEET, BODY, HANDS, HAND1, HAND2, HEAD = range( 100, 108 )

# List of slots by item type.
SLOT_FOR_TYPE = ( NOSLOT, HAND1, HAND1, HAND1, HAND1, \
    HAND1, HAND1, HAND1, HAND2, HAND2, HAND1, \
    HAND2, BODY, BODY, BODY, HEAD, HEAD, HANDS, HANDS, FEET, FEET, \
    FEET, BACK )

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
    double_handed = False
    equipped = False
    def cost( self ):
        it = 1
        if self.statline != None:
            it += self.statline.cost()
        return it
    def stamp_avatar( self, avatar, pc ):
        """Apply this item's sprite to the avatar."""
        if self.avatar_image:
            img = image.Image( self.avatar_image , 54 , 54 )
            img.render( avatar.bitmap , frame = self.avatar_frame )

    @property
    def slot( self ):
        return SLOT_FOR_TYPE[ self.itemtype ]

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
        if self.pants_image:
            img = image.Image( self.pants_image , 54 , 54 )
            if ( pc.gender == characters.MALE ) and self.male_pants:
                frame = self.male_pants
            else:
                frame = self.pants_frame
            img.render( avatar.bitmap , frame = frame )
        if self.avatar_image:
            img = image.Image( self.avatar_image , 54 , 54 )
            if ( pc.gender == characters.MALE ) and self.male_frame:
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
    avatar_frame = 4
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
    avatar_frame = 7
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
    pants_image = None
    mass = 20

class LeatherArmor( NormalClothes ):
    true_name = "Leather Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 1
    pants_frame = 5
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 90

class ChainmailArmor( Item ):
    true_name = "Chainmail Armor"
    true_desc = ""
    itemtype = HEAVY_ARMOR
    avatar_image = "avatar_cloak.png"
    avatar_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 20, stats.MAGIC_ATTACK: -20, stats.STEALTH: -10 })
    mass = 250

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

            if (item.slot == HAND1) and item.double_handed:
                # If dealing with a two handed weapon, unequip whatever's in hand 2.
                old_item = self.get_equip( HAND2 )
                if old_item:
                    old_item.equipped = False
            elif item.slot == HAND2:
                # Likewise, if equipping a hand2 item and hand1 has a two handed weapon,
                #  unequip the contents of hand1.
                old_item = self.get_equip( HAND1 )
                if old_item and old_item.double_handed:
                    old_item.equipped = False
            item.equipped = True

if __name__ == '__main__':
    tc = ThiefCloak()
    nc = NormalCloak()
    la = LeatherArmor()
    ca = ChainmailArmor()

    print tc.cost()
    print nc.cost()
    print la.cost()
    print ca.cost()


