from .. import stats
from . import Item,Attack,SHOES,BOOTS,SANDALS


class NormalShoes( Item ):
    true_name = "Shoes"
    true_desc = "Sturdy leather shoes."
    itemtype = SHOES
    avatar_image = "avatar_boot.png"
    avatar_frame = 2
    mass = 4

class NormalBoots( NormalShoes ):
    true_name = "Boots"
    true_desc = "Sturdy leather boots."
    itemtype = BOOTS
    avatar_frame = 8
    mass = 7

class NormalSandals( NormalShoes ):
    true_name = "Sandals"
    true_desc = "Plain sandals."
    itemtype = SANDALS
    avatar_frame = 16
    mass = 3


