from pyparsing import *
import query_ast

TRUE       = CaselessKeyword("true")
FALSE      = CaselessKeyword("false")
IN         = CaselessKeyword("in")
IS         = CaselessKeyword("is")
OR         = CaselessKeyword("or")
AND        = CaselessKeyword("and")
NOT        = CaselessKeyword("not")

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
ASSET_NAME = Regex(r"[a-zA-Z0-9\.\*\-\?\[\]]+")
PATH_RE    = Regex(r"[a-zA-Z0-9\.\*\-\?\[\]/]+")
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


# Parser actions, i.e. AST construction
def _pa_or_expr(x):
    if len(x) == 1:
        return x[0]
    return query_ast.Or(x[0], x[2])

def _pa_and_expr(x):
    if len(x) == 1:
        return x[0]
    if len(x) == 2:
        return query_ast.And(x[0], x[1])
    return query_ast.And(x[0], x[2])

code_single.setParseAction(lambda x: query_ast.Code(x[2]))
code_list.setParseAction(lambda x: query_ast.Code(*x[3::2]))
type_single.setParseAction(lambda x: query_ast.Type(x[2]))
type_list.setParseAction(lambda x: query_ast.Type(*x[3::2]))
cond_single.setParseAction(lambda x: query_ast.Condition(x[2]))
cond_list.setParseAction(lambda x: query_ast.Condition(*x[3::2]))
path_single.setParseAction(lambda x: query_ast.Path(x[2]))
path_list.setParseAction(lambda x: query_ast.Path(*x[3::2]))
label_expr.setParseAction(lambda x: query_ast.Labelled(x[2]))
or_expr.setParseAction(_pa_or_expr)
and_expr.setParseAction(_pa_and_expr)
not_expr.setParseAction(lambda x: query_ast.Not(x[1]))
paren_expr.setParseAction(lambda x: x[1])

def search_tree(query):
    return root.parseString(query)[0]

