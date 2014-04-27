#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       
#       Copyright 2014 Joseph Hewitt <pyrrho12@yahoo.ca>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
# 

import narrator
import context
import maps
import pygame
import pygwrap
import rpgmenu
import campaign
import util
import pickle
import image
import glob
import random
import chargen


class PosterRedraw( object ):
    def __init__( self, screen ):
        self.image = pygame.image.load( random.choice( pygwrap.POSTERS ) ).convert()
        self.image_dest = self.image.get_rect( center=(screen.get_width()//2,screen.get_height()//2) )
    def __call__( self, screen ):
        screen.fill( (0,0,0) )
        screen.blit(self.image , self.image_dest )

class TitleScreenRedraw( object ):
    def __init__( self, screen ):
        self.screen_center_x = screen.get_width() // 2
        self.screen_center_y = screen.get_height() // 2
        self.logo = image.Image( "sys_logo.png" )
        self.logo_dest = self.logo.bitmap.get_rect( midbottom=(self.screen_center_x,self.screen_center_y-25) )
        self.get_bg_image()

    def get_bg_image( self ):
        self.image = pygame.image.load( random.choice( pygwrap.POSTERS ) ).convert()
        self.image_dest = self.image.get_rect( center=(self.screen_center_x,self.screen_center_y) )

    def __call__( self, screen ):
        screen.fill( (0,0,0) )
        screen.blit(self.image , self.image_dest )
        screen.blit(self.logo.bitmap , self.logo_dest )


def start_campaign( init, screen ):
    pygwrap.please_stand_by( screen, "Building world..." )
    nart = narrator.Narrative( init )
    if nart.story:
        nart.build()
        camp = nart.camp
        pcs = campaign.load_party( screen )
        if pcs:
            camp.name = pygwrap.input_string(screen, redrawer=PosterRedraw(screen), prompt="Enter campaign name" )
            camp.add_party( pcs )
            camp.place_party()
            camp.play( screen )

def default_start_campaign( screen ):
    start_campaign( narrator.plots.PlotState(rank=1), screen )

def load_campaign( screen ):
    rpm = rpgmenu.Menu( screen,screen.get_width()//2-250,screen.get_height()//2-200,500,400,predraw=PosterRedraw(screen) )
    rpm.add_files( util.user_dir("rpg_*.sav") )
    rpm.sort()
    rpm.add_alpha_keys()
    rpm.add_item( "Cancel Load Campaign", None )
    cmd = rpm.query()
    if cmd:
        f = open( cmd, "rb" )
        camp = pickle.load( f )
        f.close()
        if camp:
            camp.play( screen )



if __name__=='__main__':
    # Set the screen size.
    if util.config.getboolean( "DEFAULT", "fullscreen" ):
        screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )
    else:
        screen = pygame.display.set_mode( (800,600) )
    pygame.init()
    pygwrap.init()
    rpgmenu.init()

    screen_center_x = screen.get_width() // 2
    screen_center_y = screen.get_height() // 2

    rpm = rpgmenu.Menu( screen,screen_center_x-100,screen_center_y + 25,200,200,predraw=TitleScreenRedraw(screen) )

    rpm.add_item( "Create Character", chargen.make_and_save_character )
    rpm.add_item( "Load Campaign", load_campaign )
    rpm.add_item( "Start Campaign", default_start_campaign )
    rpm.add_item( "Quit Game", None )

    cmd = True
    while cmd:
        cmd = rpm.query()
        if cmd:
            cmd( screen )



