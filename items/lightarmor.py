import stats
from . import Clothing,LIGHT_ARMOR

class LeatherArmor( Clothing ):
    true_name = "Leather Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 1
    pants_frame = 5
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 90

class GladiatorArmor( Clothing ):
    true_name = "Gladiator Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 4
    male_frame = 3
    pants_frame = 2
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 86

class RangerArmor( Clothing ):
    true_name = "Ranger Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 5
    pants_frame = 6
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 90

class PaddedArmor( Clothing ):
    true_name = "Padded Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 6
    pants_frame = 3
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 80

class BrigandineArmor( Clothing ):
    true_name = "Brigandine Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 7
    pants_frame = 6
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 95

class LeatherCuirass( Clothing ):
    true_name = "Leather Cuirass"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 8
    pants_frame = 5
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 100

class PaddedRobe( Clothing ):
    true_name = "Padded Robe"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 22
    male_frame = 21
    pants_image = "avatar_robebottom.png"
    pants_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 85

class BeastfurArmor( Clothing ):
    true_name = "Beastfur Armor"
    true_desc = "Constructed from the skin of an unknown creature, this armor provides good physical and magical defense."
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 24
    pants_image = None
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.MAGIC_DEFENSE: 5 })
    mass = 95

class HideArmor( Clothing ):
    true_name = "Hide Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 0
    pants_frame = 5
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 15, stats.STEALTH: -15 })
    mass = 105

class StuddedLeather( Clothing ):
    true_name = "Studded Leather Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 11
    pants_frame = 5
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 15 })
    mass = 115

class LaminatedArmor( Clothing ):
    true_name = "Laminated Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 2
    pants_frame = 3
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 15, stats.STEALTH: -5 })
    mass = 120

class ChainShirt( Clothing ):
    true_name = "Chain Shirt"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 13
    pants_frame = 4
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 15, stats.MAGIC_ATTACK: -5 })
    mass = 75

class RingMail( Clothing ):
    true_name = "Ringmail Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 23
    pants_frame = 1
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 15, stats.MAGIC_ATTACK: -15, stats.STEALTH: -10 })
    mass = 125

class WyvernskinArmor( Clothing ):
    true_name = "Wyvernskin Armor"
    true_desc = "Made only in the barbarious northlands, this armor is highly valued because of its magical properties."
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 41
    pants_image = None
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 15, stats.MAGIC_DEFENSE: 5, stats.RESIST_POISON: 10 })
    mass = 90


class ScaleMail( Clothing ):
    true_name = "Scale Mail"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 12
    pants_frame = 14
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 20, stats.MAGIC_ATTACK:-5, stats.STEALTH:-10 })
    mass = 135

class Breastplate( Clothing ):
    true_name = "Breastplate"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 14
    pants_frame = 24
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 20, stats.MAGIC_ATTACK:-10, stats.STEALTH:-5 })
    mass = 140

class LamellarArmor( Clothing ):
    true_name = "Lamellar Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 24
    pants_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 20, stats.STEALTH:-15 })
    mass = 150

class ElvenChain( Clothing ):
    true_name = "Elven Chainmail"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 10
    pants_frame = 13
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 20, stats.MAGIC_DEFENSE:10 })
    mass = 125




