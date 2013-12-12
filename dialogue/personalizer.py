import voice

""" Style Guide: When writing dialogue, try to follow the following rules.
    - Do not use contractions.
"""

class PTEntry( object ):
    def __init__( self, subtext, requires = {} ):
        self.subtext = subtext
        self.requires = requires
    def fits_voice( self, npc_voice ):
        ok = True
        for k,v in self.requires.iteritems():
            if v:
                # This key is required.
                ok = ok and ( k in npc_voice )
            else:
                # This key is prohibited.
                ok = ok and ( k not in npc_voice )
        return ok

PT_DATABASE = {
    "Hello.":   (
        PTEntry( "'Ello, ello.", { voice.ORCISH: True } ),
        PTEntry( "Lali-ho.", { voice.DWARVEN: True } ),
        ),
    "Hello,":   (
        PTEntry( "'Ello there,", { voice.ORCISH: True } ),
        PTEntry( "Lali-ho,", { voice.DWARVEN: True } ),
        ),
    "here":   (
        PTEntry( "'ere", { voice.ORCISH: True } ),
        ),
    "I am": (
        PTEntry( "I'm" ),
        ),
    "I would": (
        PTEntry( "I'd" ),
        ),
    "is not": (
        PTEntry( "isn't" ),
        PTEntry( "ain't", { voice.STUPID: True } ),
        ),
    "my":   (
        PTEntry( "me", { voice.ORCISH: True } ),
        PTEntry( "me", { voice.ORCISH: True, voice.STUPID: True } ),
        ),
    "There is": (
        PTEntry( "There's" ),
        PTEntry( "Dere's", { voice.ORCISH: True } ),
       ),
    "There is not": (
        PTEntry( "There isn't", { voice.STUPID: False } ),
        PTEntry( "There ain't", { voice.STUPID: True } ),
        PTEntry( "Dere ain't", { voice.ORCISH: True } ),
        PTEntry( "Dere ain't no", { voice.ORCISH: True, voice.STUPID: True } ),
       ),
    "This is": (
        PTEntry( "Dis ere's", { voice.ORCISH: True } ),
        PTEntry( "This here's", { voice.ORCISH: True, voice.SMART: True } )
       ),
    "Welcome": (
        PTEntry( "Lali-ho", { voice.DWARVEN: True } ),
       ),
    "Welcome to": (
        PTEntry( "Git over 'ere to", { voice.ORCISH: True } ),
       ),
    }

