
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


        for job in characters.PC_CLASSES:
            self.add_sub_plot( nart, "RESOURCE_JOBTRAINER", PlotState( elements={"JOB":job} ) )

        return True


class BardicStub( Plot ):
    LABEL = "STUB_BARDIC"
    # Creates a simple, plot-free dungeon adventure.

    def custom_init( self, nart ):
        """Create the world + starting scene, then load INTRO_2"""
        w = worlds.World()
        nart.camp.contents.append( w )
        self.register_element( "WORLD", w )
        self.chapter = Chapter( end_rank=0, world=w )
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

