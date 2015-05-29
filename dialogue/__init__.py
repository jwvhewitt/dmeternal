#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A few words on the division of labour here...
#  - The conversation builder determines the order in which things get said
#  - The grammar-based token expander determines what gets said
#  - The phrase substitution personalizer determines how it's said

# Offer: A line spoken by the NPC, with possible effects.
#   An Offer has a Context, which describes what kind of thing is being said.
# Reply: A line spoken by the PC, which leads to an Exchange.
# Cue: An empty space in a conversation waiting to be filled by an Offer.
#   Both Offers and Cues are described by a context value.
# Context: A value roughly describing the type of an offer/reply.


import random
import copy
import pygame
import pygwrap
import rpgmenu
import voice
import grammar
import personalizer
import context
from context import ContextTag
import base
from base import Cue, Offer, Reply
import offers
import replies
import re
import characters
import services
import image

def harvest( mod, class_to_collect ):
    mylist = []
    for name in dir( mod ):
        o = getattr( mod, name )
        if isinstance( o , class_to_collect ):
            mylist.append( o )
    return mylist


standard_replies = harvest( replies, Reply )
standard_offers = harvest( offers, Offer )

CUE_HELLO = Cue( context.ContextTag([context.HELLO]) )
CUE_THREATEN = Cue( context.ContextTag([context.THREATEN]))

def build_anchor_list( conversation , context_type ):
    # Find all offers in this conversation whose context matches the context_type.
    # One of these offers can be used as an anchor for attaching a new reply link
    # to the conversation.
    anchor_list = []
    if context_type.matches( conversation.context ):
        anchor_list.append( conversation )

    for r in conversation.replies:
        anchor_list += build_anchor_list( r.destination , context_type )

    return anchor_list

def find_anchor( conversation , context_type ):
    anchor_list = build_anchor_list( conversation , context_type )
    if anchor_list:
        return random.choice( anchor_list )
    else:
        return None

def build_cue_list( conversation , context_type ):
    # Find a list of all cues in this conversation which match the context type.
    cue_list = []
    if isinstance( conversation , Cue ) and conversation.context.matches( context_type ):
        cue_list.append( conversation )

    elif isinstance( conversation , Offer ):
        for r in conversation.replies:
            cue_list += build_cue_list( r.destination , context_type )

    return cue_list

def find_cue( conversation , context_type ):
    cue_list = build_cue_list( conversation , context_type )
    if cue_list:
        return random.choice( cue_list )
    else:
        return None

def find_offer_to_match_cue( cue_in_question , offers ):
    # Find an offer in this list which matches one of the provided cues.
    goffs = []
    for o in offers:
        o_cues = o.get_cue_list()
        if cue_in_question.context.matches( o.context ) and cues_accounted_for( o_cues, offers ):
            goffs.append( o )

    if goffs:
        return random.choice( goffs )
    else:
        return None


def cues_accounted_for( list_of_cues, possible_offers ):
    # Return True if every cue in the list has a possible offer.
    ok = True
    for c in list_of_cues:
        if not find_offer_to_match_cue( c, possible_offers ):
            ok = False
            break
    return ok

def find_std_offer_to_match_cue( cue_in_question , npc_offers ):
    # Find an exchange in the standard exchanges list which matches the provided
    # cue and may possibly branch to one of the provided offers.
    # Return a new instance of the good exchange found.
    candidates = []

    for e in standard_offers:
        # We want to check the links from this exchange against the offers on tap.
        # But we don't need to find a waiting offer for the root exchange.
        e_cues = e.get_cue_list()

        if cue_in_question.context.matches( e.context ) and cues_accounted_for( e_cues, npc_offers ):
            candidates.append( e )
    if candidates:
        return copy.deepcopy( random.choice( candidates ) )
    else:
        return None

def replace_all_refs( conversation , cue , exchange ):
    # Searching through the conversation tree, replace all references to cue
    # with exchange.
    for r in conversation.replies:
        if r.destination is cue:
            r.destination = exchange
        elif isinstance( r.destination , Offer ):
            replace_all_refs( r.destination , cue , exchange )

# We have Markov Cheney right where he wants us.

def build_conversation( start,npc_offers ):
    # Given a list of offers, construct a conversation which uses as many of
    # them as possible.
    # Each exchange added to the conversation must link from an exchange already
    # in the conversation. The start parameter provides a starting state from
    # which the first exchange will be generated.
    # "start" can be either a cue or an offer.
    keepgoing = True
    root = start

    while keepgoing:
        # Step one: Replace all cues in the tree with offers.
        cues = root.get_cue_list()
        while cues:
            for c in cues:
                # Convert cue "c".
                # Search the npc_offers first.
                o = find_offer_to_match_cue( c , npc_offers )
                if o:
                    # NPC offers don't get copied, since they are made specifically
                    # for this conversation.
                    exc = o
                    npc_offers.remove( o )
                else:
                    # Standard offers do get copied, because they have to be
                    # shared around.
                    exc = find_std_offer_to_match_cue( c , npc_offers )

                # We now have an exchange. Find the cue it will replace.
                cue = find_cue( root , exc.context )
                if cue is root:
                    root = exc
                else:
                    replace_all_refs( root , cue , exc )
            cues = root.get_cue_list()

        # If there are any unlinked offers, attempt to add some new links.

        # Start by determining the set of anchor contexts (those already part of
        # the conversation structure).
        anchors = root.get_context_set()

        # Check through the list of standard links to see which ones match our
        # available anchors and unlinked offers.
        possible_links = []
        for l in standard_replies:
            if filter( l.context.matches , anchors ) and cues_accounted_for( l.destination.get_cue_list(), npc_offers ):
                possible_links.append( l )

        if possible_links:
            l = random.choice( possible_links )

            # We have a link. Add it to our structure.
            # Find a place where it can link
            a = find_anchor( root , l.context )
            a.replies.append( copy.deepcopy( l ) )
        else:
            keepgoing = False

    return root

class ConvoRedraw( pygame.Rect ):
    # Note that the display will be larger than this, because the border is
    # drawn outside. Consider this measurement the safe area and the border the bleed.
    WIDTH = 350
    HEIGHT = 250
    MENU_HEIGHT = 75

    def __init__( self, npc, x=0, y=0, screen = None, predraw = None ):
        if screen:
            x = screen.get_width() // 2 - self.WIDTH // 2
            y = screen.get_height() // 2 - self.HEIGHT // 2
        super(ConvoRedraw, self).__init__(x,y,self.WIDTH,self.HEIGHT)
        self.npc = npc
        self.regenerate_avatar()
        self.smilies = image.Image( "sys_friendliness.png", 15, 15 )
        self.friendliness = 0

        self.menu_rect = pygame.Rect( x,y+self.HEIGHT-self.MENU_HEIGHT,self.WIDTH,self.MENU_HEIGHT )
        self.text_rect = pygame.Rect( x, y+70, self.WIDTH, self.HEIGHT - self.MENU_HEIGHT - 86 )

        self.text = ""
        self.predraw = predraw

    def regenerate_avatar( self ):
        mybmp = pygame.Surface( (54 , 54) )
        mybmp.fill((0,0,255))
        mybmp.set_colorkey((0,0,255),pygame.RLEACCEL)
        myimg = self.npc.generate_avatar()
        myimg.render( mybmp, frame=self.npc.FRAME )
        self.img = pygame.transform.scale2x( mybmp )

    def get_smiley( self, friendliness ):
        if friendliness < -50:
            return 0
        elif friendliness < -20:
            return 1
        elif friendliness > 50:
            return 4
        elif friendliness > 20:
            return 3
        else:
            return 2

    def __call__( self, screen ):
        if self.predraw:
            self.predraw( screen )
        pygwrap.default_border.render( screen , self )

        # Header avatar
        if self.img:
            screen.blit(self.img , (self.x-20,self.y-20) )
            self.smilies.render( screen, (self.x+50,self.y), self.get_smiley(self.friendliness))
            pygwrap.draw_text( screen, pygwrap.SMALLFONT, str( self.friendliness), pygame.Rect( self.x+55, self.y+16, 64, pygwrap.SMALLFONT.get_linesize() ), justify = -1 )

        # Header info- name and level/gender/race/class
        y = self.y + 6
        pygwrap.draw_text( screen, pygwrap.BIGFONT, str( self.npc ), pygame.Rect( self.x+64, y, self.width-64, pygwrap.BIGFONT.get_linesize() ), justify = 0, color=(240,240,240) )
        y += pygwrap.BIGFONT.get_linesize()
        pygwrap.draw_text( screen, pygwrap.SMALLFONT, self.npc.desc(), pygame.Rect( self.x+64, y, self.width-64, pygwrap.SMALLFONT.get_linesize() ), justify = 0 )

        pygwrap.draw_text( screen, pygwrap.SMALLFONT, self.text, self.text_rect, justify = -1 )


def converse( explo, pc, npc, cue ):
    # The party is going to converse with someone.
    # During the conversation, the Exploration object will have an attribute
    # called "convo" which is a tuple containing the pc, npc, and conversation.
    crd = ConvoRedraw( npc, screen = explo.screen, predraw = explo.view )

    offers = list()
    mygram = grammar.base_grammar( pc, npc, explo )

    for p in explo.camp.active_plots():
        offers += p.get_dialogue_offers( npc, explo )
        pgram = p.get_dialogue_grammar( npc, explo )
        if pgram:
            grammar.absorb( mygram, pgram )

    # Add special offers- Job Training. That's it for now.
    if npc.mr_level and npc.mr_level.__class__ in characters.PC_CLASSES:
        add_ok = False
        for chara in explo.camp.party:
            if chara.xp >= chara.xp_for_next_level() and npc.mr_level.can_take_level( chara ):
                add_ok = True
        if add_ok:
            offers.append( Offer( "[TRAINING]", context = context.ContextTag([context.TRAINING]), effect=services.JobTraining([npc.mr_level.__class__]) ) )

    conversation = build_conversation( cue , offers )
    coff = conversation

    explo.convo = (pc,npc,conversation)

    pc_voice = pc.get_voice()
    npc_voice = npc.get_voice()


    while coff:
        crd.friendliness = npc.get_friendliness(explo.camp)
        crd.text = personalize_text( coff.msg , npc_voice, mygram )
        mymenu = rpgmenu.Menu( explo.screen, crd.menu_rect.x, crd.menu_rect.y, crd.menu_rect.width, crd.menu_rect.height, border=None, predraw=crd )
        for i in coff.replies:
            mymenu.add_item( personalize_text( i.msg, pc_voice, mygram ), i.destination )
        if crd.text and not mymenu.items:
            mymenu.add_item( "[Continue]", None )
        else:
            mymenu.sort()
        nextfx = coff.effect

        coff = mymenu.query()

        if nextfx:
            nextfx( explo )

    del explo.convo



def split_words_and_punctuation( in_text ):
    """Split the string by whitespace, removing punctuation with it."""
    myre = re.compile( r"\b([\w'-]+)([.,:;!?]*)" )
    words = list()
    for mo in re.finditer( myre, in_text ):
        if mo.group(1):
            words.append( mo.group(1) )
        if mo.group(2):
            words.append( mo.group(2) )
    return words

def preprocess_out_text( otext ):
    """Join punctuation to preceding words."""
    nutext = []
    p = ""
    for w in otext:
        if w in ".,:;!?":
            p = p + w
            w = ""
        if p:
            nutext.append( p )
        p = w
    if p:
        nutext.append( p )
    return nutext


def expand_token( token_block, gramdb ):
    """Return an expansion of token according to gramdb. If no expansion possible, return token."""
    a,b,suffix = token_block.partition("]")
    token = a + b
    if token in gramdb:
        ex = random.choice( gramdb[token] )
        all_words = list()
        for word in ex.split():
            if word[0] == "[":
                word = expand_token( word, gramdb )
            all_words.append( word )
        if suffix and all_words:
            all_words[-1] += suffix
        return " ".join( all_words )
    else:
        return token

def convert_tokens( in_text, gramdb ):
    all_words = list()
    for word in in_text.split():
        if word[0] == "[":
            word = expand_token( word, gramdb )
        all_words.append( word )
    return " ".join( all_words )


def personalize_text( in_text, speaker_voice, gramdb ):
    """Return text personalized for the provided context."""
    # Split the text into individual words.
    all_words = split_words_and_punctuation( convert_tokens( in_text, gramdb ) )
    out_text = []

    # Going through the words, check for conversions in the conversion table.
    for w in all_words:
        out_text.append( w )

        for t in range( 5, 0, -1 ):
            if len( out_text ) >= t:
                mykey = " ".join( out_text[-t:] )

                if mykey in personalizer.PT_DATABASE:
                    choices = []

                    for c in personalizer.PT_DATABASE[ mykey ]:
                        if c.fits_voice( speaker_voice ):
                            choices.append( c.subtext )

                    if choices and random.randint( 0, len( choices ) + 1 ) != 0:
                        myswap = random.choice( choices )

                        del out_text[-t:]
                        words_to_add = split_words_and_punctuation( myswap )
                        out_text += words_to_add

    out_text = preprocess_out_text( out_text )
    return " ".join( out_text )

def personalize_text_for_character( explo, speaker, msg ):
    # Generates the speaker voice and the grammar database, then calls
    # the above function.
    mygram = grammar.base_grammar( speaker, None, explo )
    for p in explo.camp.active_plots():
        pgram = p.get_dialogue_grammar( speaker, explo )
        if pgram:
            grammar.absorb( mygram, pgram )
    speaker_voice = speaker.get_voice()
    return personalize_text( msg , speaker_voice, mygram )

def personalize_text_for_narrator( explo, msg ):
    mygram = grammar.base_grammar( None, None, explo )
    for p in explo.camp.active_plots():
        pgram = p.get_dialogue_grammar( None, explo )
        if pgram:
            grammar.absorb( mygram, pgram )
    return convert_tokens( msg, mygram )

