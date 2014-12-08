from sr.tools.cli.misc import cam_serial, cog_team, document, list_commands, \
                              make_purchase, mcv4b_part_code, \
                              schedule_knockout, sd_serial, srweb_version, \
                              update, usb_key_serial


def add_subparsers(subparsers):
    cam_serial.add_subparser(subparsers)
    cog_team.add_subparser(subparsers)
    document.add_subparser(subparsers)
    list_commands.add_subparser(subparsers)
    make_purchase.add_subparser(subparsers)
    mcv4b_part_code.add_subparser(subparsers)
    schedule_knockout.add_subparser(subparsers)
    sd_serial.add_subparser(subparsers)
    srweb_version.add_subparser(subparsers)
    update.add_subparser(subparsers)
    usb_key_serial.add_subparser(subparsers)
