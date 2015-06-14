
from plots import Plot,PlotError,Chapter,PlotState
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
import worlds


#
# This unit contains the one and only ADVSTUB plot. This is the first plot
# initialized in the adventure, and its only purpose is to load all of the other
# adventure components. Yay ADVSTUB!
#

class SpoonyStub( Plot ):
    LABEL = "STUB_SPOONY"
    # Creates a supposedly plot-rich dungeon adventure.
    def custom_init( self, nart ):
        """Create the world + base camp."""
        w = worlds.World()
        nart.camp.contents.append( w )
        self.register_element( "WORLD", w )
        self.chapter = Chapter( end_rank=0, world=w )
        self.add_first_locale_sub_plot( nart )

        # Determine the chapter sizes.
        if nart.end_rank < 7:
            min_dungeon_size = 2
        else:
            min_dungeon_size = 3
        num_dungeon,extra_points = divmod( nart.end_rank, min_dungeon_size )

        # Step One- Generate a plot sequence, starting at the end and moving
        #  backwards to the beginning.

        # Step Two- Moving forward through the plot, connect the plot points.


        # Step Three- Add resources and whatnot.
        for job in characters.PC_CLASSES:
            self.add_sub_plot( nart, "RESOURCE_JOBTRAINER", PlotState( elements={"JOB":job} ) )

        return True

# Shortie Done-in-one Dungeon Monkey Adventure
# - A small adventure, typically consisting of a single dungeon or wilderness
#   area.
# - Despite the limited area, see how interesting you can make it.

class ShortieStub( Plot ):
    LABEL = "STUB_SHORTIE"
    SHORTIE_GRAMMAR = {
        # [ADVENTURE] is the top level token- it will expand into a number of
        # high level tokens.
        "[ADVENTURE]": [ "[IMPERILED_PLACE] [ENEMY_BASE] [ENEMY_GOAL]",
            ],

        "[ENEMY_BASE]": [ "SDI_ENEMY_FORT SDI_ENEMY_BARRACKS SDI_BLOCKED_GATE",
            "SDI_HIDDEN_BASE SDI_WILD_DUNGEON SDI_ENEMY_BARRACKS"
            ],

        "[ENEMY_GOAL]": [ "SDI_SUPERWEAPON",
            "SDI_BOSSFIGHT"
            ],

        "[IMPERILED_PLACE]": [ "SDI_AMBUSH SDI_VILLAGE",
            "SDI_ALLIED_CAMP SDI_RECON", "SDI_VILLAGE SDI_RECON"
            ],
    }
    def custom_init( self, nart ):
        """Create the world + starting scene."""
        w = worlds.World()
        nart.camp.contents.append( w )
        self.register_element( "WORLD", w )
        self.chapter = Chapter( start_rank=nart.start_rank, end_rank=nart.end_rank, world=w )
        self.rank = nart.start_rank
        if not self.setting:
            self.setting = context.SET_RENFAN

        # Generate a plot outline for the adventure. We will do this using a
        # context free grammar expansion of the token [ADVENTURE]. The resultant
        # string will be a list of subplot request labels.
        subplot_list = self.register_element( "shortie_outline", list( dialogue.grammar.convert_tokens( "[ADVENTURE]", self.SHORTIE_GRAMMAR ).split() ) )
        print subplot_list

        # Assemble the outline into an adventure. Basically, add a subplot of
        # each generated type, in order. Each subplot describes a stage of the
        # mini adventure- usually a single scene, maybe also several scenes or
        # part of a scene, whatever.
        prev_subplot = self
        for spr in subplot_list:
            prev_subplot = self.add_sub_plot( nart, spr,
                PlotState().based_on(prev_subplot) )


        return True

# VDMA Visual Dungeon Monkey Adventure
# - World map replaced by realms map, showing area to explore.
#   Entering territory brings up VN style menu of places to explore and
#   things to do.
# - Core story + rival agents. PC may interact with agents during chapter.
#   When chapter ends, success or failure of other agents determined.
# - In general, "expert play" should make the game harder but unlock better
#   or different endings.

class BardicStub( Plot ):
    LABEL = "STUB_BARDIC"
    # Creates a simple, plot-free dungeon adventure.

    def custom_init( self, nart ):
        """Create the world + starting scene."""
        w = worlds.World()
        nart.camp.contents.append( w )
        self.register_element( "WORLD", w )
        self.chapter = Chapter( end_rank=0, world=w )
        if not self.setting:
            self.setting = context.SET_RENFAN
        self.add_first_locale_sub_plot( nart )

        # Determine the dungeon sizes.
        if nart.end_rank < 7:
            min_dungeon_size = 2
        else:
            min_dungeon_size = 3
        num_dungeon,extra_points = divmod( nart.end_rank, min_dungeon_size )
        
        prev_chapter = self.chapter
        prev_subplot = self
        for t in range( num_dungeon ):
            # We're going to add dungeons/chapters sequentially.
            new_chapter = Chapter(follows=prev_chapter)
            new_chapter.end_rank = new_chapter.start_rank + min_dungeon_size - 1
            if t == num_dungeon-1:
                new_chapter.end_rank += extra_points
            prev_subplot = self.add_sub_plot( nart, "BARDIC_DUNGEON",
                PlotState(chapter=new_chapter).based_on(prev_subplot) )
            prev_chapter = new_chapter

        # At this point, we can add the conclusion.
        self.add_sub_plot( nart, "BARDIC_CONCLUSION", PlotState(rank=nart.end_rank).based_on(prev_subplot) )

        for job in characters.PC_CLASSES:
            self.add_sub_plot( nart, "RESOURCE_JOBTRAINER", PlotState( elements={"JOB":job} ) )

        return True


class AdventureStub( Plot ):
    LABEL = "ADVSTUB"

    def custom_init( self, nart ):
        """Create the world + chapter + city, then load INTRO_2"""
        w = worlds.World()
        nart.camp.contents.append( w )
        self.register_element( "WORLD", w )
        self.chapter = Chapter( world=w )
        self.add_first_locale_sub_plot( nart )

        sp = self.add_sub_plot( nart, "INTRO_1" )

        for job in characters.PC_CLASSES:
            self.add_sub_plot( nart, "RESOURCE_JOBTRAINER", PlotState( elements={"JOB":job} ) )

        self.add_sub_plot( nart, "TESTPLOT", spstate=PlotState().based_on(sp), necessary=False )

        return True

