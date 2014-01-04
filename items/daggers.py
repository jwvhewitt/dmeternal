import stats
from . import Item,Attack,DAGGER

class Dagger( Item ):
    true_name = "Dagger"
    true_desc = ""
    itemtype = DAGGER
    avatar_image = "avatar_dagger.png"
    avatar_frame = 0
    mass = 12
    attackdata = Attack( (1,4,0), element = stats.RESIST_PIERCING )

class Sickle( Dagger ):
    true_name = "Sickle"
    true_desc = ""
    avatar_frame = 4
    mass = 15
    attackdata = Attack( (1,6,0) )

class Dirk( Dagger ):
    true_name = "Dirk"
    true_desc = ""
    avatar_frame = 3
    mass = 16
    attackdata = Attack( (1,6,0) )


