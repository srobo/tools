from sr.tools.cli.inventory import edit, findpart, list_assy_templates, \
                                   list_templates, mv, new_asset, new_group, \
                                   query, set_attr, show_parent, show, \
                                   sync_asset, touch


def add_subparsers(subparsers):
    edit.add_subparser(subparsers)
    findpart.add_subparser(subparsers)
    list_assy_templates.add_subparser(subparsers)
    list_templates.add_subparser(subparsers)
    mv.add_subparser(subparsers)
    new_asset.add_subparser(subparsers)
    new_group.add_subparser(subparsers)
    query.add_subparser(subparsers)
    set_attr.add_subparser(subparsers)
    show_parent.add_subparser(subparsers)
    show.add_subparser(subparsers)
    sync_asset.add_subparser(subparsers)
    touch.add_subparser(subparsers)
