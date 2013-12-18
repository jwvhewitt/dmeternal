import maps
import pfov
import pygwrap
import pygame
import hotmaps
import charsheet
import items
import dialogue
import animobs

# Commands should be callable objects which take the explorer and return a value.
# If untrue, the command stops.

class MoveTo( object ):
    """A command for moving to a particular point."""
    def __init__( self, scene, pos ):
        """Move the party to pos."""
        self.dest = pos
        self.tries = 300
        self.hmap = hotmaps.PointMap( scene, pos )

    def is_later_model( self, party, pc, npc ):
        return ( pc in party ) and ( npc in party ) \
            and party.index( pc ) < party.index( npc )

    def smart_downhill_dir( self, exp, pc ):
        """Return the best direction for the PC to move in."""
        best_d = None
        heat = self.hmap.map[pc.pos[0]][pc.pos[1]]
        for d in self.hmap.DELTA8:
            x2 = d[0] + pc.pos[0]
            y2 = d[1] + pc.pos[1]
            if exp.scene.on_the_map(x2,y2) and ( self.hmap.map[x2][y2] < heat ):
                target = exp.scene.get_character_at_spot( (x2,y2) )
                if not target:
                    heat = self.hmap.map[x2][y2]
                    best_d = d
                elif ( x2 == self.dest[0] ) and ( y2 == self.dest[1] ):
                    heat = 0
                    best_d = d
                elif self.is_later_model( exp.camp.party, pc, target ):
                    heat = self.hmap.map[x2][y2]
                    best_d = d
        return best_d


    def __call__( self, exp ):
        pc = exp.camp.first_living_pc()
        self.tries += -1
        if (not pc) or ( self.dest == pc.pos ) or ( self.tries < 1 ) or not exp.scene.on_the_map( *self.dest ):
            return False
        else:
            first = True
            keep_going = True
            for pc in exp.camp.party:
                if pc.is_alive() and exp.scene.on_the_map( *pc.pos ):
                    d = self.smart_downhill_dir( exp, pc )
                    if d:
                        p2 = ( pc.pos[0] + d[0] , pc.pos[1] + d[1] )
                        target = exp.scene.get_character_at_spot( p2 )

                        if exp.scene.map[p2[0]][p2[1]].blocks_walking():
                            # There's an obstacle in the way.
                            if first:
                                exp.bump_tile( p2 )
                                keep_going = False
                        elif ( not target ) or self.is_later_model( exp.camp.party, pc, target ):
                            if target:
                                target.pos = pc.pos
                            pc.pos = p2
                            pfov.PCPointOfView( exp.scene, pc.pos[0], pc.pos[1], 10 )
                        elif first:
                            exp.bump_model( target )
                            keep_going = False
                    elif first:
                        keep_going = False
                    first = False
            return keep_going

class InvExchange( object ):
    # The party will exchange inventory with a list.
    def __init__( self, party, ilist, predraw, caption="/ to switch menus" ):
        self.party = party
        self.predraw = predraw
        self.ilist = ilist
        self.caption = caption

    def __call__( self, screen ):
        """Perform the required inventory exchanges."""
        pcn = 0
        use_left_menu = False
        myredraw = charsheet.InvExchangeRedrawer( screen=screen, caption=self.caption, predraw=self.predraw )
        keep_going = True

        while keep_going:
            lmenu = charsheet.LeftMenu( screen )
            rmenu = charsheet.RightMenu( screen )
            pc = self.party[ pcn ]

            myredraw.menu = rmenu
            myredraw.pc = pc
            if use_left_menu:
                myredraw.off_menu = rmenu
            else:
                myredraw.off_menu = lmenu

            lmenu.predraw = myredraw
            lmenu.quick_keys[ pygame.K_LEFT ] = -1
            lmenu.quick_keys[ pygame.K_RIGHT ] = 1
            lmenu.quick_keys[ "/" ] = 2

            rmenu.predraw = myredraw
            rmenu.quick_keys[ pygame.K_LEFT ] = -1
            rmenu.quick_keys[ pygame.K_RIGHT ] = 1
            rmenu.quick_keys[ "/" ] = 2

            for it in pc.inventory:
                lmenu.add_item( str( it ), it )
            for it in self.ilist:
                rmenu.add_item( str( it ), it )
            lmenu.sort()
            rmenu.sort()
            lmenu.add_alpha_keys()
            rmenu.add_alpha_keys()
            lmenu.add_item( "Cancel", False )
            rmenu.add_item( "Cancel", False )

            if use_left_menu:
                it = lmenu.query()
            else:
                it = rmenu.query()

            if it is -1:
                pcn = ( pcn + len( self.party ) - 1 ) % len( self.party )
            elif it is 1:
                pcn = ( pcn + 1 ) % len( self.party )
            elif it is 2:
                use_left_menu = not use_left_menu
            elif it:
                # An item was selected. Transfer.
                if use_left_menu:
                    pc.inventory.unequip( it )
                    if not it.equipped:
                        pc.inventory.remove( it )
                        self.ilist.append( it )
                else:
                    self.ilist.remove( it )
                    pc.inventory.append( it )
            else:
                keep_going = False
        return self.ilist


class Explorer( object ):
    # The object which is exploration of a scene. OO just got existential.

    def __init__( self, screen, camp, scene ):
        self.screen = screen
        self.camp = camp
        self.scene = scene
        self.view = maps.SceneView( scene )

        # Update the view of all party members.
        for pc in camp.party:
            x,y = pc.pos
            pfov.PCPointOfView( scene, x, y, 10 )

        # Focus on the first PC.
        x,y = camp.first_living_pc().pos
        self.view.focus( screen, x, y )

    def bump_tile( self, pos ):
        pass

    def bump_model( self, target ):
        # Do the animation first.
        pc = self.camp.party_spokesperson()

        anims = [ animobs.SpeakHello(pos=pc.pos), animobs.SpeakHello(pos=target.pos)]
        animobs.handle_anim_sequence( self.screen, self.view, anims )

        offers = [ dialogue.O1, dialogue.O2 ]
        convo = dialogue.build_conversation( dialogue.CUE_HELLO , offers )
        dialogue.converse( self, pc, target, convo )

    def pick_up( self, loc ):
        """Party will pick up items at this location."""
        ilist = []
        for it in self.scene.contents[:]:
            if isinstance( it , items.Item ) and ( it.pos == loc ):
                self.scene.contents.remove( it )
                ilist.append( it )
        if ilist:
            ie = InvExchange( self.camp.party, ilist, self.view )
            ilist = ie( self.screen )
            for it in ilist:
                it.pos = loc
                self.scene.contents.append( it )
            self.view.regenerate_avatars( self.camp.party )

    def equip_item( self, it, pc, redraw ):
        pc.inventory.equip( it )

    def unequip_item( self, it, pc, redraw ):
        pc.inventory.unequip( it )

    def drop_item( self, it, pc, redraw ):
        pc.inventory.unequip( it )
        if not it.equipped:
            pc.inventory.remove( it )
            it.pos = pc.pos
            self.scene.contents.append( it )

    def trade_item( self, it, pc, redraw ):
        """Trade this item to another character."""
        mymenu = charsheet.RightMenu( self.screen, predraw = redraw )
        for opc in self.camp.party:
            if opc != pc:
                mymenu.add_item( str( opc ) , opc )
        mymenu.add_item( "Cancel" , False )
        mymenu.add_alpha_keys()

        opc = mymenu.query()
        if opc:
            pc.inventory.unequip( it )
            if not it.equipped:
                pc.inventory.remove( it )
                opc.inventory.append( it )


    def equip_or_whatevs( self, it, pc, myredraw ):
        """Equip, trade, drop, or whatever this item."""
        mymenu = charsheet.RightMenu( self.screen, predraw = myredraw )
        if it.equipped:
            mymenu.add_item( "Unequip Item", self.unequip_item )
        elif pc.can_equip( it ):
            mymenu.add_item( "Equip Item", self.equip_item )
        mymenu.add_item( "Trade Item", self.trade_item )
        mymenu.add_item( "Drop Item", self.drop_item )
        mymenu.add_item( "Exit", False )
        mymenu.add_alpha_keys()

        n = mymenu.query()

        if n:
            n( it, pc, myredraw )
            myredraw.csheet.regenerate_avatar()
            self.view.regenerate_avatars( self.camp.party )


    def view_party( self, n, can_switch=True ):
        if n >= len( self.camp.party ):
            n = 0
        pc = self.camp.party[ n ]
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=charsheet.CharacterSheet(pc, screen=self.screen), screen=self.screen, predraw=self.view, caption="View Party" )

        while keep_going:
            mymenu = charsheet.RightMenu( self.screen, predraw = myredraw )
            for i in pc.inventory:
                if i.equipped:
                    mymenu.add_item( "*" + str( i ) , i )
                else:
                    mymenu.add_item( str( i ) , i )
            mymenu.sort()
            mymenu.add_alpha_keys()
            mymenu.add_item( "Exit", False )
            myredraw.menu = mymenu
            if can_switch:
                mymenu.quick_keys[ pygame.K_LEFT ] = -1
                mymenu.quick_keys[ pygame.K_RIGHT ] = 1

            it = mymenu.query()
            if it is -1:
                n = ( n + len( self.camp.party ) - 1 ) % len( self.camp.party )
                pc = self.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=self.screen)
            elif it is 1:
                n = ( n + 1 ) % len( self.camp.party )
                pc = self.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=self.screen)

            elif it:
                # An item was selected. Deal with it.
                self.equip_or_whatevs( it, pc, myredraw )

            else:
                keep_going = False

    def go( self ):
        keep_going = True
        self.order = None

        # Do one view first, just to prep the model map and mouse tile.
        self.view( self.screen )
        pygame.display.flip()

        while keep_going:
            # Get input and process it.
            gdi = pygwrap.wait_event()

            if gdi.type == pygwrap.TIMEREVENT:
                self.view( self.screen )
                pygame.display.flip()

                if self.order:
                    if not self.order( self ):
                        self.order = None


            elif not self.order:
                # Set the mouse cursor on the map.
                self.view.overlays.clear()
                self.view.overlays[ self.view.mouse_tile ] = maps.OVERLAY_CURSOR

                if gdi.type == pygame.KEYDOWN:
                    if gdi.unicode == u"1":
                        self.view_party(0)
                    if gdi.unicode == u"2":
                        self.view_party(1)
                    if gdi.unicode == u"3":
                        self.view_party(2)
                    if gdi.unicode == u"4":
                        self.view_party(3)
                    elif gdi.unicode == u"Q":
                        keep_going = False
                elif gdi.type == pygame.QUIT:
                    keep_going = False
                elif gdi.type == pygame.MOUSEBUTTONUP:
                    if gdi.button == 1:
                        # Left mouse button.
                        if self.view.mouse_tile != self.camp.first_living_pc().pos:
                            self.order = MoveTo( self.scene, self.view.mouse_tile )
                            self.view.overlays.clear()
                        else:
                            self.pick_up( self.view.mouse_tile )




