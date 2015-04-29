from __future__ import print_function


res = 150  # Image resolution in DPI


def html_header(f, names=None, image=None, xy=None):
    import base64
    import pkg_resources

    from six.moves import reduce

    header_file = pkg_resources.resource_stream('sr.tools.cli',
                                                'bom_header.html')
    header = header_file.read().decode('UTF-8')

    title = ""
    if names is not None:
        title = " - "
        title = title + reduce(lambda t, n: t + ', ' + n, names)

    img_tag = ""
    cross_hair = ""
    if image is not None:
        img_tag = """<img id="top" src="data:image/png;base64,%s" />""" \
                  % base64.b64encode(image)
        cross_hair = """<img id="crosshair" src="data:image/png;base64,iVBOR
w0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOx
AAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAADeSURBVFiF7
ZW9DYMwEEafE6oUEUUmoWK0jJApKDINVXagT5WCiuhLYQchCrBNkBXJJ50E6Ljvyb4fI4loM+YGg
HSNTXGIV/+NZYAMkAGSAxQb/2/TARhzAp7js9RH5ZEU5lAKGsEgkPPBfStD88WIdxPhuXehEKEAz
YL415uQnMZ7G9o7fwHHlcg3cPatiWJcqcvWYgtuTRwXU2HMBajXgpPPgeRX4H8CNuHdI/IeNBP+q
w13GET+NTA3WxOVe3sEHfvE4neB1LtWI1YctrdhjUev7wmw2TJABsgAyQE+dlzYaD6jZ48AAAAAS
UVORK5CYII=" />"""

    xy_array = ""
    if xy is not None:
        jsondata = convert_xy_to_json(xy)
        xy_array = """var xy = %s;""" % jsondata

    f.write(header % {'title': title, 'img_tag': img_tag,
                      'xy': xy_array, 'cross_hair': cross_hair})


def html_footer(f):
    import os
    import time

    f.write("""
<p>Generated on %s with %s.</p>
</body>
</html>""" % (time.asctime(), os.path.basename('create-bom')))


def pcode_extract_str(pcode):
    for c in range(0, len(pcode)):
        if pcode[c].isdigit():
            return pcode[:c]


def pcode_extract_num(pcode):
    for c in range(0, len(pcode)):
        if pcode[c].isdigit():
            if "." in pcode[c:]:
                return float(pcode[c:])
            else:
                return int(pcode[c:])


def pcode_find_ranges(pcodes):
    grouped = []
    pr = {}

    for pc in pcodes:
        n = pcode_extract_num(pc)
        cs = pcode_extract_str(pc)

        if cs not in pr:
            pr[cs] = []

        if not isinstance(n, int):
            grouped.append(pc)
            continue

        pr[cs].append(n)

    for prefix, nums in pr.items():
        while len(nums):
            start = end = min(nums)
            while end in nums:
                nums.remove(end)
                end += 1
            end -= 1

            if end - start < 2:
                for n in range(start, end + 1):
                    grouped.append("%s%i" % (prefix, n))
            else:
                grouped.append("%s%i-%i" % (prefix, start, end))

    return grouped


def get_sorted_pcodes(line):
    pcodes = [x[1] for x in line]
    pcodes.sort(key=lambda x: pcode_extract_num(x))
    # pcodes = pcode_find_ranges(pcodes)
    return pcodes


def wrap_order_number(onum):
    if len(onum) > 10:
        return onum[:10] + "<wbr>" + onum[10:]
    else:
        return onum


def convert_xy_to_json(xy):
    import json

    parts = {}
    for line in xy.split("\n"):
        if len(line) == 0 or line[0] == "#":
            continue

        s = line.split(",")
        if len(s) != 7:
            continue
        x = int(float(s[3]) / 1000 * res)
        y = int(float(s[4]) / 1000 * res)
        parts[s[0]] = {'value': s[2][1:-1], 'x': x, 'y': y, 'side': s[6][0]}

    return json.dumps(parts)


def prep_parts(lines):
    out_lines = []
    for line in lines:
        if line.part["sr-code"] == "sr-nothing":
            "Ignore sr-nothing -- we don't want it in HTML BOMs"
            continue

        if line.part["manufacturer"] == "any":
            "We don't care where these parts come from"
            line.part["manufacturer"] = "any/open"

        out_lines.append(line)
    return out_lines


def writeHTML(lines, out_fn, args, pcb=None):
    import os

    outf = open(out_fn, "w")
    pcb_image = None
    pcb_xy = None
    if pcb is not None:
        pcb_image = pcb.get_image(res)
        pcb_xy = pcb.get_xy()

    html_header(outf, map(lambda n: os.path.basename(n), args.schematic),
                image=pcb_image, xy=pcb_xy)

    line_num = 1
    total_parts = 0

    for line in lines:
        outf.write("<tr>")
        p = line.part

        url = p.get_url()
        order_num = wrap_order_number(p["order-number"])
        if url is None:
            order_num_html = order_num
        else:
            order_num_html = """<a href="%s">%s</a>""" % (url, order_num)

        quantity = len(line)

        p.update({"line-no": line_num,
                  "order-no": order_num_html,
                  "qty": quantity})

        if p["part-number"] == "":
            p["part-number"] = "&nbsp;"

        outf.write("""
            <td>%(line-no)i</td>
            <td>%(sr-code)s</td>
            <td>%(qty)i</td>
            <td>%(description)s</td>
            <td>%(package)s</td>
            <td>%(supplier)s</td>
            <td>%(order-no)s</td>
            <td>%(manufacturer)s</td>
            <td>%(part-number)s</td>
        """ % p)
        line_num += 1

        total_parts += quantity

        pcodes = get_sorted_pcodes(line)
        if pcb is not None:
            pcodes = ["""<a onmouseover="highlight('%(x)s');return false" """
                      """href="#">%(x)s</a>""" % {'x': x} for x in pcodes]
        outf.write("<td>%s</td>" % "|".join(pcodes))

        outf.write("</tr>")

    outf.write("</tbody></table>")
    outf.write("<p>%i parts in total.</p>" % total_parts)

    html_footer(outf)


def writeXLS(lines, out_fn):
    import xlwt
    book = xlwt.Workbook()
    sheet = book.add_sheet('BOM')
    rowx = 0

    headings = [("Line No.", "line-no"),
                ("Internal Part No.", "sr-code"),
                ("Qty", "qty"),
                ("Value/Description", "description"),
                ("Package", "package"),
                ("Distributor", "supplier"),
                ("Distributor Order No.", "order-number"),
                ("Manufacturer", "manufacturer"),
                ("Part No.", "part-number"),
                ("Reference Designators", "pcodes")]

    # Keep try of the longest line in a column so that we can set the column
    # width
    col_char_count = [0] * len(headings)

    bold_style = xlwt.easyxf("font: bold on;")
    for colx, (heading, field) in enumerate(headings):
        sheet.write(rowx, colx, heading, bold_style)
        col_char_count[colx] = max(col_char_count[colx], len(heading))
    rowx += 1

    for line in lines:
        p = line.part
        p.update({"line-no": rowx,
                  "qty": len(line),
                  "pcodes": ", ".join(get_sorted_pcodes(line))})
        for colx, (heading, field) in enumerate(headings):
            sheet.write(rowx, colx, p[field])
            col_char_count[colx] = max(
                col_char_count[colx], len(str(p[field])))
        rowx += 1

    for colx, c in enumerate(col_char_count):
        # See http://stackoverflow.com/q/3154270 for an explanation of the
        # magic numbers
        sheet.col(colx).width = int((1 + c) * 256)

    book.save(out_fn)


def command(args):
    import os
    import sys

    import sr.tools.bom.parts_db as parts_db
    import sr.tools.bom.bom as bom
    import sr.tools.bom.geda as geda

    lib = parts_db.get_db()
    if os.path.splitext(args.outfile)[1] == '.sch':
        print("Output file has extension 'sch', "
              "aborting as this is almost certainly a mistake")
        sys.exit(1)

    pcb = None
    if args.layout:
        pcb = geda.PCB(args.layout)

    out_fn = args.outfile

    multibom = bom.MultiBoardBom(lib)
    multibom.load_boards_args(args.schematic, allow_multipliers=False)

    sorted_lines = sorted(multibom.values(), key=lambda x: x.part['sr-code'])
    lines = prep_parts(sorted_lines)

    if os.path.splitext(out_fn)[1] == ".xls":
        print("Writing XLS BOM")
        writeXLS(lines, out_fn)
    else:
        print("Writing HTML BOM")
        writeHTML(lines, out_fn, args, pcb)


def command_deprecated(args):
    import sys

    print("This is deprecated, please use 'create-bom' instead.",
          file=sys.stderr)
    command(args)


def add_subparser(subparsers):
    parser = subparsers.add_parser('create_bom', help='Create a BOM.')
    parser.add_argument(
        'schematic', nargs='+', help='The schematic to read from.')
    parser.add_argument('outfile', help='The output HTML/XLS file.')
    parser.add_argument(
        '--layout', '-l', help='The PCB layout for a single design.')
    parser.set_defaults(func=command_deprecated)

    parser = subparsers.add_parser('create-bom', help='Create a BOM.')
    parser.add_argument(
        'schematic', nargs='+', help='The schematic to read from.')
    parser.add_argument('outfile', help='The output HTML/XLS file.')
    parser.add_argument(
        '--layout', '-l', help='The PCB layout for a single design.')
    parser.set_defaults(func=command)
