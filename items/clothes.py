import stats
from . import Clothing,CLOTHES

class NormalClothes( Clothing ):
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

class PeasantGarb( Clothing ):
    true_name = "Peasant Garb"
    true_desc = ""
    avatar_frame = 0
    pants_frame = 8
    male_pants = 18
    mass = 20

class MerchantGarb( Clothing ):
    true_name = "Merchant Garb"
    true_desc = ""
    avatar_frame = 2
    male_frame = 1
    pants_frame = 6
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.RESIST_PIERCING: 5 })
    mass = 20

class MageRobe( Clothing ):
    true_name = "Mage Robe"
    true_desc = ""
    avatar_frame = 12
    male_frame = 4
    pants_image = None
    mass = 20

class DruidRobe( Clothing ):
    true_name = "Druid Robe"
    true_desc = ""
    avatar_frame = 5
    male_frame = 6
    pants_image = None
    mass = 20

class NecromancerRobe( Clothing ):
    true_name = "Necromancer Robe"
    true_desc = ""
    avatar_frame = 13
    male_frame = 7
    pants_image = None
    mass = 20

class MonkRobe( Clothing ):
    true_name = "Monk Robe"
    true_desc = ""
    avatar_frame = 8
    pants_image = None
    mass = 20

class NinjaGear( Clothing ):
    true_name = "Ninja Garb"
    true_desc = ""
    avatar_frame = 9
    pants_frame = 3
    mass = 20

class AnimalSkin( Clothing ):
    true_name = "Animal Skin"
    true_desc = ""
    avatar_frame = 10
    pants_image = None
    mass = 50

class LeatherJacket( Clothing ):
    true_name = "Leather Jacket"
    true_desc = ""
    avatar_frame = 11
    pants_frame = 3
    mass = 25

