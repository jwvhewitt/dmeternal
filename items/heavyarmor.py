import stats
from . import Clothing,HEAVY_ARMOR

class ChainmailArmor( Clothing ):
    true_name = "Chainmail Armor"
    true_desc = ""
    itemtype = HEAVY_ARMOR
    avatar_image = "avatar_heavyarmor.png"
    avatar_frame = 0
    pants_frame = 1
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 20, stats.MAGIC_ATTACK: -20, stats.STEALTH: -10 })
    mass = 250

class BandedMail( Clothing ):
    true_name = "Banded Mail"
    true_desc = ""
    itemtype = HEAVY_ARMOR
    avatar_image = "avatar_heavyarmor.png"
    avatar_frame = 1
    pants_frame = 10
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 25, stats.MAGIC_ATTACK: -20, stats.STEALTH: -10 })
    mass = 345

class FieldPlate( Clothing ):
    true_name = "Field Plate Armor"
    true_desc = ""
    itemtype = HEAVY_ARMOR
    avatar_image = "avatar_heavyarmor.png"
    avatar_frame = 11
    pants_frame = 16
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 30, stats.MAGIC_ATTACK: -25, stats.STEALTH: -15 })
    mass = 370

class FullPlate( Clothing ):
    true_name = "Full Plate Armor"
    true_desc = ""
    itemtype = HEAVY_ARMOR
    avatar_image = "avatar_heavyarmor.png"
    avatar_frame = 10
    pants_frame = 16
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 35, stats.MAGIC_ATTACK: -30, stats.STEALTH: -15 })
    mass = 400

class ElvenPlate( Clothing ):
    true_name = "Elven Plate Armor"
    true_desc = ""
    itemtype = HEAVY_ARMOR
    avatar_image = "avatar_heavyarmor.png"
    avatar_frame = 17
    pants_frame = 11
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 35, stats.MAGIC_DEFENSE: 10, stats.STEALTH: -10 })
    mass = 295

