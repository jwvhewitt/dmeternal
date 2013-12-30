import characters
import teams
import hotmaps
import pygwrap
import pygame
import maps
import collections
import image

class TacticsRedraw( object ):
    def __init__( self, chara, comba, explo, hmap = None ):
        self.chara = chara
        self.comba = comba
        self.explo = explo
        self.hmap = hmap
        self.rect = pygame.Rect( 32, 32, 300, 15 )
        self.gems = image.Image( "sys_counters.png", 10, 16 )

    def __call__( self, screen ):
        self.explo.view( screen )
        pygwrap.default_border.render( screen, self.rect )
        pygwrap.draw_text( screen, pygwrap.SMALLFONT, str( self.chara ), self.rect )
        ap = min( self.chara.get_move() - self.comba.ap_spent[ self.chara ], 24 )
        if self.hmap and self.comba.scene.on_the_map( *self.explo.view.mouse_tile ):
            apr = ap - self.hmap.map[self.explo.view.mouse_tile[0]][self.explo.view.mouse_tile[1]]
        else:
            apr = ap

        if ap > 0:
            mydest = pygame.Rect( self.rect.x + 180, self.rect.y, 32, 32 )
            pygwrap.draw_text( screen, pygwrap.ITALICFONT, "AP:", mydest )
            for t in range( 1, (ap+3)//2 ):
                mydest.x = self.rect.x + 198 + t * 8
                if t <= ( apr + 1 ) //2:
                    if apr >= t * 2:
                        self.gems.render( screen, mydest, 1 )
                    else:
                        self.gems.render( screen, mydest, 6 )
                else:
                    self.gems.render( screen, mydest, 5 )




class Combat( object ):
    def __init__( self, explo, monster_zero ):
        self.active = []
        self.scene = explo.scene
        self.camp = explo.camp
        self.ap_spent = collections.defaultdict( int )
        self.no_quit = True

        for m in explo.scene.contents:
            if isinstance( m, characters.Character ) and m.is_alright():
                if m in self.camp.party:
                    self.active.append( m )
                elif self.scene.range( m.pos, monster_zero.pos ) < 5:
                    self.active.append( m )
                elif m.team and m.team == monster_zero.team:
                    self.active.append( m )
        # Sort based on initiative roll.
        self.active.sort( key = characters.roll_initiative, reverse=True )

    def num_enemies( self ):
        """Return the number of active, hostile characters."""
        n = 0
        for m in self.active:
            if isinstance( m, characters.Character ) and m.is_alright() and m.get_reaction( self.camp ) < teams.ENEMY_THRESHOLD:
                n += 1
        return n

    def can_act( self, chara ):
        """Return True if the provided character can act right now."""
        return chara.is_alright() and self.ap_spent[ chara ] < chara.get_move()

    def still_fighting( self ):
        """Keep playing as long as there are enemies, players, and no quit."""
        return self.num_enemies() and self.camp.first_living_pc() and self.no_quit and not pygwrap.GOT_QUIT

    def step( self, chara, hmap ):
        """Move chara to a better position according to hmap."""
        best_d = hmap.downhill_dir( chara.pos )

        if best_d:
            x2 = best_d[0] + chara.pos[0]
            y2 = best_d[1] + chara.pos[1]
            target = self.scene.get_character_at_spot( (x2,y2) )

            if not target:
                chara.pos = (x2,y2)
                self.ap_spent[ chara ] += 1 + abs(best_d[0]) + abs(best_d[1])
                return False
            else:
                return target
        else:
            return True


    def move_player_to_spot( self, explo, chara, pos, redraw=None ):
        result = None
        if not redraw:
            redraw = explo.view
        explo.view.overlays.clear()
        if self.scene.on_the_map( *pos ) and not self.scene.map[pos[0]][pos[1]].blocks_walking():
            hmap = hotmaps.PointMap( self.scene, pos, avoid_models=True )

            while self.ap_spent[ chara ] < chara.get_move():
                result = self.step( chara, hmap )
                self.scene.update_pc_position( chara )
                if result:
                    break

                redraw( explo.screen )
                pygame.display.flip()

        return result


    def do_player_action( self, explo, chara ):
        #Start by making a hotmap centered on PC, to see how far can move.
        hm = hotmaps.MoveMap( self.scene, chara )

        tacred = TacticsRedraw( chara, self, explo, hm )

        while self.can_act( chara ) and self.still_fighting():
            # Get input and process it.
            gdi = pygwrap.wait_event()

            if gdi.type == pygwrap.TIMEREVENT:
                explo.view.overlays.clear()
                explo.view.overlays[ chara.pos ] = maps.OVERLAY_CURRENTCHARA
                explo.view.overlays[ explo.view.mouse_tile ] = maps.OVERLAY_CURSOR

                tacred( explo.screen )
                pygame.display.flip()

            else:
                if gdi.type == pygame.KEYDOWN:
                    if gdi.unicode == u"Q":
                        self.no_quit = False
                elif gdi.type == pygame.MOUSEBUTTONUP:
                    if gdi.button == 1:
                        # Left mouse button.
                        if ( explo.view.mouse_tile != chara.pos ) and self.scene.on_the_map( *explo.view.mouse_tile ):
                            tacred.hmap = None
                            self.move_player_to_spot( explo, chara, explo.view.mouse_tile, tacred )
                            tacred.hmap = hotmaps.MoveMap( self.scene, chara )

    def do_npc_action( self, explo, chara ):
        pass


    def do_combat_action( self, explo, chara ):
        if chara in self.camp.party:
            self.do_player_action( explo, chara )
        else:
            self.do_npc_action( explo, chara )

    def go( self, explo ):
        """Perform this combat."""

        n = 0
        while self.still_fighting():
            if self.active[n].is_alright():
                self.do_combat_action( explo, self.active[n] )
            n += 1
            if n >= len( self.active ):
                n = 0
                self.ap_spent.clear()

# I do not intend to create one more boring derivative fantasy RPG. I intend to create all of the boring derivative fantasy RPGs.



