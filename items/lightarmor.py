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
    avatar_frame = 9
    pants_sprite = None
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 85

class HideArmor( Clothing ):
    true_name = "Hide Armor"
    true_desc = ""
    itemtype = LIGHT_ARMOR
    avatar_image = "avatar_lightarmor.png"
    avatar_frame = 0
    pants_frame = 5
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 15 })
    mass = 95


