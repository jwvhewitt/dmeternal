from .. import stats
from . import Item,Attack,GLOVE

class KnuckleGloves( Item ):
    true_name = "Knuckle Gloves"
    true_desc = ""
    itemtype = GLOVE
    avatar_image = "avatar_arm.png"
    avatar_frame = 1
    mass = 1

class LeatherGloves( Item ):
    true_name = "Leather Gloves"
    true_desc = ""
    itemtype = GLOVE
    avatar_image = "avatar_arm.png"
    avatar_frame = 3
    mass = 2

class BracersOfDefense( Item ):
    true_name = "Bracers of Defense"
    true_desc = ""
    itemtype = GLOVE
    avatar_image = "avatar_arm.png"
    avatar_frame = 16
    mass = 8
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.MAGIC_DEFENSE: 5, stats.NATURAL_DEFENSE: 5 })






