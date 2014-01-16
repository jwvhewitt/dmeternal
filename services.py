import spells
import charsheet
import pygame

class Shop( object ):
    def __init__( self, ware_types = (), allow_misc=True, allow_magic=False, caption="Shop" ):
        self.wares = list()
        self.ware_types = ware_types
        self.allow_misc = allow_misc
        self.allow_magic = allow_magic
        self.caption = caption


    def __call__( self, explo ):
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

