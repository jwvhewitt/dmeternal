import util

class Campaign( object ):
    """A general holder for all the stuff that goes into a DME campaign."""
    def __init__( self, name = "BobDwarf19" ):
        self.name = name
        self.party = []
        self.scenes = []


    def save( self ):
        f = open( util.user_dir( "rpg_" + self.name + ".sav" ) , "wb" )
        pickle.dump( self , f, -1 )
        f.close()

