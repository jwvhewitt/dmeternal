from plots import Plot,PlotError,PlotState
import context
import items
import maps
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import random


class CashReward( Plot ):
    """Get a cash payout and XP."""
    LABEL = "REWARD"
    UNIQUE = False
    active = False
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the ORIGIN to exist."""
        return pstate.elements.get("ORIGIN")
    def give_reward( self, explo ):
        gp = self.rank * 100 + random.randint(1,100)
        explo.camp.gold += gp
        for pc in explo.camp.party:
            pc.xp += 100
        explo.alert( "You gain {0}gp and 100XP.".format( gp ) )
        self.active = False
    def ORIGIN_offers( self, explo ):
        ol = list()
        ol.append( dialogue.Offer( "Here is some gold to thank you for your help.",
             context = context.ContextTag([context.REWARD]), effect=self.give_reward )
        )
        return ol

class ScrollReward( Plot ):
    """Get a scroll and XP."""
    LABEL = "REWARD"
    UNIQUE = False
    active = False
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the ORIGIN to exist and be a spellcaster."""
        return pstate.elements.get("ORIGIN") and pstate.elements["ORIGIN"].total_spell_gems()
    def custom_init( self, nart ):
        self._scroll = items.generate_scroll(self.rank)
        return self._scroll
    def give_reward( self, explo ):
        pc = explo.camp.first_living_pc()
        pc.contents.append( self._scroll )
        for pc in explo.camp.party:
            pc.xp += 100
        explo.alert( "You gain a {0} and 100XP.".format( self._scroll ) )
        self.active = False
    def ORIGIN_offers( self, explo ):
        ol = list()
        ol.append( dialogue.Offer( "Here is a {} to thank you for your help.".format(self._scroll),
             context = context.ContextTag([context.REWARD]), effect=self.give_reward )
        )
        return ol


