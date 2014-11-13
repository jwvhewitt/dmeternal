""" Chatter is in-party dialogue, no NPCs necessarily involved.

    When a chatter stream is activated, the list of possible responses
    is searched until a legal response is found. If no response is found,
    this chatter stream has failed, which may or may not be a problem for
    the parent.
"""
import random

class Say( object ):
    def __init__( self, msg, children=None, end_ok=True, speaker=None, species=None, job=None ):
        self.msg = msg
        self.children = children
        self.end_ok = end_ok
        self.speaker = speaker
        self.species = species
        self.job = job

    def find_speaker( self, explo, cast=list() ):
        # Locate a PC that meets this seeker's requirements and has not yet
        # been used.
        candidates = list()
        for pc in explo.camp.party:
            if pc not in cast and pc.is_alright():
                seems_legit = True
                if self.species:
                    seems_legit = seems_legit and isinstance( pc.species, self.species )
                if self.job:
                    seems_legit = seems_legit and isinstance( pc.mr_level, self.job )
                if seems_legit:
                    candidates.append( pc )
        if candidates:
            return random.choice( candidates )

    def build( self, explo, cast ):
        # We are going to Say.eet now.
        # -Attempt to find a speaker
        # -If not a good end, attempt to find a child.
        my_cutscene = list()
        pc = self.find_speaker( explo, cast )
        if pc:
            my_cutscene.append( (pc,self.msg) )

            if self.children:
                random.shuffle( self.children )
                nucast = cast + [pc,]
                child_added = False

                for candidate in self.children:
                    reply = candidate.build( explo, nucast )
                    if reply:
                        my_cutscene += reply
                        child_added = True
                        break

                if not (child_added or self.end_ok):
                    my_cutscene = None

        return my_cutscene

def roll_cutscene( explo, cslist, cast=list() ):
    random.shuffle( cslist )
    beats = list()

    for candidate in cslist:
        beats = candidate.build( explo, cast )
        if beats:
            for b in beats:
                explo.alert( "{0}: {1}".format( *b ) )
            break


