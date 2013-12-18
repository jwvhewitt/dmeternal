import image
import pygwrap
import pygame


class AnimOb( object ):
    """An animation for the map."""
    def __init__( self, sprite_name, width=54, height=54, pos=(0,0), start_frame=0, end_frame=0, ticks_per_frame=1, loop=0, y_off=0 ):
        self.sprite = image.Image( sprite_name, width, height )
        self.start_frame = start_frame
        self.frame = start_frame
        self.end_frame = end_frame
        self.ticks_per_frame = ticks_per_frame
        self.counter = 0
        self.loop = loop
        self.y_off = y_off
        self.needs_deletion = False
        self.pos = pos

    def update( self ):
        self.counter += 1
        if self.counter > self.ticks_per_frame:
            self.frame += 1
            self.counter = 0

        if self.frame <= self.end_frame:
            self.x += self.dx
            self.y += self.dy
        else:
            self.loop += -1
            if self.loop < 0:
                self.needs_deletion = True
            else:
                self.frame = self.start_frame
                self.counter = 0


    def render( self, view, screen, dest ):
        mydest = pygame.Rect( dest )
        mydest.y += self.y_off
        self.sprite.render( screen, mydest, self.frame )

class SpeakHello( AnimOb ):
    def __init__(self, pos=(0,0), loop=10 ):
        super(SpeakHello, self).__init__(sprite_name="fx_emoticons.png",pos=pos,loop=loop,y_off=-16)
        self.go_up = True
    def update( self ):
        self.counter += 1
        if self.counter > self.loop:
            self.needs_deletion = True

class Projectile( AnimOb ):
    """An AnimOb which moves along a line."""
    def __init__( self, sprite_name, width=54, height=54, start_pos=(0,0), end_pos=(0,0) frame=0, y_off=0 ):
        self.sprite = image.Image( sprite_name, width, height )
        self.frame = frame
        self.counter = 0
        self.y_off = y_off
        self.needs_deletion = False
        self.pos = start_pos
        self.itinerary = self.get_line( start_pos[0], start_pos[1], end_pos[0], end_pos[1] )

	def dir_frame_offset( self, start_pos, end_pos ):
		# There are 8 sprites for each projectile type, one for each of 
		# the eight directions. Determine the direction which best suits 
		# this vector. 
		# Sprite 0 is pointing 12 o'clock and they go clockwise from there.
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]

        # Note that much of the following is magic translated from Pascal.
        # I must've put some thought into it, but it looks mysterious now.
		if dx == 0:
			if dy > 0:
				return 1
			else:
				return 5
		else:
			slope = float(dx)/float(dy)
			if slope > 4.51:
                tmp = 0
			elif slope > 0.414:
                tmp = 1
			elif slope > -0.414:
                tmp = 2
			elif slope > -4.51:
                tmp = 3
			else:
                tmp = 4
			if DX > 0:
                return 5 - tmp
			else:
                return ( 9 - tmp ) mod 8;

    def get_line(x1, y1, x2, y2):
        # Bresenham's line drawing algorithm, as obtained from RogueBasin.
        points = []
        issteep = abs(y2-y1) > abs(x2-x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2-y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if issteep:
                points.append((y, x))
            else:
                points.append((x, y))
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax
        # Reverse the list if the coordinates were reversed
        if rev:
            points.reverse()
        return points

    def update( self ):
        self.counter += 1
        if self.counter >= len( self.itinerary ):
            self.needs_deletion = True
        else:
            self.pos = self.itinerary[ self.counter ]


def handle_anim_sequence( screen, view, anims ):
    view.anims.clear()
    while anims:
        for a in anims[:]:
            view.anims[a.pos] = a
            a.update()
            if a.needs_deletion:
                anims.remove( a )
        view( screen )
        pygame.display.flip()
        while pygwrap.wait_event().type != pygwrap.TIMEREVENT:
            pass
    view.anims.clear()



