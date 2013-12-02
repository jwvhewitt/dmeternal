import stats
from . import Item,Attack,SWORD


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

class BastardSword( Item ):
    true_name = "Bastard Sword"
    true_desc = ""
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 7
    mass = 55
    attackdata = Attack( (1,10,0) )

class Katana( Item ):
    true_name = "Katana"
    true_desc = ""
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 4
    mass = 45
    attackdata = Attack( (1,10,0) )



