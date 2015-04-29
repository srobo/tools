import json
import subprocess

from sr.tools.config import Config


def cmd(args):
    """
    Run the given Gerrit command and return the response.

    This will get the Gerrit SSH host from the configuration file.

    :param list args: The arguments to run on Gerrit.
    :returns: The contents from the result.
    """
    conf = Config()
    c = ["ssh", conf["gerrit_ssh"], "gerrit"] + args
    return subprocess.check_output(c, universal_newlines=True).strip()


def query(**conditions):
    """
    Perform a Gerrit query.

    :param conditions: The conditions of the query.
    :returns: A list of results from the query.
    :rtype: list of dicts
    """
    args = ["query", "--format", "json"]
    for vname, val in conditions.items():
        args.append("{0}:{1}".format(vname, val))

    resp = cmd(args)

    results = []
    # query returns a series of json docs with one-to-a-line
    # the last entry contains stats about the query's execution
    for l in resp.splitlines()[:-1]:
        results.append(json.loads(l))

    return results
