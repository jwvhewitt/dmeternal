from .plots import Plot,PlotError,PlotState
from .. import context
from .. import items
from .. import maps
from .. import randmaps
from .. import waypoints
from .. import monsters
from .. import dialogue
from .. import services
from .. import teams
from .. import characters
import random
from .. import stats
from .. import namegen

### SideStories are stories affecting the people in a building in a city.
### They are there to add flavor, and typically won't be particularly
### important.

class DateMyCousinPlease( Plot ):
    """The cousin of the shopkeeper must be removed from the house."""
    LABEL = "SIDE_STORY"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the SHOPKEEPER, SHOPKEEPER.species, and BUILDING_INT to exist."""
        return pstate.elements.get("SHOPKEEPER") and pstate.elements.get("SHOPKEEPER").species and pstate.elements.get("BUILDING_INT")
    def room_seeker( self, thing ):
        return isinstance( thing, randmaps.Room ) and context.ROOM_PUBLIC in thing.tags
    def custom_init( self, nart ):
        """Create the cousin, add puzzle subplot."""
        npc = self.elements["SHOPKEEPER"]
        the_room = self.seek_element( nart, "_THE_ROOM", self.room_seeker, scope=self.elements.get("BUILDING_INT") )
        the_cousin = monsters.generate_npc(species=npc.species.__class__)
        self.register_element( "TARGET", the_cousin )
        self.started = False
        self.dated = False
        self.add_sub_plot( nart, "SB_DATE", PlotState().based_on( self ) )
        self.add_sub_plot( nart, "REWARD", PlotState(elements={"ORIGIN":npc}).based_on( self ), ident="next" )
        return True
    def TARGET_DATE( self, explo ):
        self.dated = True
        self.subplots["next"].active = True
    def tell_problem( self, explo ):
        # Move the cousin into the room.
        scene = self.elements["BUILDING_INT"]
        area = self.elements["_THE_ROOM"].area
        pos = scene.find_entry_point_in_rect(area)
        if pos:
            the_cousin = self.elements["TARGET"]
            the_cousin.place( scene, pos )
            self.started = True
    def TARGET_offers( self, explo ):
        ol = list()
        if self.dated:
            myoffer = dialogue.Offer( "Thanks for helping me out.",
             context = context.ContextTag([context.HELLO]) )
            ol.append( myoffer )
        return ol
    def SHOPKEEPER_offers( self, explo ):
        ol = list()
        the_cousin = self.elements["TARGET"]
        if self.dated and self.subplots["next"].active:
            myoffer = dialogue.Offer( msg = "Thanks for getting {0} out of my hair; {1} still hangs around here too much but it's better than it used to be.".format(the_cousin, the_cousin.subject_pronoun()) ,
             context = context.ContextTag( [context.HELLO,context.REWARD] ) ,
             replies = [ dialogue.Reply( "You're welcome." ,
                    destination = dialogue.Cue( context.ContextTag( [context.REWARD] ) ) ) ]
             )
            ol.append( myoffer )
        elif not self.started:
            myoffer = dialogue.Offer( "It's my cousin {0}... {1} hangs out here all day bothering me.".format(the_cousin,the_cousin.subject_pronoun()),
             context = context.ContextTag([context.PROBLEM,context.PERSONAL]), effect=self.tell_problem )
            ol.append( myoffer )
        return ol

class DungeonBreakthrough( Plot ):
    """Work in the basement has broken through to a dungeon."""
    LABEL = "SIDE_STORY"
    UNIQUE = True
    active = True
    scope = "BUILDING_INT"
    @classmethod
    def matches( self, pstate ):
        """Requires the SHOPKEEPER and BUILDING_INT to exist."""
        return pstate.elements.get("SHOPKEEPER") and pstate.elements.get("BUILDING_INT")
    def custom_init( self, nart ):
        prev = self.elements["BUILDING_INT"]
        # Generate the levels
        self.levels = self.get_dungeon_levels( nart, tuple(), min( prev.rank+2, self.rank ), self.rank )
        # Connect all the levels, and name them.
        self.install_dungeon( nart, self.levels, prev, "Dungeon of {0}".format( namegen.ELDRITCH.gen_word() ) )
        return True
    def end_plot( self, explo ):
        self.active = False
    def SHOPKEEPER_offers( self, explo ):
        ol = list()
        myoffer = dialogue.Offer( msg = "When we were working on the basiment earlier we broke through into some kind of dungeon. You're free to go downstairs and check it out.",
             context = context.ContextTag( [context.INFO,context.HINT] ), effect=self.end_plot)
        ol.append( myoffer )
        return ol


class TooMuchWork( Plot ):
    """The significant other of the shopkeeper sends you on a quest to find some
       part time help."""
    LABEL = "SIDE_STORY"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the SHOPKEEPER, SHOPKEEPER.species, and BUILDING_INT to exist."""
        return pstate.elements.get("SHOPKEEPER") and pstate.elements.get("SHOPKEEPER").species and pstate.elements.get("BUILDING_INT")
    def room_seeker( self, thing ):
        return isinstance( thing, randmaps.Room ) and context.ROOM_PUBLIC in thing.tags
    def custom_init( self, nart ):
        sk = self.elements["SHOPKEEPER"]
        the_room = self.seek_element( nart, "_THE_ROOM", self.room_seeker, scope=self.elements.get("BUILDING_INT") )
        npc = monsters.generate_npc(species=sk.species.__class__)
        # Assume a heteronormativity rate of 50%.
        if random.randint(1,2) == 1:
            if sk.gender == stats.MALE:
                npc.gender = stats.FEMALE
            elif sk.gender == stats.FEMALE:
                npc.gender = stats.MALE
        self.register_element( "_NPC", npc, dident="_THE_ROOM" )
        self.add_sub_plot( nart, "REWARD", PlotState(elements={"ORIGIN":npc}).based_on( self ), ident="next" )
        self.quest_started = False
        self.employees = [sk,npc]
        self.needed_stat = random.choice( stats.PRIMARY_STATS )
        return True
    def start_quest( self, explo ):
        self.quest_started = True
    def end_quest( self, explo ):
        self.active = False
    STAT_DESC = { stats.STRENGTH: "strong", stats.TOUGHNESS: "hardy", stats.REFLEXES: "quick", \
        stats.INTELLIGENCE: "smart", stats.PIETY: "diligent", stats.CHARISMA: "friendly" }
    def _NPC_offers( self, explo ):
        ol = list()
        if not self.quest_started:
            sk = self.elements["SHOPKEEPER"]
            myoffer = dialogue.Offer( msg = "{0} is always busy these days. We should get some help, but we're too busy to go looking!".format(sk, sk.subject_pronoun()) ,
             context = context.ContextTag( [context.HELLO] ) ,
             replies = [ dialogue.Reply( "I could do that for you." ,
                    destination = dialogue.Offer( msg = "Really? We need three {0} folks to cover all this work. Let me know if you find anyone.".format(self.STAT_DESC[self.needed_stat]) ,
                     context = context.ContextTag( [context.PERSONAL] ), effect=self.start_quest )) ]
             )
            ol.append( myoffer )
        else:
            myoffer = dialogue.Offer( msg = "Have you found me three {0} folks yet?".format(self.STAT_DESC[self.needed_stat]),
             context = context.ContextTag( [context.HELLO] ) )
            if len( self.employees ) >= 5:
                myoffer.replies.append( dialogue.Reply( "I found everyone you need." ,
                    destination = dialogue.Offer( msg = "Great! With {0}, {1}, and {2} on staff things here will be much easier. Thank you so much.".format(self.employees[2],self.employees[3],self.employees[4]),
                     context = context.ContextTag( [context.PERSONAL] ), effect=self.end_quest, replies=[ dialogue.Reply( "You're welcome." ,
                    destination = dialogue.Cue( context.ContextTag( [context.REWARD] ) ) ) ] ))
                )
            else:
                myoffer.replies.append( dialogue.Reply( "I'm still working on it." ,destination = dialogue.Cue( context.ContextTag( [context.GOODLUCK] ))))
                ol.append( dialogue.Offer( msg = "Good luck with that. I'll be waiting right here... as if I had time to go anywhere else.",
                     context = context.ContextTag( [context.GOODLUCK] ) ) )
            ol.append( myoffer )

        return ol
    def add_this_npc( self, explo ):
        # Add the NPC in the current conversation to the list of employees.
        npc = explo.convo[1]
        self.employees.append( npc )
        if len( self.employees ) >= 5:
            self.subplots["next"].active = True
    ACCEPT_JOB_REPLIES = ( "I could use the extra money. Tell {0} I can start next week.",
        "Do I look like I need part time work? Yeah, I guess I probably do... Tell {0} I will take the job.",
        "Why not? You can tell {0} I will help out.",
        "Alright, I can do that.", "For {0} I would be glad to help out."
        )
    def get_generic_offers( self, npc, explo ):
        ol = list()
        if self.quest_started and npc not in self.employees and npc.get_stat(self.needed_stat) > (12+self.rank//2) and len( self.employees ) < 5:
            qgnpc = self.elements["_NPC"]
            myoffer = dialogue.Offer( msg = "What is it?" ,
             context = context.ContextTag( [context.BRINGMESSAGE,context.QUESTION] ) ,
             replies = [ dialogue.Reply( "{0} is looking for help.".format(qgnpc) ,
                    destination = dialogue.Offer( msg = random.choice(self.ACCEPT_JOB_REPLIES).format(qgnpc.object_pronoun()) ,
                     context = context.ContextTag( [context.PERSONAL] ), effect=self.add_this_npc )) ]
             )
            ol.append( myoffer )
        return ol



