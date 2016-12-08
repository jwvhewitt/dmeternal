from plots import Plot,PlotError,PlotState
from .. import context
from .. import items
from .. import maps
from .. import waypoints
from .. import monsters
from .. import dialogue
from .. import services
from .. import teams
from .. import characters
import random
from .. import randmaps
from .. import effects
from .. import stats
from .. import animobs

#  ***************************
#  ***   SPECIAL_FEATURE   ***
#  ***************************
#
# One special feature gets placed in most scenes. It's not necessarily an
# encounter, not necessarily a treasure... just something to make life more
# interesting.

class Barracks( Plot ):
    # Find where the enemy sleeps.
    LABEL = "SPECIAL_FEATURE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist, be a dungeon, and have a faction."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags
                and pstate.elements["LOCALE"].fac )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        room = randmaps.rooms.SharpRoom(random.randint(9,15),random.randint(9,15))
        room.DECORATE = randmaps.decor.BedroomDec()
        room.contents.append( teams.Team(default_reaction=0, rank=self.rank, 
          strength=120, habitat=scene.get_encounter_request(), fac=scene.fac ) )
        for t in range( random.randint(1,3) ):
            mychest = waypoints.SmallChest()
            mychest.stock(self.rank)
            room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

class BoringLevel( Plot ):
    # This level gets a boring decoration of some type.
    LABEL = "SPECIAL_FEATURE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.contents.append( random.choice( self.DECOR_OPTIONS ) )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True
    DECOR_OPTIONS = ( maps.SKULL,maps.BONE,maps.KEG,maps.PILED_GOODS,
        maps.LIGHT_STAND,maps.PUDDLE,maps.ROCKS )

class CheaterChest( Plot ):
    LABEL = "SPECIAL_FEATURE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.DECORATE = randmaps.decor.MonsterDec()
        mychest = waypoints.LargeChest()
        mychest.TILE = maps.Tile( None, None, maps.LARGE_CHEST_OPEN )
        mychest.gold = 1
        room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True


class DungeonPoem( Plot ):
    LABEL = "SPECIAL_FEATURE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        mysign = waypoints.Signpost()
        mysign.desc = '"Dark and foreboding, the final rest of many: eaten by a grue."'
        room.contents.append( mysign )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True


class FountainOfDeath( Plot ):
    LABEL = "SPECIAL_FEATURE"
    active = True
    scope = "LOCALE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon of > rank 1."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags
                and pstate.rank > 1 )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myfountain = waypoints.Fountain( plot_locked = True )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        self.register_element( "FOUNTAIN", myfountain, dident="_ROOM" )
        return True
    def FOUNTAIN_menu( self, thingmenu ):
        thingmenu.desc = "{0} Do you want to take a drink?".format( thingmenu.desc )
        thingmenu.add_item( "Take a drink.", self.use_fountain )
        thingmenu.add_item( "Leave it alone.", None )
    FOUNTAIN_FX = effects.HealthDamage( att_dice=(1,8,0), element=stats.RESIST_POISON,
        anim=animobs.PoisonCloud )
    def use_fountain( self, explo ):
        fountain = self.elements[ "FOUNTAIN" ]
        explo.alert( "The water is poison!" )
        targets = list()
        for pc in explo.camp.party:
            if pc.is_alright():
                targets.append( pc.pos )
        explo.invoke_effect( self.FOUNTAIN_FX, None, targets )
        fountain.plot_locked = False
        fountain.desc = "You don't want to try drinking from this fountain again."
        self.active = False

class FountainOfHealing( Plot ):
    LABEL = "SPECIAL_FEATURE"
    active = True
    scope = "LOCALE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM(tags=(context.GOAL,))
        myfountain = waypoints.HealingFountain( plot_locked = True )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        self.register_element( "FOUNTAIN", myfountain, dident="_ROOM" )
        return True
    def FOUNTAIN_menu( self, thingmenu ):
        thingmenu.desc = "{0} Do you want to take a drink?".format( thingmenu.desc )
        thingmenu.add_item( "Take a drink.", self.use_fountain )
        thingmenu.add_item( "Leave it alone.", None )
    def use_fountain( self, explo ):
        fountain = self.elements[ "FOUNTAIN" ]
        explo.alert( "The refreshing water heals your wounds." )
        fountain.unlocked_use( explo )
        fountain.plot_locked = False
        self.active = False

class FountainOfDoubt( Plot ):
    LABEL = "SPECIAL_FEATURE"
    active = True
    scope = "LOCALE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myfountain = waypoints.Fountain( plot_locked = True )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        self.register_element( "FOUNTAIN", myfountain, dident="_ROOM" )
        return True
    def FOUNTAIN_menu( self, thingmenu ):
        thingmenu.desc = "{0} Do you want to take a drink?".format( thingmenu.desc )
        thingmenu.add_item( "Take a drink.", self.use_fountain )
        thingmenu.add_item( "Leave it alone.", None )
    def use_fountain( self, explo ):
        fountain = self.elements[ "FOUNTAIN" ]
        explo.alert( "This fountain doesn't seem to do anything. Perhaps it's the Fountain of Doubt." )
        fountain.plot_locked = False
        self.active = False

class LibraryOfTheDead( Plot ):
    LABEL = "SPECIAL_FEATURE"
    UNIQUE = True
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist, to be tunnels or building, and to include LUNAR or UNDEAD."""
        return ( pstate.elements.get("LOCALE")
         and pstate.elements["LOCALE"].biome in (context.HAB_BUILDING,context.HAB_TUNNELS)
         and ( context.DES_LUNAR in pstate.elements["LOCALE"].desctags
         or context.GEN_UNDEAD in pstate.elements["LOCALE"].desctags ) )
    GOALS = ("power","gold","knowledge")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        room = randmaps.rooms.SharpRoom()
        room.DECORATE = randmaps.decor.LibraryDec(win=None)
        room.contents.append( waypoints.Bookshelf() )
        # Create a chest, and stock it with magical goodies.
        mychest = waypoints.LargeChest()
        mychest.stock(self.rank,item_types=(items.SCROLL,items.POTION))
        room.contents.append( mychest )
        for t in range( random.randint(5,8) ):
            myitem = items.generate_scroll( self.rank + 1 )
            if myitem:
                myitem.identified = True
                mychest.contents.append( myitem )
        # Create a team for our undead spellcaster.
        myhabitat = {context.GEN_UNDEAD: True }
        myteam = self.register_element( "TEAM", teams.Team(default_reaction=-25, rank=self.rank, 
          strength=0, habitat=myhabitat ) )
        room.contents.append( myteam )
        mh2 = myhabitat.copy()
        mh2[(context.MTY_MAGE,context.MTY_PRIEST)] = True
        btype = monsters.choose_monster_type(self.rank-1,self.rank+4,mh2)
        if btype:
            boss = monsters.generate_boss( btype, self.rank+4, team=myteam )
            myitem = items.generate_special_item( self.rank+2, items.WAND )
            if myitem:
                boss.contents.append( myitem )
            self.register_element( "_ROOM", room, dident="LOCALE" )
            self.register_element( "BOSS", boss, "_ROOM" )

            # Record the one thing this boss cares about.
            self.boss_goal = random.choice( self.GOALS )
            self.boss_shop = self.register_element( "SHOPSERVICE",
              services.Shop( services.MAGIC_STORE, rank=self.rank+5, allow_misc=False, num_items=25, turnover=5, npc=boss ) )
            self.shop_open = False
        return btype
    def get_dialogue_grammar( self, npc, explo ):
        mygram = {
            "[RUMOUR]": ["[rumourleadin] in life, {0} only cared about {1}.".format( self.elements["BOSS"], self.boss_goal )],
        }
        return mygram
    def BOSS_DEATH( self, explo ):
        self.active = False
    REWARDS = { "power": (stats.MAGIC_ATTACK,5), "gold": (stats.LOOTING,10),
        "knowledge": (stats.INTELLIGENCE,1) }
    def answer_correctly( self, explo ):
        self.elements["TEAM"].charm_roll = 999
        self.shop_open = True
        r_stat,r_amount = self.REWARDS.get( self.boss_goal, (stats.TOUGHNESS,1) )
        ao = list()
        for pc in explo.camp.party:
            pc.statline[r_stat] = pc.statline.get(r_stat,0) + r_amount
            ao.append( animobs.PurpleSparkle( pos = pc.pos ) )
        animobs.handle_anim_sequence( explo.screen, explo.view, ao )
    def answer_incorrectly( self, explo ):
        self.elements["TEAM"].charm_roll = -999
    def BOSS_offers( self, explo ):
        # Return list of boss offers.
        ol = list()
        if self.shop_open:
            # If you make friends with this boss, you can buy magic here.
            ol.append( dialogue.Offer( "[SHOP_MAGIC]" ,
             context = context.ContextTag([context.SHOP,context.GENERALSTORE]), effect=self.boss_shop ) )
        else:
            # If you haven't yet made friends, things could be tricky...
            challenge1 = dialogue.Offer( "Who dares to disturb my eternal studies? Speak, mortals, and tell me what you expect to find!", context = context.ContextTag([context.THREATEN,] ))
            challenge2 = dialogue.Offer( "Tell me, mortals... what is it that you seek in life?", context = context.ContextTag([context.HELLO,] ))
            right_answer = dialogue.Offer( "Then that is what you shall find!", effect = self.answer_correctly )
            wrong_answer = dialogue.Offer( "Fools! Your inevitable death shall be meaningless!", effect = self.answer_incorrectly )
            for t,goal in enumerate( self.GOALS ):
                myreply = dialogue.Reply( "We seek {}.".format( goal ) )
                if goal is self.boss_goal:
                    # Congratulations, you've figured it out.
                    myreply.destination = right_answer
                else:
                    # This is the wrong answer, by undead standards.
                    myreply.destination = wrong_answer
                challenge1.replies.append( myreply )
                challenge2.replies.append( myreply )
            ol += [challenge1,challenge2]
        return ol

class NeutralTraders( Plot ):
    LABEL = "SPECIAL_FEATURE"
    active = True
    scope = "LOCALE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        # Add a group of humanoids, neutral reaction score.
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myhabitat={ context.MTY_HUMANOID: context.PRESENT }
        myteam = teams.Team(default_reaction=0, rank=self.rank, 
          strength=random.randint(90,120), habitat=myhabitat )
        room.contents.append( myteam )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        myhabitat[ context.MTY_LEADER ] = context.MAYBE
        btype = monsters.choose_monster_type(self.rank-1,self.rank+2,myhabitat)
        if btype:
            boss = monsters.generate_boss( btype, self.rank-1, team=myteam )
            myteam.boss = boss
            self.shop = self.register_element( "SHOPSERVICE", services.Shop( rank=self.rank+3, num_items=15, npc=boss ) )
            self.first_time = True
            self.register_element( "BOSS", boss, "_ROOM" )
        return btype
    def SpeakFirstTime( self, explo ):
        self.first_time = False
    def BOSS_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "[SHOP_GENERAL]" ,
         context = context.ContextTag([context.SHOP,context.GENERALSTORE]), effect=self.shop ) )
        if self.first_time:
            ol.append( dialogue.Offer( "I am a wandering trader, interested in both buying and selling. This is a dangerous place. You could use a good [weapon].",
             context = context.ContextTag([context.HELLO,context.SHOP,context.GENERALSTORE]), effect=self.SpeakFirstTime ) )
        return ol

class RedHerringsChest( Plot ):
    # Just an unguarded chest in the dungeon... to make the players worry.
    LABEL = "SPECIAL_FEATURE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        mychest = waypoints.SmallChest()
        mychest.stock(self.rank)
        room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

class RivalParty( Plot ):
    LABEL = "SPECIAL_FEATURE"
    active = True
    scope = "LOCALE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE")
    FIGHTERS = ( characters.Warrior, characters.Samurai, characters.Knight, characters.Monk, None )
    THIEVES = ( characters.Thief, characters.Ninja, characters.Bard, characters.Ranger, None )
    PRIESTS = ( characters.Priest, characters.Druid, None )
    MAGES = ( characters.Mage, characters.Necromancer, None )
    LANDMARKS = ( waypoints.Fountain,waypoints.PowerCrystal,waypoints.Campsite )
    def custom_init( self, nart ):
        # Add a group of humanoids, neutral reaction score.
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myteam = self.register_element( "TEAM", teams.Team( default_reaction=0, strength=0 ) )
        room.contents.append( myteam )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        p1 = self.register_element( "NPC1", monsters.generate_npc(team=myteam,job=random.choice( self.FIGHTERS ),upgrade=True,rank=self.rank), dident="_ROOM")
        p2 = self.register_element( "NPC2", monsters.generate_npc(team=myteam,job=random.choice( self.THIEVES ),upgrade=True,rank=self.rank), dident="_ROOM")
        p3 = self.register_element( "NPC3", monsters.generate_npc(team=myteam,job=random.choice( self.PRIESTS ),upgrade=True,rank=self.rank), dident="_ROOM")
        p4 = self.register_element( "NPC4", monsters.generate_npc(team=myteam,job=random.choice( self.MAGES ),upgrade=True,rank=self.rank), dident="_ROOM")
        self.add_sub_plot( nart, "RESOURCE_NPCCONVO", PlotState( elements={"NPC":random.choice((p1,p2,p3,p4))} ).based_on( self ) )
        room.contents.append( random.choice( self.LANDMARKS )() )
        return True
    def do_truce( self, explo ):
        self.elements["TEAM"].charm_roll = 999
    def get_generic_offers( self, npc, explo ):
        ol = list()
        if npc.team is self.elements["TEAM"]:
            ol.append( dialogue.Offer( msg = "That is a relief. This place is quite dangerous, you know.",
             context = context.ContextTag( [context.TRUCE] ), effect=self.do_truce)
            )
            ol.append( dialogue.Offer( msg = "[ATTACK]",
             context = context.ContextTag( [context.ATTACK] ))
            )
        return ol


class WildernessInn( Plot ):
    LABEL = "SPECIAL_FEATURE"
    active = True
    scope = "BUILDING_INT"
    NAME_PATTERNS = ( "{0}'s Inn", "The {1} and {2}" )
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be wilderness."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_WILDERNESS in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        exterior = randmaps.rooms.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.SMALL_WINDOW
        exterior.special_c[ "sign1" ] = maps.DRINK_SIGN
        self.register_element( "_EXTERIOR", exterior, dident="LOCALE" )
        interior = maps.Scene( 50,50, sprites={maps.SPRITE_WALL: "terrain_wall_wood.png",maps.SPRITE_FLOOR: "terrain_floor_wood.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = randmaps.BuildingScene( interior )
        gate_1 = waypoints.GateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = self.elements.get( "LOCALE" )
        gate_2.otherside = gate_1
        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="LOCALE" )
        exterior.special_c[ "door" ] = gate_1
        int_mainroom = randmaps.rooms.SharpRoom( random.randint(12,20), random.randint(12,20),
         tags=(context.CIVILIZED,context.ROOM_PUBLIC), anchor=randmaps.anchors.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        int_mainroom.contents.append( waypoints.Bookshelf() )
        int_mainroom.contents.append( maps.FIREPLACE )
        gate_2.anchor = randmaps.anchors.south
        int_mainroom.DECORATE = randmaps.decor.TavernDec(win=maps.SMALL_WINDOW)
        npc = monsters.generate_npc(job=monsters.base.Innkeeper)
        npc.tags.append( context.CHAR_INNKEEPER )
        interior.name = random.choice( self.NAME_PATTERNS ).format( npc, random.choice(monsters.MONSTER_LIST).name, random.choice(monsters.MONSTER_LIST).name )
        gate_1.mini_map_label = "Traveler's Inn"
        int_mainroom.contents.append( npc )
        self.register_element( "SHOPKEEPER", npc )
        int_mainroom.contents.append( maps.TABLE )
        int_mainroom.contents.append( maps.TABLE )
        int_mainroom.contents.append( maps.TABLE )
        # Add at least one visitor.
        npc = self.register_element( "NPC", monsters.generate_npc( rank=self.rank+2,upgrade=True ) )
        self.add_sub_plot( nart, "RESOURCE_NPCCONVO" )
        int_mainroom.contents.append( npc )

        int_bedroom = randmaps.rooms.SharpRoom( tags=(context.CIVILIZED,), parent=interior )
        int_bedroom.contents.append( maps.LIGHT_STAND )
        int_bedroom.DECORATE = randmaps.decor.BedroomDec()
        self.shop = services.Inn()
        return True
    def SHOPKEEPER_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "[SERVICE_INN]" ,
         context = context.ContextTag([context.SERVICE,context.INN]), effect=self.shop ) )
        return ol


