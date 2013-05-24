"Config for the SR tools"
import os
from subprocess import check_output
import yaml

class Config(dict):
    "Configuration reader for the SR tools"

    def __init__(self):
        # Load the config from ${THIS_REPO}/config.yaml
        self.update_from_file( os.path.join( self.get_tools_root(), 
                                             "config.yaml" ) )

        # Override with the local config
        local_fname = os.path.expanduser( "~/.sr/config.yaml" )
        if os.path.exists( local_fname ):
            self.update_from_file( local_fname )

    @staticmethod
    def get_tools_root():
        "Return the root directory of tools.git"

        # Discover our directory
        mydir = os.path.dirname( __file__ )

        # Find the root of this git repo
        root = check_output( [ "git", "rev-parse", "--show-toplevel" ],
                             cwd = mydir )

        return root[0:-1]

    def update_from_file(self, fname):
        "Update the config from the given YAML file"

        with open(fname, "r") as f:
            d = yaml.load(f, Loader = yaml.CLoader )

        self.update(d)
        
        
