class Cue(object):
    # An empty node, waiting to be filled with randomly selected dialog.
    def __init__( self , context ):
        self.context = context

    def get_context_set(self):
        # Get the set of all context tags used by this Cue. Since a cue doesn't
        # link to anything else, that would be its own context and nothing else.
        return set( [ self.context ] )

    def get_cue_list(self):
        # Get the set of all cues. Since this is a cue, return itself.
        return [ self, ]


class Offer(object):
    # An Offer is a single line spoken by the NPC, along with its context tag,
    # effect, and a list of replies.
    def __init__(self, msg, context=(), effect = None, replies = None ):
        self.msg = msg
        self.context = context
        self.effect = effect

        if replies == None:
            self.replies = []
        else:
            self.replies = replies

    def get_context_set(self):
        # Get the set of all context tags used by this offer and any offers or
        # cues linked by the replies.
        context = set( [ self.context ] )
        for e in self.replies:
            context = context | e.destination.get_context_set()
        return context

    def get_cue_list(self):
        # Get the set of all offers which are not really offers, but are just
        # cues waiting to be filled.
        cues = list()
        for e in self.replies:
            cues += e.destination.get_cue_list()
        return cues

    def __str__(self):
        return self.msg


class Reply(object):
    # A persona.Reply is a single line spoken by the PC, leading to a new exchange
    def __init__(self, msg, destination=None, context=() ):
        self.msg = msg
        self.destination = destination
        self.context = context

    def get_context_set( self ):
        # Get the set of contexts this link. This is going to depend on the links
        # in the replies.
        return self.destination.get_context_set()

    def __str__(self):
        return self.msg

