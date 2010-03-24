import os

def get_dict( TOOLS ):
    """Returns a dict of all the available tools """
    cmds = {}

    # Find the executable files in the subdirectories
    for d in os.listdir( TOOLS ):
        if d in [".svn"]:
            continue

        path = os.path.join( TOOLS, d )

        if os.path.isdir( path ):
            # Go through the files in this subdir 
            for f in os.listdir(path):
                if f == "sr":
                    continue

                fp = os.path.join( path, f )

                if os.path.isfile(fp) and os.access( fp, os.X_OK ):
                    cmds[f] = fp

    return cmds
