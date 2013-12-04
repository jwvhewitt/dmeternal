import stats
from . import Item,Attack,SWORD


class Shortsword( Item ):
    true_name = "Shortsword"
    true_desc = "This light sword favors reflexes over brute strength."
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 0
    mass = 15
    attackdata = Attack( (1,6,0), skill_mod=stats.REFLEXES )

class Rapier( Item ):
    true_name = "Rapier"
    true_desc = "This light, flexible sword relies on reflexes rather than brute strength."
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 28
    mass = 12
    attackdata = Attack( (1,8,0), element = stats.RESIST_PIERCING, skill_mod=stats.REFLEXES )

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
    mass = 85
    attackdata = Attack( (1,10,0) )

class Katana( Item ):
    true_name = "Katana"
    true_desc = ""
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 5
    mass = 45
    attackdata = Attack( (1,10,0) )

class Claymore( Item ):
    true_name = "Claymore"
    true_desc = ""
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 16
    mass = 62
    attackdata = Attack( (1,10,0), double_handed = True )

class GreatSword( Item ):
    true_name = "Greatsword"
    true_desc = ""
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 3
    mass = 150
    attackdata = Attack( (2,6,0), double_handed = True )

class Flamberge( Item ):
    true_name = "Flamberge"
    true_desc = "The flamelike waves on this sword's blade help with parrying enemy attacks."
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 11
    mass = 55
    attackdata = Attack( (1,8,0) )
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })


class SilverShortsword( Item ):
    true_name = "Silver Shortsword"
    true_desc = "This blade was forged to slay unholy creatures. Its light weight favors reflexes over brute strength."
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 28
    mass = 45
    attackdata = Attack( (1,8,0), element=stats.RESIST_SOLAR, skill_mod=stats.REFLEXES )
    statline = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })

class SilverLongsword( Item ):
    true_name = "Silver Longsword"
    true_desc = "This silver blade was forged with protective runes, to do battle against unholy creatures."
    itemtype = SWORD
    avatar_image = "avatar_sword.png"
    avatar_frame = 6
    mass = 45
    attackdata = Attack( (1,10,0), element=stats.RESIST_SOLAR )
    statline = stats.StatMod({ stats.MAGIC_DEFENSE: 5 })


