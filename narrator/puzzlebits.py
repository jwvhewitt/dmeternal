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
import namegen
import random
import randmaps
import stats
import effects
import animobs

""" PuzzleBits are atomic actions which can be used to generate random puzzles.
    Generation happens backwards, starting with the end state and stringing
    along actions until the causality chain terminates.

    A PB request will include an element TARGET, which is the thing to be
    affected by the action. When the action is performed, a script trigger
    will be sprung with a trigger ID equal to the action name (minus "PB_")
    and thing set to the target item.
"""

#  **********************
#  ***   PB_DESTROY   ***
#  **********************
#
# TARGET must be destroyed.

class DESTROY_JustAddWater( Plot ):
    """This DES_FIRE type target can be destroyed by opening water main."""
    LABEL = "PB_DESTROY"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires LOCALE, TARGET, and TARGET.desctags to include DES_FIRE."""
        # Probably not the best way to do this... probably not important anyhow.
        return (pstate.elements.get("LOCALE") and pstate.elements.get("TARGET")
         and hasattr(pstate.elements["TARGET"],"desctags") and 
         context.DES_FIRE in pstate.elements["TARGET"].desctags)
    def custom_init( self, nart ):
        # Create the lever and water control room.
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )

        # Lever room
        lever_room = randmaps.rooms.SharpRoom( tags = (context.ENTRANCE,) )
        lever_room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=150, habitat=scene.get_encounter_request() ) )
        self.register_element( "_LEVER_ROOM", lever_room, dident="LOCALE" )

        lever = waypoints.PuzzleSwitch()
        self.register_element( "_LEVER", lever, dident="_LEVER_ROOM" )
        lever_room.contents.append( waypoints.Signpost( desc="**WATER MAIN CONTROL** \n Use only in case of emergency. Unauthorized use punishable by fines or death.", anchor=randmaps.anchors.middle ))

        return True

    def _LEVER_USE( self, explo ):
        explo.alert( "You hear flowing water, followed by the hiss of steam." )
        self.active = False
        explo.check_trigger( "WIN", self )

class DESTROY_SpiritPower( Plot ):
    """Fight the elemental power source."""
    LABEL = "PB_DESTROY"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires LOCALE, TARGET, and TARGET.desctags."""
        # Probably not the best way to do this... probably not important anyhow.
        return (pstate.elements.get("LOCALE") and pstate.elements.get("TARGET")
         and hasattr(pstate.elements["TARGET"],"desctags") and 
         pstate.elements["TARGET"].desctags)
    def custom_init( self, nart ):
        # Create the lever and spirit room.
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )

        # Spirit jar room
        puzzle_room = randmaps.rooms.SharpRoom( tags = (context.ENTRANCE,) )
        team = teams.Team(default_reaction=-999, respawn=False )
        if random.randint(1,3) == 1:
            puzzle_room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
              strength=100, habitat=scene.get_encounter_request(), fac=scene.fac ) )
        self.register_element( "_PUZZLE_ROOM", puzzle_room, dident="LOCALE" )
        self.register_element( "_SOURCE", waypoints.SpiritJar(plot_locked=True,anchor=randmaps.anchors.middle), dident="_PUZZLE_ROOM" )
        self.spirit_contained = True

        myhabitat = { (context.MTY_ELEMENTAL,context.MTY_UNDEAD,context.MTY_CELESTIAL,context.MTY_DEMON): True,
            tuple(self.elements["TARGET"].desctags): True}
        btype = monsters.choose_monster_type(self.rank,self.rank+2,myhabitat)
        if btype:
            boss = self.register_element("_MONSTER",monsters.generate_boss( btype, self.rank+2, team=team ))
        if random.randint(1,2) == 1:
            myitem = self.register_element("_ITEM",items.generate_special_item( self.rank + random.randint(1,2)))
        else:
            myitem = self.register_element("_ITEM",items.generate_scroll(self.rank+random.randint(1,2)))

        return btype and myitem

    def _MONSTER_DEATH( self, explo ):
        # Killing the monster cuts the power.
        self.active = False
        explo.check_trigger( "WIN", self )
    def release_spirit( self, explo ):
        # Make a Charisma roll; if successful, get thanked by spirit.
        self.spirit_contained = False
        pc = explo.camp.party_spokesperson()
        spirit = self.elements["_MONSTER"]
        explo.alert("You release the seals on the jar. The spirit emerges...")
        self.elements["_SOURCE"].release_spirit()
        pos = explo.camp.scene.find_entry_point_in_rect(self.elements["_PUZZLE_ROOM"].area)
        spirit.place( explo.camp.scene, pos )
        explo.invoke_effect( effects.NoEffect(anim=animobs.PurpleSparkle),None,(pos,))
        charm_roll = random.randint(1,100) + pc.get_stat_bonus( stats.CHARISMA ) + pc.rank() * 4 - spirit.get_stat( stats.MAGIC_DEFENSE ) - spirit.get_stat_bonus( stats.CHARISMA )
        if charm_roll > 74:
            # Congratulations! The spirit is grateful.
            reward = self.elements["_ITEM"]
            explo.alert('''"Hello {}; my name is {}", it says. "I have been trapped in this place for so long. In thanks for releasing me, I give you this {}."'''.format(pc,spirit,reward))
            pc.contents.append( reward )
            explo.invoke_effect( effects.NoEffect(anim=animobs.YellowSparkle),None,(pos,pc.pos))
            explo.camp.scene.contents.remove(spirit)
            self.active = False
            explo.check_trigger( "WIN", self )
        else:
            # Whoops. This isn't a friendly spirit.
            explo.alert("It attacks!")
            explo.camp.activate_monster( spirit )
    def _SOURCE_menu( self, thingmenu ):
        if self.spirit_contained:
            thingmenu.desc = "This spirit jar appears to contain a {}; its power is being drained for some nefarious purpose.".format(self.elements["_MONSTER"].monster_name)
            thingmenu.add_item( "Release the spirit.", self.release_spirit )
            thingmenu.add_item( "Leave it alone, for now.", None )
        else:
            thingmenu.desc = "This spirit jar is now empty."

#  *******************
#  ***   PB_OPEN   ***
#  *******************

class OPEN_HintAndSearch( Plot ):
    """The PC will learn there's a secret door in the waypoint, and can then search."""
    LABEL = "PB_OPEN"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist and be a waypoint."""
        # Probably not the best way to do this... probably not important anyhow.
        return pstate.elements.get("TARGET") and isinstance( pstate.elements["TARGET"], waypoints.Waypoint )
    def custom_init( self, nart ):
        """Create the hint, call a get secret subplot."""
        self._learned = False
        target = self.elements["TARGET"]
        if not hasattr( target, "mini_map_label" ):
            target.mini_map_label = "Thingamajig"
        secret = self.register_element( "_MYSECRET", "There's a {0} around here with a secret panel in it.".format( target.mini_map_label ) )
        self.add_sub_plot( nart, "GET_SECRET", PlotState( elements={"TARGET":secret} ).based_on( self ) )
        return True
    def _MYSECRET_SECRET( self, explo ):
        self._learned = True
    def TARGET_menu( self, thingmenu ):
        if self._learned:
            thingmenu.add_item( "Look for the secret panel.", self.use_panel )
    def use_panel( self, explo ):
        explo.alert( "You find the secret panel and open a passageway." )
        explo.check_trigger( "OPEN", self.elements[ "TARGET" ] )
        self.active = False

class OPEN_Lever( Plot ):
    """Pull a switch, open the whatever."""
    LABEL = "PB_OPEN"
    UNIQUE = False
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist."""
        return pstate.elements.get("TARGET")
    def custom_init( self, nart ):
        """Create the lever, call a getter subplot."""
        lever = self.register_element( "_LEVER", waypoints.PuzzleSwitch() )
        self.add_sub_plot( nart, "GET_THING", PlotState( elements={"TARGET":lever} ).based_on( self ) )
        return True
    def _LEVER_USE( self, explo ):
        explo.alert( "You hear a grinding sound in the distance." )
        explo.check_trigger( "OPEN", self.elements[ "TARGET" ] )
        self.active = False


class OPEN_SecretKnock( Plot ):
    """The PC will learn there's a secret knock to open the waypoint."""
    LABEL = "PB_OPEN"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the TARGET to exist and be a waypoint."""
        # Probably not the best way to do this... probably not important anyhow.
        return pstate.elements.get("TARGET") and isinstance( pstate.elements["TARGET"], waypoints.Waypoint )
    def custom_init( self, nart ):
        """Create the hint, call a get secret subplot."""
        self._learned = False
        target = self.elements["TARGET"]
        if not hasattr( target, "mini_map_label" ):
            target.mini_map_label = "Thingamajig"
        secret = self.register_element( "_MYSECRET", "To open the {0}, knock three times.".format( target.mini_map_label ) )
        self.add_sub_plot( nart, "GET_SECRET", PlotState( elements={"TARGET":secret} ).based_on( self ) )
        return True
    def _MYSECRET_SECRET( self, explo ):
        self._learned = True
    def TARGET_menu( self, thingmenu ):
        if self._learned:
            thingmenu.add_item( "Knock three times.", self.use_panel )
    def use_panel( self, explo ):
        explo.alert( "You knock on the {0}. Moments later, a secret passageway creaks open.".format( self.elements["TARGET"].mini_map_label) )
        explo.check_trigger( "OPEN", self.elements[ "TARGET" ] )
        self.active = False



