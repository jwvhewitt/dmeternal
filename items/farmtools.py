import stats
from . import Item,Attack,FARMTOOL

class Sickle( Item ):
    true_name = "Sickle"
    true_desc = ""
    itemtype = FARMTOOL
    avatar_image = "avatar_farmtool.png"
    avatar_frame = 0
    mass = 15
    attackdata = Attack( (1,6,0), element = stats.RESIST_SLASHING )

class Pitchfork( Item ):
    true_name = "Pitchfork"
    true_desc = "A farm tool that can also be used as a weapon."
    itemtype = FARMTOOL
    avatar_image = "avatar_farmtool.png"
    avatar_frame = 1
    attackdata = Attack( (1,6,0), element = stats.RESIST_PIERCING, double_handed=True )
    mass = 65


