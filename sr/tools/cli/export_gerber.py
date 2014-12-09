from __future__ import print_function


OUTPUT_DIR = "./gerbers"


def command(args):
    import os
    import shutil
    import subprocess
    import sys

    import sr.tools.bom.geda as geda

    BOARD = args.board

    if os.path.exists(OUTPUT_DIR) and not os.path.isdir(OUTPUT_DIR):
        print("%s exists and is not a directory" % OUTPUT_DIR)
        print("Cowardly refusing to remove it!")
        sys.exit(1)

    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    with open(BOARD) as file:
        assert geda.file_is_geda_pcb(file)

    print("Generating gerbers from %s" % BOARD)
    # You can't specify the output dir and of the files created some
    # are in the cwd, others are in the same dir as the PCB file :S

    shutil.copy(BOARD, OUTPUT_DIR)
    os.chdir(OUTPUT_DIR)

    cmd = "pcb -x gerber %s" % BOARD
    subprocess.check_call(cmd, shell=True)

    os.remove(BOARD)


def add_subparser(subparsers):
    parser = subparsers.add_parser('export-gerber',
                                   help='Export gerbers. Will output gerbers '
                                        'to directory %s' % OUTPUT_DIR)
    parser.add_argument('board', help='Board to export.')
    parser.set_defaults(func=command)
