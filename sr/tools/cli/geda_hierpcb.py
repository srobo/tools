from __future__ import print_function


class ParseState:
    IDLE = 1
    STARTCOMP = 2
    INCOMP = 3
    STARTTEXT = 4


def command(args):
    import re
    import os
    import sys

    # Read a list of the schematics to process from the gEDA project file
    project_filename = args.project
    schematic_filenames = None
    try:
        project_file = open(project_filename, 'r')
        # Get list of schematics
        for line in project_file:
            if (line.split(' ')[0] == "schematics"):
                clean_line = line.strip('\n')
                schematic_filenames = clean_line.split(' ')[1:]
        project_file.close()
    except IOError:
        print("File not found: %s" % project_filename)
        sys.exit(1)

    if schematic_filenames is None:
        print("Did not find any schematics in project file.")
        sys.exit(1)

    # Get path to sub-schematics from gafrc file
    search_path = ['.']
    try:
        gafrc = open('gafrc', 'r')
        for line in gafrc:
            key = line.split(' ')[0].strip('(')
            if key == "source-library":
                value = line.split(' ')[1].strip(")\n")
                value = value.strip('"')
                search_path.append(value)
        gafrc.close()
    except IOError:
        print('Unable to open gafrc, will only look in the current '
              'directory for schematics.')

    sub_schematic_components = []
    # Iterate over each schematic looking for components with 'source'
    # attribute
    state = ParseState.IDLE
    for schematic_filename in schematic_filenames:
        try:
            schematic = open(schematic_filename, 'r')
            for line in schematic:
                if state == ParseState.STARTCOMP:
                    if line[0] == '{':
                        state = ParseState.INCOMP
                        continue
                    else:
                        state = ParseState.IDLE

                # Drop through to here straight after detecting a component
                # with no extra info
                if state == ParseState.IDLE:
                    if line[0] == 'C':
                        refdes = None
                        source = None
                        state = ParseState.STARTCOMP
                        continue

                if state == ParseState.INCOMP:
                    if line[0] == 'T':
                        state = ParseState.STARTTEXT
                        continue
                    elif line[0] == '}':
                        # At the end of a component, see if we have found one
                        # with a source attrib
                        if source is not None:
                            sub_schematic_components.append((refdes, source))
                        state = ParseState.IDLE
                        continue

                if state == ParseState.STARTTEXT:
                    kv = line.split('=')
                    key = kv[0]
                    value = kv[1].strip('\n')
                    if key == 'refdes':
                        refdes = value
                    elif key == 'source':
                        source = value
                    state = ParseState.INCOMP

            schematic.close()
        except:
            print("Unable to open schematic '%s'" % schematic_filename)

    if len(sub_schematic_components) == 0:
        print("Did not find any sub-schematic components.")
        sys.exit(0)
    else:
        print("Found %s sub-schematic components." %
              len(sub_schematic_components))

    for sub_sche in sub_schematic_components:
        # Find out if a PCB layout already exists for the sub-schematic
        block_filename = sub_sche[1].rsplit('.', 1)[0]
        refdes = sub_sche[0]
        pcb_filename = None

        for path in search_path:
            if os.path.exists(os.path.join(path, block_filename + ".pcb")):
                pcb_filename = os.path.join(path, block_filename + ".pcb")
                print("Found pre-existing PCB layout for %s in %s" %
                      (refdes, pcb_filename))

        if pcb_filename is None:
            # Did not find pre-existing PCB layout
            continue

        dst_filename = os.path.join('.', block_filename + '_' +
                                    refdes + ".pcb")
        try:
            # Open the original PCB layout
            src_pcb = open(pcb_filename, 'r')
            # Open the new PCB layout
            dst_pcb = open(dst_filename, 'w')

            for line in src_pcb:
                if "Element[" in line:
                    regex = r"(Element\[\".*?\" \".*?\" \")(.*)", r"\1" + \
                            refdes + r"/\2"
                    dst_pcb.write(re.sub(regex, line))
                else:
                    dst_pcb.write(line)

            dst_pcb.close()
            src_pcb.close()

            print("Created %s for %s" % (dst_filename, refdes))
        except:
            print("Failed to copy %s to %s" % (pcb_filename, dst_filename))
            continue


def add_subparser(subparsers):
    parser = subparsers.add_parser('geda-hierpcb', help='Geda Hierarchy PCB')
    parser.add_argument('project', help='A gEDA project file.')
    parser.set_defaults(func=command)
