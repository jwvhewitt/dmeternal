import stats
from . import Item,Attack,HELM

class SteelHelmet( Item ):
    true_name = "Steel Helmet"
    true_desc = ""
    itemtype = HELM
    avatar_image = "avatar_helm.png"
    avatar_frame = 0
    mass = 30
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })

class ChainCoif( Item ):
    true_name = "Chain Coif"
    true_desc = ""
    itemtype = HELM
    avatar_image = "avatar_helm.png"
    avatar_frame = 1
    mass = 20
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.AWARENESS: -5 })

class HornedHelmet( Item ):
    true_name = "Horned Helmet"
    true_desc = ""
    itemtype = HELM
    avatar_image = "avatar_helm.png"
    avatar_frame = 2
    mass = 25
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5, stats.STEALTH: -5 })

class SteelHelm( Item ):
    true_name = "Steel Helm"
    true_desc = ""
    itemtype = HELM
    avatar_image = "avatar_helm.png"
    avatar_frame = 5
    mass = 55
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.AWARENESS: -10 })

class PlumedHelm( Item ):
    true_name = "Plumed Helm"
    true_desc = ""
    itemtype = HELM
    avatar_image = "avatar_helm.png"
    avatar_frame = 4
    mass = 55
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.AWARENESS: -10, stats.STEALTH: -5 })

