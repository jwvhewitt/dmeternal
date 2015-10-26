import stats
import animobs
from . import Item,MissileWeapon,ManaWeapon,Ammo,Attack,BOW,ARROW

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
        element=stats.RESIST_PIERCING, shot_anim = animobs.Arrow, reach=8 )


class Longbow( MissileWeapon ):
    true_name = "Longbow"
    true_desc = ""
    itemtype = BOW
    AMMOTYPE = ARROW
    avatar_image = "avatar_bow.png"
    avatar_frame = 1
    mass = 46
    attackdata = Attack( (1,8,0), skill_mod=stats.REFLEXES, damage_mod=None, \
        element=stats.RESIST_PIERCING, shot_anim = animobs.Arrow, reach=8 )

class CompositeShortbow( MissileWeapon ):
    true_name = "Composite Shortbow"
    true_desc = ""
    itemtype = BOW
    AMMOTYPE = ARROW
    avatar_image = "avatar_bow.png"
    avatar_frame = 2
    mass = 37
    attackdata = Attack( (1,8,0), skill_mod=stats.REFLEXES, damage_mod=stats.STRENGTH, \
        element=stats.RESIST_PIERCING, shot_anim = animobs.Arrow, reach=9 )


class CompositeLongbow( MissileWeapon ):
    true_name = "Composite Longbow"
    true_desc = ""
    itemtype = BOW
    AMMOTYPE = ARROW
    avatar_image = "avatar_bow.png"
    avatar_frame = 3
    mass = 51
    attackdata = Attack( (1,10,0), skill_mod=stats.REFLEXES, damage_mod=stats.STRENGTH, \
        element=stats.RESIST_PIERCING, shot_anim = animobs.Arrow, reach=9 )

class FrostBow( ManaWeapon ):
    true_name = "Frost Bow"
    true_desc = ""
    itemtype = BOW
    avatar_image = "avatar_bow.png"
    avatar_frame = 6
    mass = 44
    attackdata = Attack( (2,8,0), skill_mod=stats.REFLEXES, damage_mod=stats.PIETY, \
        element=stats.RESIST_COLD, reach=9, hit_anim=animobs.BlueExplosion,
        shot_anim = animobs.BlueBolt, double_handed=True )



