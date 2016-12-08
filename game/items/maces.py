from .. import stats
from . import Item,Attack,MACE

class FlangedMace( Item ):
    true_name = "Flanged Mace"
    true_desc = ""
    itemtype = MACE
    avatar_image = "avatar_mace.png"
    avatar_frame = 8
    mass = 40
    attackdata = Attack( (1,6,0), element = stats.RESIST_CRUSHING )

class Club( Item ):
    true_name = "Club"
    true_desc = "A big piece of wood."
    itemtype = MACE
    avatar_image = "avatar_mace.png"
    avatar_frame = 0
    mass = 30
    attackdata = Attack( (1,6,0), element = stats.RESIST_CRUSHING )

class Warhammer( Item ):
    true_name = "Warhammer"
    true_desc = ""
    itemtype = MACE
    avatar_image = "avatar_mace.png"
    avatar_frame = 7
    mass = 80
    attackdata = Attack( (1,8,0), element = stats.RESIST_CRUSHING )

class Morningstar( Item ):
    true_name = "Morningstar"
    true_desc = ""
    itemtype = MACE
    avatar_image = "avatar_mace.png"
    avatar_frame = 12
    mass = 70
    attackdata = Attack( (1,8,0), element = stats.RESIST_CRUSHING )

class TitanHammer( Item ):
    true_name = "Hammer of the Titans"
    true_desc = ""
    itemtype = MACE
    avatar_image = "avatar_titanic.png"
    avatar_frame = 0
    mass = 1400
    attackdata = Attack( (5,8,0), element = stats.RESIST_CRUSHING )


