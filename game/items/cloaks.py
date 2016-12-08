from .. import stats
from . import Item,Attack,CLOAK

class NormalCloak( Item ):
    true_name = "Cloak"
    true_desc = "A warm grey cloak."
    itemtype = CLOAK
    avatar_image = "avatar_cloak.png"
    avatar_frame = 0
    mass = 10
    statline = stats.StatMod({ stats.RESIST_COLD: 5 })

class ThiefCloak( NormalCloak ):
    true_name = "Thief Cloak"
    true_desc = "A dark cloak to help you hide in shadows."
    avatar_frame = 4
    statline = stats.StatMod({ stats.STEALTH: 5, stats.RESIST_COLD: 5 })

class FireproofCloak( NormalCloak ):
    true_name = "Fireproof Cloak"
    true_desc = "A thick cloak made of a fireproof material."
    avatar_frame = 7
    statline = stats.StatMod({ stats.RESIST_COLD: 5, stats.RESIST_FIRE: 25 })

class WeatherproofCloak( NormalCloak ):
    true_name = "Weatherproof Cloak"
    true_desc = "A thick cloak which will protect you from harsh elements."
    avatar_frame = 1
    statline = stats.StatMod({ stats.STEALTH: 5, stats.RESIST_COLD: 20, stats.RESIST_WIND: 20, stats.RESIST_WATER: 20 })



