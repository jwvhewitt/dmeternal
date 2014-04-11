import maps
import pfov
import pygwrap
import pygame
import hotmaps
import charsheet
import items
import dialogue
import animobs
import characters
import random
import teams
import combat
import stats
import services
import image
import rpgmenu
import spells


# Commands should be callable objects which take the explorer and return a value.
# If untrue, the command stops.

class MoveTo( object ):
    """A command for moving to a particular point."""
    def __init__( self, explo, pos ):
        """Move the party to pos."""
        self.dest = pos
        self.tries = 300
        pcpos = explo.camp.first_living_pc().pos
        if explo.scene.distance( pcpos, pos ) < 30:
            limit = pygame.Rect(0,0,50,50)
            limit.center = ( (pos[0]+pcpos[0])//2, (pos[1]+pcpos[1])//2 )
            self.hmap = hotmaps.PointMap( explo.scene, pos, limits=limit )
        else:
            self.hmap = hotmaps.PointMap( explo.scene, pos )

    def is_later_model( self, party, pc, npc ):
        return ( pc in party ) and ( npc in party ) \
            and party.index( pc ) < party.index( npc )

    def smart_downhill_dir( self, exp, pc ):
        """Return the best direction for the PC to move in."""
        best_d = None
        random.shuffle( self.hmap.DELTA8 )
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
                if pc.is_alright() and exp.scene.on_the_map( *pc.pos ):
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
                        elif first:
                            exp.bump_model( target )
                            keep_going = False
                    elif first:
                        keep_going = False
                    first = False
            # Now that all of the pcs have moved, check the tiles_in_sight for
            # hidden models.
            exp.scene.update_party_position( exp.camp.party )
            awareness = exp.camp.party_stat( stats.AWARENESS, stats.INTELLIGENCE )
            for m in exp.scene.contents:
                if isinstance( m, characters.Character ) and m.hidden and m.pos in exp.scene.in_sight and \
                  awareness > m.get_stat( stats.STEALTH ) + m.get_stat_bonus(stats.REFLEXES):
                    m.hidden = False

            return keep_going

class InvExchange( object ):
    # The party will exchange inventory with a list.
    def __init__( self, party, ilist, predraw, caption="/ to switch menus" ):
        self.party = []
        for p in party:
            if p.is_alright():
                self.party.append( p )
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

            for it in pc.contents:
                if it.equipped:
                    lmenu.add_item( "*"+str( it ), it )
                elif not pc.can_equip( it ):
                    lmenu.add_item( "#"+str( it ), it )
                else:
                    lmenu.add_item( str( it ), it )
            for it in self.ilist:
                if not pc.can_equip( it ):
                    rmenu.add_item( "#"+str( it ), it )
                else:
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
                    pc.contents.unequip( it )
                    if not it.equipped:
                        pc.contents.remove( it )
                        self.ilist.append( it )
                elif pc.can_take_item( it ) and pc.is_alright():
                    self.ilist.remove( it )
                    pc.contents.append( it )
            else:
                keep_going = False
        return self.ilist

class WorldExplorer( object ):
    def __init__( self, explo ):
        self.explo = explo
        self.w = explo.camp.current_world()
        self.view()

    def draw( self, screen ):
        self.explo.view( screen )
        pygwrap.map_border.render( screen, self.dest )
        self.pic.render( screen, self.dest, 0 )
        pos = self.menu.items[ self.menu.selected_item ].value.world_map_pos.coords
        if pos and ( self.explo.view.phase // 5 ) % 2 == 0:
            self.quill.render( screen, ( self.dest.x + pos[0] * 32 + 16, self.dest.y + pos[1] * 32 ) )

    def view( self ):
        self.pic = image.Image( frame_width = 480, frame_height = 480 )
        self.quill = image.Image( "sys_quill.png", 21, 18 )
        mmbits = image.Image( "sys_worldmapbits.png", 32, 32 )
        self.dest = self.pic.bitmap.get_rect( center=(self.explo.screen.get_width()//2-100, self.explo.screen.get_height()//2 ) )
        self.menu = rpgmenu.Menu(self.explo.screen,self.explo.screen.get_width()//2+215, self.explo.screen.get_height()//2-200, 150, 400, predraw=self.draw )

        for t in self.w.contents:
            if hasattr( t, "world_map_pos" ) and t.world_map_pos.visible:
                self.menu.add_item( t.world_map_pos.name, t )
                mmbits.render( self.pic.bitmap, (t.world_map_pos.coords[0]*32,t.world_map_pos.coords[1]*32), t.world_map_pos.icon )

        self.menu.sort()
        dest = self.menu.query()
        if dest:
            pass


class MiniMap( object ):
    def __init__( self, explo ):
        self.explo = explo
        self.view()

    def draw( self, screen ):
        self.explo.view( screen )
        pygwrap.map_border.render( screen, self.dest )
        self.pic.render( screen, self.dest, 0 )
        pos = self.menu.items[ self.menu.selected_item ].value
        if pos and ( self.explo.view.phase // 5 ) % 2 == 0:
            self.quill.render( screen, ( self.dest.x + pos[0] * 4 + 2, self.dest.y + pos[1] * 4 - 16 ) )

    def view( self ):
        self.pic = image.Image( frame_width = self.explo.scene.width * 4, frame_height = self.explo.scene.height * 4 )
        self.quill = image.Image( "sys_quill.png", 21, 18 )
        mmbits = image.Image( "sys_mapbits.png", 4, 4 )
        for x in range( self.explo.scene.width ):
            for y in range( self.explo.scene.height ):
                if self.explo.scene.map[x][y].visible:
                    t = 0
                    if self.explo.scene.map[x][y].wall:
                        t = 2
                    if self.explo.scene.map[x][y].blocks_walking():
                        t += 1
                    mmbits.render( self.pic.bitmap, (x*4,y*4), t )
        self.dest = self.pic.bitmap.get_rect( center=(self.explo.screen.get_width()//2-100, self.explo.screen.get_height()//2 ) )
        self.menu = rpgmenu.Menu(self.explo.screen,self.explo.screen.get_width()//2+215, self.explo.screen.get_height()//2-200, 150, 400, predraw=self.draw )

        self.menu.add_item( "Party", self.explo.camp.first_living_pc().pos )
        for t in self.explo.scene.contents:
            if hasattr( t, "mini_map_label" ) and self.explo.scene.get_visible( *t.pos ):
                self.menu.add_item( t.mini_map_label, t.pos )
        self.menu.sort()
        if hasattr( self.explo.scene, "world_map_pos" ):
            self.menu.add_item( "[World Map]", 0 )

        pos = self.menu.query()
        if pos:
            self.explo.view.focus( self.explo.screen, *pos )
        elif pos is 0:
            WorldExplorer( self.explo )

# Rubicon Hiscock had her entire body tattooed by a cloister of Gothic monks, and in this way she became illuminated.

class Explorer( object ):
    # The object which is exploration of a scene. OO just got existential.

    def __init__( self, screen, camp ):
        self.screen = screen
        self.camp = camp
        self.scene = camp.scene
        self.view = maps.SceneView( camp.scene )
        self.time = 0

        self.shop = services.Shop()

        # Update the view of all party members.
        for pc in camp.party:
            if pc.pos and pc.is_alright():
                x,y = pc.pos
                pfov.PCPointOfView( camp.scene, x, y, 15 )

        # Hide any monsters who can manage it.
        for m in self.scene.contents:
            if isinstance( m, characters.Character ) and m.can_use_stealth() and m.is_hostile( camp ):
                m.hidden = True

        # Focus on the first PC.
        x,y = camp.first_living_pc().pos
        self.view.focus( screen, x, y )

    def field_camp( self ):
        """The party is going camping. Yahoo!"""
        self.alert( "You camp down to take a short rest..." )
        awareness = min( self.camp.party_stat( stats.AWARENESS, stats.INTELLIGENCE ), 75 ) + 15
        if random.randint(1,100) <= awareness:
            self.camp.rest( 0.5 )
            self.alert( "...and wake up perfectly refreshed." )
        elif random.randint(1,3)==2 and self.camp.gold > random.randint( 1500,10000 ):
            lose = max( self.camp.gold // 2, 1 )
            self.camp.gold -= lose
            self.camp.rest( 0.5 )
            self.alert( "...but when you wake up, {0}gp is missing!".format( lose ) )
        else:
            pc = self.camp.first_living_pc()
            aoe = list()
            for x in range( pc.pos[0]-3, pc.pos[0]+4 ):
                for y in range( pc.pos[1]-3, pc.pos[1]+4 ):
                    if self.scene.on_the_map(x,y) and not self.scene.map[x][y].blocks_walking() and not self.scene.get_character_at_spot((x,y)):
                        aoe.append( (x,y) )
            team = teams.Team(default_reaction=-999,rank=(self.scene.rank + self.camp.party_rank() )//2, strength=random.randint(40,65), habitat=self.scene.get_encounter_request())
            mons = team.build_encounter( self.scene )
            for m in mons:
                if aoe:
                    p = random.choice( aoe )
                    aoe.remove( p )
                    m.place( self.scene, p )
                else:
                    break
            self.alert( "...and get woken up by monsters!" )
            self.camp.activate_monster( mons[0] )


    def probe( self, target ):
        csheet = charsheet.CharacterSheet( target, screen=self.screen )
        myredraw = charsheet.CharacterViewRedrawer( csheet=csheet, screen=self.screen, caption="Probe", predraw=self.view)
        mymenu = charsheet.RightMenu( self.screen, predraw=myredraw )
        mymenu.add_item( "Close" , -1 )
        mymenu.query()

    def invoke_effect( self, effect, originator, area_of_effect, opening_anim = None, delay_point=None ):
        all_anims = list()
        if opening_anim:
            all_anims.append( opening_anim )
            anims = opening_anim.children
        else:
            anims = all_anims
        delay = 1
        for p in area_of_effect:
            if delay_point:
                delay = self.scene.distance( p, delay_point ) * 2 + 1
            effect( self.camp, originator, p, anims, delay )
        animobs.handle_anim_sequence( self.screen, self.view, all_anims )

        # Remove dead models from the map, and handle probes.
        for m in self.scene.contents[:]:
            if hasattr( m, "probe_me" ) and m.probe_me:
                self.probe( m )
                m.probe_me = False
            if isinstance( m, characters.Character ) and not m.is_alright():
                self.scene.contents.remove( m )
                # Drop all held items.
                for i in m.contents[:]:
                    if hasattr( i, "place" ):
                        m.contents.remove(i)
                        i.equipped = False
                        i.place( self.scene, m.pos )

    def invoke_technique( self, tech, originator, area_of_effect, opening_anim = None, delay_point=None ):
        if self.camp.fight and self.camp.fight.cstat[originator].silent and isinstance( tech, spells.Spell ):
            anims = [ animobs.SpeakSilence(originator.pos), ]
            animobs.handle_anim_sequence( self.screen, self.view, anims )
        else:
            self.invoke_effect( tech.fx, originator, area_of_effect, opening_anim, delay_point )
        tech.pay_invocation_price( originator )

    SELECT_AREA_CAPTION_ZONE = pygame.Rect( 32, 32, 300, 15 )
    def select_area( self, origin, aoegen, caption = None ):
        # Start by determining the possible target tiles.
        legal_tiles = aoegen.get_targets( self.camp, origin )
        target = None
        aoe = set()

        # Keep processing until a target is selected.
        while not target:
            # Get input and process it.
            gdi = pygwrap.wait_event()

            if gdi.type == pygwrap.TIMEREVENT:
                # Set the mouse cursor on the map.
                self.view.overlays.clear()
                self.view.overlays[ origin ] = maps.OVERLAY_CURRENTCHARA
                self.view.overlays[ self.view.mouse_tile ] = maps.OVERLAY_CURSOR
                if self.view.mouse_tile in legal_tiles:
                    aoe = aoegen.get_area( self.camp, origin, self.view.mouse_tile )
                    for p in aoe:
                        self.view.overlays[ p ] = maps.OVERLAY_AOE

                self.view( self.screen )
                if caption:
                    pygwrap.default_border.render( self.screen, self.SELECT_AREA_CAPTION_ZONE )
                    pygwrap.draw_text( self.screen, pygwrap.SMALLFONT, caption, self.SELECT_AREA_CAPTION_ZONE )

                pygame.display.flip()

            elif gdi.type == pygame.QUIT:
                self.no_quit = False
                break
            elif gdi.type == pygame.MOUSEBUTTONUP:
                if gdi.button == 1 and self.view.mouse_tile in legal_tiles:
                    target = self.view.mouse_tile
                else:
                    break
        self.view.overlays.clear()
        return target


    def pc_use_technique( self, chara, tech, aoegen ):
        """Let chara invoke tech, selecting area of effect, return True if not cancelled."""
        if aoegen.AUTOMATIC:
            # This is easy.
            tiles = aoegen.get_area( self.camp, chara.pos, None )
            target = None
        else:
            target = self.select_area( chara.pos, aoegen, caption = str(tech) )
            if target:
                tiles = aoegen.get_area( self.camp, chara.pos, target )
            else:
                tiles = None

        if tiles:
            if target and tech.shot_anim:
                shot = tech.shot_anim( chara.pos, target )
            else:
                shot = None
            if aoegen.delay_from < 0:
                delay_point = chara.pos
            elif aoegen.delay_from > 0 and target:
                delay_point = target
            else:
                delay_point = None
            self.invoke_technique( tech, chara, tiles, opening_anim = shot, delay_point = delay_point )
            return True
        else:
            return False


    def invoke_enchantments( self, chara ):
        """If this character has any effect enchantments, handle them."""
        aoe = (chara.pos,)
        for enc in chara.condition[:]:
            if enc.FX:
                self.invoke_effect( enc.FX, chara, aoe )
                if not chara.is_alright():
                    break
                if enc.MAX_USES:
                    enc.uses += 1
                    if enc.uses >= enc.MAX_USES:
                        chara.condition.remove( enc )

    def update_enchantments( self ):
        for c in self.scene.contents:
            if hasattr( c, "condition" ) and c.condition:
                self.invoke_enchantments( c )

    def alert( self, txt ):
        mydest = pygame.Rect( self.screen.get_width() // 2 - 200, self.screen.get_height()//2 - 100, 400, 200 )
        mytext = pygwrap.render_text( pygwrap.SMALLFONT, txt, 400 )
        mydest = mytext.get_rect( center = (self.screen.get_width() // 2, self.screen.get_height()//2) )

        while True:
            ev = pygame.event.wait()
            if ( ev.type == pygame.MOUSEBUTTONUP) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
                break
            elif ev.type == pygwrap.TIMEREVENT:
                self.view( self.screen )
                pygwrap.default_border.render( self.screen, mydest )
                self.screen.blit( mytext, mydest )
                pygame.display.flip()

    def bump_tile( self, pos ):
        target = self.scene.get_bumpable_at_spot( pos )
        if target:
            target.bump( self )

    def bump_model( self, target ):
        # Do the animation first.
        pc = self.camp.party_spokesperson()

        anims = [ animobs.SpeakHello(pos=pc.pos), animobs.SpeakHello(pos=target.pos)]
        animobs.handle_anim_sequence( self.screen, self.view, anims )

        offers = list()
        for p in self.camp.active_plots():
            offers += p.get_dialogue_offers( target )
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
        pc.contents.equip( it )

    def unequip_item( self, it, pc, redraw ):
        pc.contents.unequip( it )

    def drop_item( self, it, pc, redraw ):
        pc.contents.unequip( it )
        if not it.equipped:
            pc.contents.remove( it )
            it.place( self.scene, pc.pos )

    def trade_item( self, it, pc, redraw ):
        """Trade this item to another character."""
        mymenu = charsheet.RightMenu( self.screen, predraw = redraw )
        for opc in self.camp.party:
            if opc != pc and opc.is_alright():
                mymenu.add_item( str( opc ) , opc )
        mymenu.add_item( "Cancel" , False )
        mymenu.add_alpha_keys()

        opc = mymenu.query()
        if opc:
            pc.contents.unequip( it )
            if not it.equipped:
                if opc.can_take_item( it ):
                    pc.contents.remove( it )
                    opc.contents.append( it )
                else:
                    self.alert( "{0} can't carry any more.".format( str( opc ) ) )


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

    def cast_explo_spell( self, n, can_switch=True ):
        if n >= len( self.camp.party ):
            n = 0
        pc = self.camp.party[ n ]
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=charsheet.CharacterSheet(pc, screen=self.screen, camp=self.camp), screen=self.screen, predraw=self.view, caption="Spells & Techniques" )

        while keep_going:
            mymenu = charsheet.RightMenu( self.screen, predraw = myredraw )
            for tech in pc.techniques:
                mymenu.add_item( str( tech ) , tech )
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
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=self.screen, camp=self.camp)
            elif it is 1:
                n = ( n + 1 ) % len( self.camp.party )
                pc = self.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=self.screen, camp=self.camp)

            elif it:
                # A spell was selected. Deal with it.
                if pc.is_alright() and it.can_be_invoked( pc ):
                    self.pc_use_technique( pc, it, it.exp_tar )
                else:
                    self.alert( "That technique cannot be used right now." )
                keep_going = False
            else:
                keep_going = False

    def view_party( self, n, can_switch=True ):
        if n >= len( self.camp.party ):
            n = 0
        pc = self.camp.party[ n ]
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=charsheet.CharacterSheet(pc, screen=self.screen, camp=self.camp), screen=self.screen, predraw=self.view, caption="View Party" )

        while keep_going:
            mymenu = charsheet.RightMenu( self.screen, predraw = myredraw )
            for i in pc.contents:
                if i.equipped:
                    mymenu.add_item( "*" + str( i ) , i )
                elif not pc.can_equip( i ):
                    mymenu.add_item( "#" + str( i ) , i )
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
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=self.screen, camp=self.camp)
            elif it is 1:
                n = ( n + 1 ) % len( self.camp.party )
                pc = self.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=self.screen, camp=self.camp)

            elif it:
                # An item was selected. Deal with it.
                self.equip_or_whatevs( it, pc, myredraw )

            else:
                keep_going = False

    def monster_inactive( self, mon ):
        return mon not in self.camp.party and (( not self.camp.fight ) or mon not in self.camp.fight.active)

    def update_monsters( self ):
        for m in self.scene.contents:
            if isinstance( m, characters.Character ) and self.monster_inactive(m):
                # First handle movement.
                if m.get_move() and ( ((self.time + hash(m)) % 35 == 1 ) or self.camp.fight ):
                    rdel = random.choice( self.scene.DELTA8 )
                    nupos = ( m.pos[0] + rdel[0], m.pos[1] + rdel[1] )

                    if self.scene.on_the_map(nupos[0],nupos[1]) and not self.scene.map[nupos[0]][nupos[1]].blocks_walking() and not self.scene.get_character_at_spot(nupos):
                        if m.team and m.team.home:
                            if m.team.home.collidepoint( nupos ):
                                m.pos = nupos
                        else:
                            m.pos = nupos

                    # Monsters that can hide may hide.
                    if m.can_use_stealth() and m.is_hostile( self.camp ) and random.randint(1,6) == 1:
                        m.hidden = True

                # Next, check visibility to PC.
                if m.team and m.team.on_guard() and m.pos in self.scene.in_sight:
                    pov = pfov.PointOfView( self.scene, m.pos[0], m.pos[1], 5 )
                    in_sight = False
                    for pc in self.camp.party:
                        if pc.pos in pov.tiles and pc in self.scene.contents:
                            in_sight = True
                            break
                    if in_sight:
                        react = m.get_reaction( self.camp )
                        if react < characters.FRIENDLY_THRESHOLD:
                            if react < characters.ENEMY_THRESHOLD:
                                anims = [ animobs.SpeakAttack(m.pos,loop=16), ]
                                animobs.handle_anim_sequence( self.screen, self.view, anims )
                                self.camp.activate_monster( m )
                                break
                            else:
                                anims = [ animobs.SpeakAngry(m.pos,loop=16), ]
                                animobs.handle_anim_sequence( self.screen, self.view, anims )

    def check_trigger( self, trigger, thing=None ):
        # Something is happened that plots may need to react to.
        for p in self.camp.active_plots():
            p.handle_trigger( self, trigger, thing )

    def expand_puzzle_menu( self, thing, thingmenu ):
        # Something is happened that plots may need to react to.
        for p in self.camp.active_plots():
            p.modify_puzzle_menu( thing, thingmenu )
        if not thingmenu.items:
            thingmenu.add_item( "[Continue]", None )
        else:
            thingmenu.sort()
            thingmenu.add_alpha_keys()


    def keep_exploring( self ):
        return self.camp.first_living_pc() and self.no_quit and not pygwrap.GOT_QUIT and not self.camp.destination

    def update_scene( self ):
        """If appropriate, move models back to their home zone and restock monsters."""
        if self.scene.last_updated < self.camp.day:
            for m in self.scene.contents:
                if isinstance( m, characters.Character ) and m.team and m.team.home and not m.team.home.collidepoint( m.pos ):
                    # This monster is lost. Send it back home.
                    m.pos = self.scene.find_entry_point_in_rect( m.team.home )

            # Check the monster zones. Restock random monsters.
            for mz in self.scene.monster_zones:
                if self.scene.monster_zone_is_empty( mz ) and random.randint(1,2) != 2:
                    NewTeam = teams.Team( default_reaction=-100, home=mz,
                      rank=max( self.scene.rank, ( self.scene.rank + self.camp.party_rank() ) // 2 ),
                      strength=100, habitat=self.scene.get_encounter_request() )
                    mlist = NewTeam.build_encounter(self.scene)
                    poslist = self.scene.find_free_points_in_rect( mz )

                    for m in mlist:
                        if poslist:
                            pos = random.choice( poslist )
                            m.place( self.scene, pos )
                            poslist.remove( pos )
                        else:
                            break

            self.scene.last_updated = self.camp.day

    def go( self ):
        self.no_quit = True
        self.order = None
        if self.scene.name:
            caption = pygwrap.SMALLFONT.render(self.scene.name, True, pygwrap.TEXT_COLOR )
            caption_rect = caption.get_rect(topleft=(32,32))
            caption_timer = 35
        else:
            caption = None

        self.update_scene()

        # Do one view first, just to prep the model map and mouse tile.
        self.view( self.screen )
        pygame.display.flip()

        # Do a start trigger, unless we're in combat.
        if not self.camp.fight:
            self.check_trigger( "START" )

        while self.keep_exploring():
            if self.camp.fight:
                self.order = None
                self.camp.fight.go( self )
                if pygwrap.GOT_QUIT or not self.camp.fight.no_quit:
                    self.no_quit = False
                    break
                self.camp.fight = None

            # Get input and process it.
            gdi = pygwrap.wait_event()

            if gdi.type == pygwrap.TIMEREVENT:
                self.view( self.screen )
                if caption and caption_timer > 0:
                    pygwrap.default_border.render( self.screen, caption_rect )
                    self.screen.blit( caption, caption_rect )
                    caption_timer += -1
                    if caption_timer < 1:
                        caption = None
                pygame.display.flip()

                self.time += 1

                if self.order:
                    if not self.order( self ):
                        self.order = None

                self.update_monsters()

                if self.time % 150 == 0:
                    self.update_enchantments()

            elif not self.order:
                # Set the mouse cursor on the map.
                self.view.overlays.clear()
                self.view.overlays[ self.view.mouse_tile ] = maps.OVERLAY_CURSOR

                if gdi.type == pygame.KEYDOWN:
                    if gdi.unicode == u"1":
                        self.view_party(0)
                    elif gdi.unicode == u"2":
                        self.view_party(1)
                    elif gdi.unicode == u"3":
                        self.view_party(2)
                    elif gdi.unicode == u"4":
                        self.view_party(3)
                    elif gdi.unicode == u"Q":
                        self.no_quit = False
                    elif gdi.unicode == u"a":
                        self.alert( "This is a test of the alert system. Let me know how it turns out." )
                    elif gdi.unicode == u"c":
                        self.view.focus( self.screen, *self.camp.first_living_pc().pos )
                    elif gdi.unicode == u"m":
                        self.cast_explo_spell(0)
                    elif gdi.unicode == u"M":
                        MiniMap( self )
                    elif gdi.unicode == u"R":
                        self.field_camp()
                    elif gdi.unicode == u"s":
                        self.shop( self )
                    elif gdi.unicode == u"*":
                        for pc in self.camp.party:
                            pc.advance( pc.mr_level.__class__ )

                elif gdi.type == pygame.QUIT:
                    self.no_quit = False
                elif gdi.type == pygame.MOUSEBUTTONUP:
                    if gdi.button == 1:
                        # Left mouse button.
                        if ( self.view.mouse_tile != self.camp.first_living_pc().pos ) and self.scene.on_the_map( *self.view.mouse_tile ):
                            self.order = MoveTo( self, self.view.mouse_tile )
                            self.view.overlays.clear()
                        else:
                            self.pick_up( self.view.mouse_tile )
                    else:
                        # If YouTube comments were as good as these comments, we'd all have ponies by now.
                        animobpos = self.view.mouse_tile
#                        ao_pro = animobs.GreenSpray(self.camp.first_living_pc().pos,self.view.mouse_tile )
#                        anims = [ ao_pro, ]
#                        ao_pro.children.append( animobs.Pearl( pos=animobpos ) )


#                        area = pfov.PointOfView( self.scene, animobpos[0], animobpos[1], 5 )
#                        for a in area.tiles:
#                            ao = animobs.SnowCloud( pos=a )
#                            ao = animobs.BlueCloud( pos=a, delay=self.scene.distance(a,animobpos ) * 2 + 1 )
#                            ao.y_off = -25 + 5 * ( abs( a[0]-animobpos[0] ) + abs( a[1]-animobpos[1] ) )
#                            ao_pro.children.append( ao )

#                        animobpos = self.view.mouse_tile
                        pcpos = self.camp.first_living_pc().pos
                        anims = list()

#                        area = pfov.Cone( self.scene, pcpos, animobpos ).tiles
                        area = animobs.get_line( pcpos[0], pcpos[1], animobpos[0], animobpos[1] )
                        area.remove( pcpos )
                        for a in area:
                            ao = animobs.Spark( pos=a, delay=self.scene.distance(a,pcpos ) + 1 )
                            anims.append( ao )
#                        for a in self.scene.contents:
#                            if a.pos in area:
#                                ao = animobs.Caption( str(random.randint(5,27)), a.pos, delay=self.scene.distance(a.pos,pcpos ) + 1 )
#                                anims.append( ao )

                        animobs.handle_anim_sequence( self.screen, self.view, anims )



