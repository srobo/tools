from __future__ import print_function


def command(args):
    import subprocess

    gsymoutput = []
    symbolfile = []
    inputfile = args.inputfile
    outputfile = args.outputfile

    def readfile(filename):
        with open(filename, 'r') as f:
            symbolfile = [line.strip() for line in f]
        return symbolfile

    # If the output line from gsymcheck gives the coordinates of the error,
    # then use this function to fix the line in symbolfile

    def fix_object_with_coords(line, firstchars, colour, elementno):
        x1 = ''
        y1 = ''
        x = line.find("x1=") + 3
        y = line.find("y1=") + 3
        while line[x] != ',':
            x1 = x1 + line[x]
            x = x + 1
        while line[y] != ')':
            y1 = y1 + line[y]
            y = y + 1
        search = firstchars + x1 + " " + y1
        return fix_line_colour(search, colour, elementno)

    def fix_line_colour(searchstring, colour, elementno, offset=0):
        for entryno in range(0, len(symbolfile)):
            if searchstring in symbolfile[entryno]:
                array = symbolfile[entryno + offset].split(' ')
                print(array)
                array[elementno] = colour
                s = ' '.join(array)
                print(s)
                symbolfile[entryno + offset] = s

    def fix_colours():
        for i in range(0, len(gsymoutput)):
            line = gsymoutput[i]
            if line.find("pin color") != -1:
                fix_object_with_coords(line, "P ", "1", 5)
            elif line.find("Line at") != -1:
                fix_object_with_coords(line, "L ", "3", 5)
            elif line.find("Bus at") != -1:
                fix_object_with_coords(line, "U ", "10", 5)
            elif line.find("Box at") != -1:
                fix_object_with_coords(line, "B ", "3", 5)
            elif line.find("Arc with center") != -1:
                fix_object_with_coords(line, "A ", "3", 6)
            elif line.find("Circle with center") != -1:
                fix_object_with_coords(line, "C ", "3", 4)
            elif (line.find("Text") != -1 and
                  line.find("not using text color") != -1):
                fix_object_with_coords(line, "T ", "9", 3)
            elif (line.find("refdes=") != -1 and
                  line.find("detached attribute color") != -1):
                fix_line_colour("refdes=", "8", 3, -1)
            elif (line.find("pinnumber=") != -1 and
                  line.find("attribute color") != -1):
                fix_line_colour(line[0:line.find(' ')], "5", 3, -1)
            elif (line.find("pinlabel=") != -1 and
                  line.find("text color") != -1):
                print(line[line.find("pinlabel"):line.find(' not')])
                fix_line_colour(line[line.find("pinlabel"):line.find(' not')],
                                "9", 3, -1)
        return symbolfile

    # Write modified symbol file to a new file.

    def write_file(outputfile):
        output = open(outputfile, 'w')
        for item in symbolfile:
            output.write("%s\n" % item)
        output.close()

    def gsymcheck(filename):
        command = ["gsymcheck", "-vv", filename]
        try:
            output = subprocess.check_output(command, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            output = e.output

        gsymoutput = output.splitlines()
        gsymoutput.pop(0)  # first line of output is always blank
        return gsymoutput
        # print error and warning messages associated with a symbol file

    gsymoutput = gsymcheck(inputfile)
    symbolfile = readfile(inputfile)
    print(symbolfile)
    symbolfile = fix_colours()
    write_file(outputfile)
    print(symbolfile)


def add_subparser(subparsers):
    parser = subparsers.add_parser('symbol-correct',
                                   help='Check if symbols are correct.')
    parser.add_argument('inputfile', help='Input filename.')
    parser.add_argument('outputfile', help='Output filename.')
    parser.set_defaults(func=command)
