import stats
from . import Item,Attack,STAFF

class Quarterstaff( Item ):
    true_name = "Quarterstaff"
    true_desc = ""
    itemtype = STAFF
    avatar_image = "avatar_staff.png"
    avatar_frame = 0
    attackdata = Attack( (1,4,0), double_handed = True, element = stats.RESIST_CRUSHING )
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })
    mass = 20

class IronStaff( Item ):
    true_name = "Iron Staff"
    true_desc = ""
    itemtype = STAFF
    avatar_image = "avatar_staff.png"
    avatar_frame = 1
    attackdata = Attack( (1,8,0), double_handed = True, element = stats.RESIST_CRUSHING )
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })
    mass = 105



