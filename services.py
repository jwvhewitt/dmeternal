import spells
import charsheet
import pygame
import items

GENERAL_STORE = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF,
    items.BOW, items.POLEARM, items.ARROW, items.SHIELD, items.SLING, items.BULLET,
    items.CLOTHES, items.LIGHT_ARMOR, items.HEAVY_ARMOR, items.HAT, items.HELM,
    items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, items.BOOTS,
    items.CLOAK, items.FARMTOOL )

class Shop( object ):
    def __init__( self, ware_types = GENERAL_STORE, allow_misc=True, allow_magic=False, caption="Shop", rank=3, num_items=30 ):
        self.wares = list()
        self.ware_types = ware_types
        self.allow_misc = allow_misc
        self.allow_magic = allow_magic
        self.caption = caption
        self.rank = rank
        self.num_items = num_items
        self.last_updated = -1

    def update_wares( self ):
        # Once a day the wares get updated. Delete some items, make sure that
        # there's at least one item of every ware_type, and then fill up the
        # store to full capacity.
        needed_wares = list( self.ware_types )
        for i in self.wares:
            if i.itemtype in needed_wares:
                needed_wares.remove( i.itemtype )

        for w in needed_wares:
            it = items.choose_item( w, self.rank )
            if it:
                self.wares.append( it )
        while len( self.wares ) < self.num_items:
            it = items.choose_item( None, self.rank )
            if it and not any( i.true_name == it.true_name for i in self.wares ):
                self.wares.append( it )
            elif not it:
                break

        print [ str(w) for w in self.wares ]


    def __call__( self, explo ):
        if explo.camp.day > self.last_updated:
            self.update_wares()
            self.last_updated = explo.camp.day

        charsheets = dict()
        for pc in explo.camp.party:
            charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp )
        psr = charsheet.PartySelectRedrawer( predraw=explo.view, charsheets=charsheets, screen=explo.screen, caption="Who needs to buy something?" )

        rpm = charsheet.RightMenu( explo.screen, predraw=psr, add_desc=False )
        psr.menu = rpm
        for pc in explo.camp.party:
            rpm.add_item( str( pc ), pc )
        rpm.sort()
        rpm.add_alpha_keys()
        rpm.add_item( "Exit", None )
        keep_going = True

        while keep_going:
            pc = rpm.query()

            if pc:
                self.enter_shop( explo, pc )
            else:
                keep_going = False


class Library( object ):
    def __init__( self, spell_list = spells.SPELL_LIST, caption="Library" ):
        self.spell_list = spell_list
        self.caption = caption

    def learn_spell( self, explo, pc ):
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=charsheet.CharacterSheet(pc, screen=explo.screen, camp=explo.camp), screen=explo.screen, predraw=explo.view, caption="Learn New Spell" )

        while keep_going:
            mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )

            for s in self.spell_list:
                if s.can_be_learned( pc ) and s not in pc.techniques:
                    mymenu.add_item( str( s ), s )
            mymenu.sort()
            mymenu.add_alpha_keys()
            mymenu.add_item( "Exit", False )
            myredraw.menu = mymenu
            mymenu.quick_keys[ pygame.K_LEFT ] = -1
            mymenu.quick_keys[ pygame.K_RIGHT ] = 1

            it = mymenu.query()
            if it is -1:
                n = ( explo.camp.party.index(pc) + len( explo.camp.party ) - 1 ) % len( explo.camp.party )
                pc = explo.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=explo.screen, camp=explo.camp)
            elif it is 1:
                n = ( explo.camp.party.index(pc) + 1 ) % len( explo.camp.party )
                pc = explo.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=explo.screen, camp=explo.camp)
            elif it:
                # A spell was selected. Deal with it.
                pc.techniques.append( it )
            else:
                keep_going = False

    def discard_spell( self, explo, pc ):
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=charsheet.CharacterSheet(pc, screen=explo.screen, camp=explo.camp), screen=explo.screen, predraw=explo.view, caption="Discard Known Spell" )

        while keep_going:
            mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )
            for s in pc.techniques:
                if isinstance( s, spells.Spell ):
                    mymenu.add_item( str( s ), s )
            mymenu.sort()
            mymenu.add_alpha_keys()
            mymenu.add_item( "Exit", False )
            myredraw.menu = mymenu
            mymenu.quick_keys[ pygame.K_LEFT ] = -1
            mymenu.quick_keys[ pygame.K_RIGHT ] = 1

            it = mymenu.query()
            if it is -1:
                n = ( explo.camp.party.index(pc) + len( explo.camp.party ) - 1 ) % len( explo.camp.party )
                pc = explo.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=explo.screen, camp=explo.camp)
            elif it is 1:
                n = ( explo.camp.party.index(pc) + 1 ) % len( explo.camp.party )
                pc = explo.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=explo.screen, camp=explo.camp)
            elif it:
                # A spell was selected. Deal with it.
                pc.techniques.remove( it )
            else:
                keep_going = False

    def enter_library( self, explo, pc ):
        """Find out what the PC wants to do."""
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=charsheet.CharacterSheet(pc, screen=explo.screen, camp=explo.camp), screen=explo.screen, predraw=explo.view, caption=self.caption )

        mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )
        mymenu.add_item( "Learn New Spell", self.learn_spell )
        mymenu.add_item( "Discard Known Spell", self.discard_spell )
        mymenu.add_item( "Exit", False )
        mymenu.add_alpha_keys()
        myredraw.menu = mymenu
        mymenu.quick_keys[ pygame.K_LEFT ] = -1
        mymenu.quick_keys[ pygame.K_RIGHT ] = 1

        while keep_going:
            it = mymenu.query()
            if it is -1:
                n = ( explo.camp.party.index(pc) + len( explo.camp.party ) - 1 ) % len( explo.camp.party )
                pc = explo.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=explo.screen, camp=explo.camp)
            elif it is 1:
                n = ( explo.camp.party.index(pc) + 1 ) % len( explo.camp.party )
                pc = explo.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=explo.screen, camp=explo.camp)
            elif it:
                # A method was selected. Deal with it.
                it( explo, pc )
            else:
                keep_going = False


    def __call__( self, explo ):
        charsheets = dict()
        for pc in explo.camp.party:
            charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp )
        psr = charsheet.PartySelectRedrawer( predraw=explo.view, charsheets=charsheets, screen=explo.screen, caption="Who needs to change spells?" )

        rpm = charsheet.RightMenu( explo.screen, predraw=psr, add_desc=False )
        psr.menu = rpm
        for pc in explo.camp.party:
            rpm.add_item( str( pc ), pc )
        rpm.sort()
        rpm.add_alpha_keys()
        rpm.add_item( "Exit", None )
        keep_going = True

        while keep_going:
            pc = rpm.query()

            if pc:
                self.enter_library( explo, pc )
            else:
                keep_going = False

