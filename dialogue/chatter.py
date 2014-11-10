""" Chatter is in-party dialogue, no NPCs necessarily involved.

    When a chatter stream is activated, the list of possible responses
    is searched until a legal response is found. If no response is found,
    this chatter stream has failed, which may or may not be a problem for
    the parent.
"""

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



