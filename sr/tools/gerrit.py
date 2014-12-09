import json
import subprocess

from sr.tools.config import Config


def cmd(args):
    """Run the given gerrit command and return the response."""
    conf = Config()
    c = ["ssh", conf["gerrit_ssh"], "gerrit"] + args
    return subprocess.check_output(c)


def query(**conditions):
    """Perform a gerrit query."""
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
