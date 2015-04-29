from __future__ import print_function


class CachedAssetFinder:
    """
    A class that can be used for finding assets in trees.

    The results are also cached to improve performance.

    :param repo: The repository to work on.
    """
    def __init__(self, repo):
        self.repo = repo

    def search(self, code=None, id=None, path=None):
        """
        Set the search mode.

        The finder has two modes, one for finding assets from their code and
        one for finding assets from their blob ID and path.

        :param code: The asset code to search for.
        :param id: The blob ID to search for.
        :param path: The path to search for.
        """
        self._cache = {}
        self.search_code = code
        self.search_id = id
        self.search_path = path

    def _test_object(self, id, name, path):
        if self.search_id and self.search_path:
            if id == self.search_id and self.search_path == path:
                return True
        else:
            if self.search_code in name:
                return True

    def test(self, obj, name=None, path=''):
        """
        Test if the Git object (typically a tree) contains the asset.

        :param obj: The object to test.
        """
        try:
            return self._cache[obj.id]
        except KeyError:
            pass

        import pygit2

        if isinstance(obj, pygit2.Tree):
            for entry in obj:
                entry_path = '/'.join([path, entry.name])
                res = self.test(self.repo[entry.id], entry.name, entry_path)
                if res:
                    return res

            self._cache[obj.id] = None
            return None
        elif isinstance(obj, pygit2.Blob):
            if self._test_object(obj.id, name, path):
                return (self.search_code, obj.id, path)
            else:
                self._cache[obj.id] = None
                return None
        else:
            raise ValueError('Must be a tree or blob.')


def find_asset_by_code(asset_finder, asset_code, all_commits):
    """
    Find an asset by the asset code.

    :param asset_finder: The cached asset finder to use.
    :param asset_code: The code of the asset to search for.
    :param all_commits: All the commits to look for.
    :returns: A pair containing the result from the 'test' and the commit.
    """
    asset_finder.search(code=asset_code)

    for commit in all_commits:
        res = asset_finder.test(commit.tree)
        if res:
            return res, commit


def get_history(repo, asset_code):
    """
    Get the history of an asset in the repository.

    :param repo: The repository to look in.
    :param asset_code: The code of the asset to look for.
    :returns: An iterator where each item is a tuple containing a status of the
              the event, the commit and any additional arguments.
    """
    import pygit2

    asset_finder = CachedAssetFinder(repo)
    asset_finder.search(code=asset_code)

    sort_mode = pygit2.GIT_SORT_TOPOLOGICAL | pygit2.GIT_SORT_REVERSE
    all_commits = repo.walk(repo.head.target, sort_mode)

    old_res, _ = added_res, added_commit = find_asset_by_code(asset_finder,
                                                              asset_code,
                                                              all_commits)
    asset_finder.search(id=added_res[1], path=added_res[2])

    yield ('A', added_commit, added_res[2])

    for commit in all_commits:
        res = asset_finder.test(commit.tree)
        if res is None:
            res2, commit = find_asset_by_code(asset_finder, asset_code,
                                              all_commits)
            asset_finder.search(id=res2[1], path=res2[2])

            if old_res[2] != res2[2]:
                yield ('R', commit, (old_res[2], res2[2]))
            else:
                yield ('M', commit, (old_res[1], res2[1]))

            old_res = res2


def command(args):
    import datetime
    import os
    import textwrap

    import pygit2

    from sr.tools.environment import get_terminal_size
    from sr.tools.inventory.inventory import assetcode, get_inventory

    inventory = get_inventory()
    repo = pygit2.Repository(inventory.root_path)

    asset_code = 'sr{}'.format(assetcode.normalise(args.asset_code))

    for event in get_history(repo, asset_code):
        status = event[0]
        commit = event[1]

        if args.output == 'commits':
            print(commit.id)
        else:
            description = ''
            if status == 'A':
                description = "'{}' created.".format(event[2])
            elif status == 'R':
                old_path = event[2][0]
                new_path = event[2][1]
                description = "Moved from '{}' into '{}'." \
                              .format(os.path.dirname(old_path),
                                      os.path.dirname(new_path))
            elif status == 'M':
                description = 'Contents modifed.'
            else:
                description = 'Something happened.'

            terminal_width, terminal_height = get_terminal_size()

            if args.output == 'full':
                print('Commit {} by {} on {}'.format(
                    commit.id,
                    commit.committer.name,
                    datetime.datetime.fromtimestamp(commit.commit_time)
                ))

                for line in textwrap.wrap(description, width=terminal_width-2):
                    print(' ', line)
                print()
            else:
                print(description)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-history',
                                   help='Get the history of an asset.')
    parser.add_argument('asset_code', help='The code of the asset to inspect.')
    parser.add_argument('--output', '-o',
                        choices=['commits', 'description', 'full'],
                        default='full')
    parser.set_defaults(func=command)
