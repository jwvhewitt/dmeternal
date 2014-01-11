from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats

BLESSING = Spell( "BLESSING", "Blessing",
    "Increases the physical and magic attack scores of all allies within 6 tiles by +5%. This effect lasts until the end of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.BlessingEn, anim=animobs.YellowSparkle )
    ,) ), rank=1, gems={SOLAR:1}, com_tar=targetarea.SelfCentered() )


