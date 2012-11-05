from pyparsing import *

TRUE       = Keyword("true")
FALSE      = Keyword("false")
IN         = Keyword("in")
IS         = Keyword("is")
OR         = Keyword("or")
AND        = Keyword("and")
NOT        = Keyword("not")

EQUALS     = Literal("=")
COLON      = Literal(":")
L_C_BRKT   = Literal("{")
R_C_BRKT   = Literal("}")
L_BRKT     = Literal("(")
R_BRKT     = Literal(")")
COMMA      = Literal(",")

EQUALITY   = Or((EQUALS, COLON, IS))

CODE       = Literal("code")
TYPE       = Literal("type")
COND       = Or((Literal("condition"), Literal("cond")))
LABELLED   = Literal("labelled")
PATH       = Literal("path")

ASSET_CODE = Regex(r"(sr)?[a-zA-Z0-9]+")
ASSET_NAME = Regex(r"[a-z0-9\.\*\-\?\[\]]+")
PATH_RE    = Regex(r"[a-zA-Z0-9-\./]+")
CONDITIONS = oneOf("working unknown broken")

def generate_in_expr(prop, val_type):
    return (prop + IN + L_C_BRKT +
            val_type + ZeroOrMore(COMMA + val_type) +
            R_C_BRKT)

code_single = CODE + EQUALITY + ASSET_CODE
code_list   = generate_in_expr(CODE, ASSET_CODE)
code_expr   = code_list | code_single

type_single = TYPE + EQUALITY + ASSET_NAME
type_list   = generate_in_expr(TYPE, ASSET_NAME)
type_expr   = type_list | type_single

cond_single = COND + EQUALITY + CONDITIONS
cond_list   = generate_in_expr(COND, CONDITIONS)
cond_expr   = cond_list | cond_single

path_single = PATH + EQUALITY + PATH_RE
path_list   = generate_in_expr(PATH, PATH_RE)
path_expr   = path_list | path_single

label_expr  = LABELLED + EQUALITY + Or((TRUE, FALSE))

or_expr     = Forward()
and_expr    = Forward()
not_expr    = Forward()
primary     = Forward()

base_expr   = (not_expr | code_expr | type_expr | cond_expr |
               path_expr | label_expr)
paren_expr  = L_BRKT + or_expr + R_BRKT
primary     << (base_expr | paren_expr)

and_expr    << (primary + Optional(AND) + and_expr | primary)
or_expr     << (and_expr + OR + or_expr | and_expr)
not_expr    << NOT + primary

root        = or_expr


def search_tree(query):
    return root.parseString(query)[0]

