import stats
from . import Item,Attack,DAGGER

class Dagger( Item ):
    true_name = "Dagger"
    true_desc = ""
    itemtype = DAGGER
    avatar_image = "avatar_dagger.png"
    avatar_frame = 2
    mass = 12
    attackdata = Attack( (1,4,0), element = stats.RESIST_PIERCING )

class Dirk( Dagger ):
    true_name = "Dirk"
    true_desc = ""
    avatar_frame = 1
    mass = 16
    attackdata = Attack( (1,6,0) )

class Stiletto( Dagger ):
    true_name = "Stiletto"
    true_desc = ""
    avatar_frame = 5
    mass = 13
    attackdata = Attack( (1,6,0), element = stats.RESIST_PIERCING, skill_mod=stats.REFLEXES )

