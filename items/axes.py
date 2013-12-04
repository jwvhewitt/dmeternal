import stats
from . import Item,Attack,AXE

class Hatchet( Item ):
    true_name = "Hatchet"
    true_desc = "A small axe used for chopping wood."
    itemtype = AXE
    avatar_image = "avatar_axe.png"
    avatar_frame = 0
    mass = 20
    attackdata = Attack( (1,4,0) )

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
    avatar_frame = 2
    mass = 110
    attackdata = Attack( (1,8,0), double_handed = True )

class Greataxe( Item ):
    true_name = "Greataxe"
    true_desc = "This massive axe can only be weilded by the strongest fighters."
    itemtype = AXE
    avatar_image = "avatar_axe.png"
    avatar_frame = 3
    mass = 145
    attackdata = Attack( (1,10,0), double_handed = True )

class DwarvenWaraxe( Item ):
    true_name = "Dwarven Waraxe"
    true_desc = "The blade of this axe is nearly sharp enough to cut stone. It is used by dwarves in tunnel fighting."
    itemtype = AXE
    avatar_image = "avatar_axe.png"
    avatar_frame = 6
    mass = 85
    attackdata = Attack( (2,6,0) )

class OrcishBattleaxe( Item ):
    true_name = "Orcish Battleaxe"
    true_desc = "Though crudely made, the sheer weight of this weapon is enough to cause massive damage."
    itemtype = AXE
    avatar_image = "avatar_axe.png"
    avatar_frame = 7
    mass = 160
    attackdata = Attack( (1,12,0), double_handed = True )


class ExecutionersAxe( Item ):
    true_name = "Executioner's Axe"
    true_desc = "This axe is so sharp it has been known to decapitate opponents in a single blow."
    itemtype = AXE
    avatar_image = "avatar_axe.png"
    avatar_frame = 5
    mass = 150
    attackdata = Attack( (2,5,2), double_handed = True )
    statline = stats.StatMod({ stats.CRITICAL_HIT: 5 })


class Pickaxe( Item ):
    true_name = "Pickaxe"
    true_desc = "Generally used for mining, this tool can also be used as a weapon."
    itemtype = AXE
    avatar_image = "avatar_axe.png"
    avatar_frame = 8
    mass = 60
    attackdata = Attack( (1,6,1) )


