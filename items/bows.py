import stats
import animobs
from . import Item,MissileWeapon,Ammo,Attack,BOW,ARROW

class Arrows( Ammo ):
    true_name = "Arrows"
    true_desc = "The ammunition for bows."
    itemtype = ARROW
    mass_per_shot = 2

class Shortbow( MissileWeapon ):
    true_name = "Shortbow"
    true_desc = ""
    itemtype = BOW
    AMMOTYPE = ARROW
    avatar_image = "avatar_bow.png"
    avatar_frame = 0
    mass = 32
    attackdata = Attack( (1,6,0), skill_mod=stats.REFLEXES, damage_mod=None, \
        element=stats.RESIST_PIERCING, reach=8 )
    shot_anim = animobs.Arrow


class Longbow( MissileWeapon ):
    true_name = "Longbow"
    true_desc = ""
    itemtype = BOW
    AMMOTYPE = ARROW
    avatar_image = "avatar_bow.png"
    avatar_frame = 1
    mass = 46
    attackdata = Attack( (1,8,0), skill_mod=stats.REFLEXES, damage_mod=None, \
        element=stats.RESIST_PIERCING, reach=8 )
    shot_anim = animobs.Arrow

