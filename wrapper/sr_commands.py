import git_repos, os

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

    # If the git repos are around, list them too:
    if os.path.exists( os.path.join( TOOLS, "git" ) ):
        for name, git in git_repos.gits.iteritems():
            for cmd in git["commands"]:
                path = os.path.join( TOOLS, "git", name, cmd )
                cmds[ os.path.basename( path ) ] = path

    return cmds
