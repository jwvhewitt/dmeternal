import stats
import animobs
from . import Item,MissileWeapon,Ammo,Attack,SLING,BULLET

class Bullets( Ammo ):
    true_name = "Bullets"
    true_desc = "The ammunition for slings."
    itemtype = BULLET

class Sling( MissileWeapon ):
    true_name = "Sling"
    true_desc = ""
    itemtype = SLING
    AMMOTYPE = BULLET
    avatar_image = "avatar_sling.png"
    avatar_frame = 0
    mass = 8
    attackdata = Attack( (1,4,0), skill_mod=stats.REFLEXES, damage_mod=None, \
        element=stats.RESIST_CRUSHING, reach=6 )
    shot_anim = animobs.SlingStone

