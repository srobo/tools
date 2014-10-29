"""
Queries
=======

Currently, there are 3 types of expressions: *equality/match*, *membership*
and *function*.  The equality/match expression takes the form
`KEY (':' | '=' | 'is') VALUE`.  The membership expression takes the form
`KEY 'in' '{' VALUE (',' VALUE)* '}'`.  The function expression takes the
form `FUNCTION 'of' EXPR`, where `EXPR` is another valid expression.


Supported keys
--------------

### Code:

Match on a part code.

* *Keys:* `code`
* *Values:* *a valid SR part code, with or without the `sr` prefix*
* *Example:* `code:srEEN`


### Serial:

Match on a serial number.

* *Keys:* `serial`
* *Values:* *a valid serial number*
* *Example:* `serial:D851F850`


### Condition:

Match on the condition of a part/assembly.  An assembly is considered `working`
if and only if all expected sub-parts are considered `working`.  If any
sub-part is `broken` or missing, the assembly is `broken`.  If any sub-part is
`unknown` and the assembly is not `broken` then the assembly is `unknown`.

* *Keys:* `condition`, `cond`
* *Values:* `working`, `unknown`, `broken`
* *Example:* `condition is working`


### Labelled:

Match based on how labelled a part is.

* *Keys:* `labelled`
* *Values:* `true`, `false`
* *Example:* `labelled=true`


### Type or name of part:

Match on the name of a part/assembly.  Python's `fnmatch` is used, and it uses
glob-like syntax.  Basic usage: '`*`' matches any character, any number of
times; `?` matches a single character; `[ab]` matches one of the characters
`a` or `b`.

* *Keys:* `type`
* *Values:* *a glob-like pattern*
* *Examples:* `type:power*`, for all parts whose name begins with 'power'


### Path:

Match on the path to the part in the inventory.  Python's `fnmatch` is used here
too, but with an implicit `*` at the end.  This makes path searching more
intuitive.

* *Keys:* `path`
* *Values:* *a valid glob-like pattern*
* *Example:* `path:vault`, for all parts under any path, relative to the
inventory root, that begins with '`vault`'


### Assembly:

Match based on whether a part/assembly is an assembly or not.

* *Keys:* `assy`
* *Values:* `true`, `false`
* *Example:* `assy:true`



Logic
-----

`AND`, `OR`, and `NOT` are all supported.  `NOT` may be abreviated to `!`.
When two expressions appear side-by-side with no operator (`AND`, or `OR`)
between them, `AND` is assumed, e.g. `a b` is equivalent to `a AND b`.
These keywords are not case insensitive.

One may also use parenthetic expressions.



Function Expressions
--------------------

Function expressions currently allow one to *map* the list of matches (from
the input expression) using some named function.  The current functions are:
`parent`, `siblings`, `children`, and `descendants`.  For example,
`parent of type:power-board-sr13.f` will return the parent nodes of sr13
power boards.  (Note that this particular example doesn't guarantee the
parents are assemblies, they could be boxes for example.  One can fix this
by adding `assy:true`.)  Function expressions bind tighter than `AND`, so
`parent of type:power-board-sr13.f AND assy:true`, with parentheses for clarity,
means `(parent of type:power-board-sr13.f) AND assy:true`.



Examples
--------

* `cond:working` - returns all working parts and assemblies.

* `type is *power*` - returns parts that match that glob pattern (power boards
  and assys, power supplies, etc...).

* `!path:vault` - returns items not under paths starting with `vault`.

* `path:vault !cond:working` - returns the things in the vault that are not
  `working` (note the implicit `AND`).

* `cond:working AND (path:bees OR path:face)` - returns working things in
  `bees*` or in `face*`.  This could be simplified with the membership syntax:
  `cond:working AND path in {bees*, face*}`

* `type in {motor-board-sr11.f, motor-board-sr13.f}` - returns all of our motor
  boards.  In this case, a glob pattern could be used to shorten it:
  `type:motor-board-sr1[13].f`.

* `descendants of code:srBOX and cond:broken` - return all the broken things
  in srBOX.

* `siblings of code:srABC` - things at the same level in the hierarchy as srABC.

"""
import sys

import sr.tools.inventory.inventory as inventory
import sr.tools.inventory.oldinv as oldinv
import sr.tools.inventory.query_parser as query_parser

def _get_inv():
    top = oldinv.gettoplevel()
    if top is None:
        print("Error: Must be run from within the inventory.", file=sys.stderr)
        exit(1)
    return inventory.Inventory(top).root

def query(query_str, inv=None):
    if inv is None:
        inv = _get_inv()
    tree = query_parser.search_tree(query_str)
    return tree.match(inv.parts.values())
