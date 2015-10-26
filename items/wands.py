import stats
import animobs
from . import ManaWeapon,Attack,WAND

class FireWand( ManaWeapon ):
    true_name = "Fire Wand"
    true_desc = ""
    itemtype = WAND
    MP_COST = 1
    avatar_image = "avatar_wand.png"
    avatar_frame = 2
    mass = 5
    attackdata = Attack( (1,8,1), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_FIRE, reach=7, hit_anim=animobs.OrangeExplosion,
        shot_anim = animobs.Fireball)

class IceWand( ManaWeapon ):
    true_name = "Ice Wand"
    true_desc = ""
    itemtype = WAND
    MP_COST = 1
    avatar_image = "avatar_wand.png"
    avatar_frame = 1
    mass = 5
    attackdata = Attack( (1,8,1), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_COLD, reach=7, hit_anim=animobs.BlueExplosion,
        shot_anim = animobs.BlueComet )

class AcidWand( ManaWeapon ):
    true_name = "Acid Wand"
    true_desc = ""
    itemtype = WAND
    MP_COST = 1
    avatar_image = "avatar_wand.png"
    avatar_frame = 0
    mass = 5
    attackdata = Attack( (1,8,1), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_ACID, reach=7, hit_anim=animobs.GreenSplat,
        shot_anim = animobs.GreenSpray )

class LightningWand( ManaWeapon ):
    true_name = "Lightning Wand"
    true_desc = ""
    itemtype = WAND
    MP_COST = 1
    avatar_image = "avatar_wand.png"
    avatar_frame = 27
    mass = 5
    attackdata = Attack( (1,8,1), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_LIGHTNING, reach=7, hit_anim=animobs.BlueZap,
        shot_anim = animobs.Lightning )

class TelekinesisWand( ManaWeapon ):
    true_name = "Telekinesis Wand"
    true_desc = ""
    itemtype = WAND
    MP_COST = 1
    avatar_image = "avatar_wand.png"
    avatar_frame = 21
    mass = 5
    attackdata = Attack( (3,6,0), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_CRUSHING, reach=7, hit_anim=animobs.RedBoom,
        shot_anim = animobs.CrystalBall )

