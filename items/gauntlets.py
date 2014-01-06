import stats
from . import Item,Attack,GAUNTLET

class BlackGauntlets( Item ):
    true_name = "Black Gauntlets"
    true_desc = ""
    itemtype = GAUNTLET
    avatar_image = "avatar_arm.png"
    avatar_frame = 0
    mass = 10
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.MAGIC_ATTACK: -5 })

class SteelGauntlets( Item ):
    true_name = "Steel Gauntlets"
    true_desc = ""
    itemtype = GAUNTLET
    avatar_image = "avatar_arm.png"
    avatar_frame = 5
    mass = 10
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.MAGIC_ATTACK: -5 })

