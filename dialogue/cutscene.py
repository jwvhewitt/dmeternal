""" Chatter is in-party dialogue, no NPCs necessarily involved.

    When a chatter stream is activated, the list of possible responses
    is searched until a legal response is found. If no response is found,
    this chatter stream has failed, which may or may not be a problem for
    the parent.
"""
import random

class PCSeek( object ):
    def __init__( self, species=None, job=None, can_be_dead=False ):
        self.species = species
        self.job = job
        self.gender = gender
    def find( self, explo, cast=dict() ):
        # Locate a PC that meets this seeker's requirements and has not yet
        # been used.
        candidates = list()
        for pc in explo.camp.party:
            if pc not in cast.items() and ( pc.is_alright() or self.can_be_dead ):
                seems_legit = True
                if self.species:
                    seems_legit = isinstance( pc.species, self.species )
                if self.job:
                    seems_legit = isinstance( pc.mr_level, self.job )
                if seems_legit:
                    candidates.append( pc )
        return random.choice( candidates )

class Say( object ):
    def __init__( self, msg, speaker, children=None, end_ok=True ):
        self.msg = msg
        self.speaker = speaker
        self.children = children
        self.end_ok = end_ok

    def speak( self, actors ):
        # We are going to Say.eet now.
        # -Attempt to find a speaker
        # -If not a good end, attempt to find a child.



