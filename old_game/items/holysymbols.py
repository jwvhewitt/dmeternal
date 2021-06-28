from .. import stats
from . import Item,Attack,HOLYSYMBOL

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


