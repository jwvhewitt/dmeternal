import stats
from . import Item,Attack,POLEARM

class Pitchfork( Item ):
    true_name = "Pitchfork"
    true_desc = "A farm tool that can also be used as a weapon."
    itemtype = POLEARM
    avatar_image = "avatar_polearm.png"
    avatar_frame = 10
    attackdata = Attack( (1,6,0), element = stats.RESIST_PIERCING )
    mass = 65

class Spear( Item ):
    true_name = "Spear"
    true_desc = ""
    itemtype = POLEARM
    avatar_image = "avatar_polearm.png"
    avatar_frame = 0
    attackdata = Attack( (1,8,0), element = stats.RESIST_PIERCING )
    mass = 90

class Poleax( Item ):
    true_name = "Poleax"
    true_desc = ""
    itemtype = POLEARM
    avatar_image = "avatar_polearm.png"
    avatar_frame = 3
    attackdata = Attack( (1,8,0), double_handed=True, element = stats.RESIST_SLASHING )
    mass = 90

class Trident( Item ):
    true_name = "Trident"
    true_desc = ""
    itemtype = POLEARM
    avatar_image = "avatar_polearm.png"
    avatar_frame = 18
    attackdata = Attack( (1,10,0), element = stats.RESIST_PIERCING )
    mass = 95

class Pike( Item ):
    true_name = "Pike"
    true_desc = ""
    itemtype = POLEARM
    avatar_image = "avatar_polearm.png"
    avatar_frame = 11
    attackdata = Attack( (1,10,0), double_handed=True, element=stats.RESIST_PIERCING, reach=2 )
    mass = 110

class Halbard( Item ):
    true_name = "Halbard"
    true_desc = ""
    itemtype = POLEARM
    avatar_image = "avatar_polearm.png"
    avatar_frame = 1
    attackdata = Attack( (2,6,0), double_handed = True, element = stats.RESIST_SLASHING, reach=2 )
    mass = 140


