from __future__ import print_function


def which(name):
    import os

    # Adapted from answer to
    # http://stackoverflow.com/questions/775351/os-path-exists-for-files-in-your-path
    for p in os.environ["PATH"].split(os.pathsep):
        possible_path = os.path.join(p, name)
        if os.path.exists(possible_path):
            return possible_path

    return None


def ensure_callable(*names):
    import sys

    missing = [name for name in names if which(name) is None]
    if len(missing) == 0:
        return
    end = 'y' if len(missing) == 1 else 'ies'
    print("Missing dependenc{0}: {1}".format(end, ", ".join(missing)))
    sys.exit(1)


def command(args):
    import os
    import pkg_resources
    import shutil
    import subprocess
    import sys
    import tempfile
    import zipfile

    source = args.source.read()

    ensure_callable('pandoc', 'pdflatex')

    cmdline = ['pandoc',
               '-f', 'html' if args.html else 'markdown',
               '-t', 'latex',
               '-']
    pandoc_process = subprocess.Popen(cmdline,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      universal_newlines=True)
    pandoc_process.stdin.write(source)
    pandoc_process.stdin.close()
    generated = pandoc_process.stdout.read()
    pandoc_process.wait()

    generated = generated.replace(
        '\section', '\section*').replace('\subsection', '\subsection*')

    prefix_file = pkg_resources.resource_stream('sr.tools.cli',
                                                'document_prefix.tex')
    suffix_file = pkg_resources.resource_stream('sr.tools.cli',
                                                'document_suffix.tex')
    prefix = prefix_file.read().decode('UTF-8')
    suffix = suffix_file.read().decode('UTF-8')

    signature_block = ''
    if args.signature:
        signature_elements = args.signature.split(':')
        if len(signature_elements) == 1:
            signature_username = signature_elements[0]
            signature_title = None
        else:
            signature_username, signature_title = signature_elements
        signature_block = '\n'.join([r'\bigskip'] * 5)
        signature_block += '\n{0}\n'.format(signature_username)
        if signature_title:
            signature_block += '\\\\ {0}\n'.format(signature_title)

    total = '\n'.join((prefix, generated, signature_block, suffix))

    if args.latex:
        args.output.write(total)
        sys.exit(0)

    temp_dir = tempfile.mkdtemp('srdoc')

    main_file = os.path.join(temp_dir, 'main.tex')
    with open(main_file, 'w') as f:
        f.write(total)

    file = pkg_resources.resource_stream('sr.tools.cli',
                                         'latex-assets.zip')
    with zipfile.ZipFile(file) as zf:
        for name in ('ecs.png', 'moto.png', 'bitbox.png', 'sr-logo.pdf'):
            zf.extract(name, temp_dir)

    cmdline = ['pdflatex', '-interaction=nonstopmode', 'main.tex']
    pdflatex_proc = subprocess.Popen(cmdline,
                                     cwd=temp_dir,
                                     stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     universal_newlines=True)

    while pdflatex_proc.returncode is None:
        (out, err) = pdflatex_proc.communicate()
        errors = [line for line in out.split(
            os.linesep) if len(line) > 0 and line[0] == '!']
        if len(errors) > 0:
            print(os.linesep.join(errors))

    output_file = os.path.join(temp_dir, 'main.pdf')
    success = pdflatex_proc.returncode == 0 and os.path.exists(output_file)
    if success:
        with open(output_file, 'rb') as f:
            args.output.write(f.read())

    shutil.rmtree(temp_dir)

    if not success:
        print('Error: pdflatex failed to produce output')
        sys.exit(1)


def add_subparser(subparser):
    import argparse

    parser = subparser.add_parser(
        'document', help="Generate formatted documents.")
    parser.add_argument("source", metavar="FILE", type=argparse.FileType('r'),
                        help="Source markdown file")
    parser.add_argument("-o", "--output", dest="output",
                        metavar="FILE", type=argparse.FileType('wb'),
                        help="Output file", required=True)
    parser.add_argument("-l", action="store_true", dest="latex",
                        help="Emit LaTeX source rather than PDF")
    parser.add_argument("-s", dest="signature", type=str,
                        help="Add a signature space")
    parser.add_argument("-H", action="store_true", dest="html",
                        help="Take HTML rather than markdown")
    parser.set_defaults(func=command)
