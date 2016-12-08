from .. import stats
from .. import animobs
from .. import effects
from .. import enchantments
from . import Item,ManaWeapon,Attack,WAND

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
        shot_anim = animobs.BlueBolt )

class FrostWand( ManaWeapon ):
    true_name = "Frost Wand"
    true_desc = "On a successful hit, this wand may freeze its target solid for a short time."
    itemtype = WAND
    MP_COST = 1
    avatar_image = "avatar_wand.png"
    avatar_frame = 12
    mass = 5
    attackdata = Attack( (3,4,0), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_COLD, reach=7, hit_anim=animobs.BlueExplosion,
        shot_anim = animobs.BlueBolt, extra_effect=effects.OpposedRoll( on_success = (
        effects.Paralyze( max_duration = 3 )
        ,)) )

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

class WindWand( ManaWeapon ):
    true_name = "Wind Wand"
    true_desc = ""
    itemtype = WAND
    MP_COST = 1
    avatar_image = "avatar_wand.png"
    avatar_frame = 4
    mass = 5
    attackdata = Attack( (2,4,1), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_WIND, reach=7, hit_anim=animobs.Spiral,
        shot_anim = animobs.Whirlwind )

class WaterWand( ManaWeapon ):
    true_name = "Water Wand"
    true_desc = ""
    itemtype = WAND
    MP_COST = 1
    avatar_image = "avatar_wand.png"
    avatar_frame = 22
    mass = 5
    attackdata = Attack( (2,4,1), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_WATER, reach=7, hit_anim=animobs.Bubbles,
        shot_anim = animobs.BlueComet )

class SunWand( ManaWeapon ):
    true_name = "Sun Wand"
    true_desc = ""
    itemtype = WAND
    MP_COST = 1
    avatar_image = "avatar_wand.png"
    avatar_frame = 11
    mass = 5
    attackdata = Attack( (2,4,1), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_SOLAR, reach=7, hit_anim=animobs.YellowExplosion,
        shot_anim = animobs.YellowBolt )

class WitherWand( ManaWeapon ):
    true_name = "Wither Wand"
    true_desc = "This wand drains the strength of its target."
    itemtype = WAND
    MP_COST = 2
    avatar_image = "avatar_wand.png"
    avatar_frame = 7
    mass = 5
    attackdata = Attack( (1,8,1), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_LUNAR, reach=7, hit_anim=animobs.PurpleExplosion,
        shot_anim = animobs.MysticBolt, extra_effect=effects.StatDamage( stats.STRENGTH, amount=3 ) )

class VenomWand( ManaWeapon ):
    true_name = "Venom Wand"
    true_desc = "A hit from this wand will poison living creatures."
    itemtype = WAND
    MP_COST = 2
    avatar_image = "avatar_wand.png"
    avatar_frame = 10
    mass = 5
    attackdata = Attack( (1,8,1), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_WATER, reach=7, hit_anim=animobs.GreenCloud,
        shot_anim = animobs.GreenSpray, 
        extra_effect=effects.TargetIs( effects.ALIVE, on_true=( 
              effects.Enchant( enchantments.PoisonClassic ),
        ) ) )

class TelekinesisWand( ManaWeapon ):
    true_name = "Telekinesis Wand"
    true_desc = ""
    itemtype = WAND
    MP_COST = 2
    avatar_image = "avatar_wand.png"
    avatar_frame = 21
    mass = 5
    attackdata = Attack( (3,6,0), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_CRUSHING, reach=7, hit_anim=animobs.RedBoom,
        shot_anim = animobs.CrystalBall )

class AtomicWand( ManaWeapon ):
    true_name = "Atomic Wand"
    true_desc = ""
    itemtype = WAND
    MP_COST = 3
    avatar_image = "avatar_wand.png"
    avatar_frame = 9
    mass = 5
    attackdata = Attack( (2,6,1), skill_mod=stats.REFLEXES, damage_mod=stats.INTELLIGENCE, \
        element=stats.RESIST_ATOMIC, reach=7, hit_anim=animobs.Nuclear,
        shot_anim = animobs.Fireball )

