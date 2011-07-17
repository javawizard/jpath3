# coding=UTF-8

from parcon import (Literal, InfixExpr, SignificantLiteral, Forward, 
        number as p_number, Alphanum, CharNotIn, concat, alpha_chars, 
        digit_chars, CharIn, digit, Alpha, Upper, Lower, Optional, ZeroOrMore,
        Keyword, OneOrMore, flatten)
from jpath.query.productions import *
from collections import namedtuple

string_escape_map = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "'": "'"}

PathWrapper = namedtuple("PathWrapper", ("expr",))
PredicateWrapper = namedtuple("PredicateWrapper", ("expr",))

def keyword(text):
    return Keyword(Literal(text), CharNotIn(alpha_chars))


def lookup_string_escape(char):
    return string_escape_map[char]


def create_function_call((name, args)):
    if args is None:
        return FunctionCall(name, [])
    if isinstance(args, SequenceConstructor):
        return FunctionCall(name, args.exprs)
    return FunctionCall(name, [args])


def create_pattern_or_special(text):
    if text == "true":
        return BooleanLiteral(True)
    if text == "false":
        return BooleanLiteral(False)
    if text == "null":
        return NullLiteral()
    return Pattern(text)


def create_path(sequence):
    pass


upper = Upper()(name="upper")
lower = Lower()(name="lower")
alpha = (upper | lower)(name="alpha")
alphanum = (alpha | digit)(name="alphanum")

expr = Forward()

number = p_number[NumberLiteral]
string_escape = ("\\" + alphanum)[lookup_string_escape]
string_char = CharNotIn('"\\')(desc='any char except " or \\') | string_escape
string = ('"' + string_char[...][concat] + '"')(name="string")[StringLiteral]
var_name = ("$" + +(alphanum | CharIn("-_")))[concat](name="variable")
var_reference = var_name[VarReference]
function_name = (alpha + (alphanum | CharIn("-_."))[...])[concat](name="function name")
function_call = (function_name + "(" + Optional(expr, (None,)) + ")")[create_function_call](name="function call")
pattern = (alpha + (alphanum | CharIn("-_"))[...])[concat][create_pattern_or_special](name="pattern")
pair_pattern = ("@" + alpha + (alphanum | CharIn("-_"))[...])[concat][PairPattern](name="pair pattern")
context_item = Literal(".")[lambda t: ContextItem()](name="context item")
children = Literal("*")[lambda t: Children()](name="children")
pair_children = Literal("@*")[lambda t: PairChildren()](name="pair children")
paren_expr = ("(" + expr + ")")[ParenExpr](name="parens")
list_constructor = ("[" + expr + "]")[ListConstructor](name="list")
empty_list_constructor = (Literal("[") + "]")[lambda t: EmptyListConstructor()](name="empty list")
object_constructor = ("{" + expr + "}")[ObjectConstructor](name="object")
empty_object_constructor = (Literal("{") + "}")[lambda t: EmptyObjectConstructor()](name="empty object")
empty_sequence_constructor = (Literal("(") + ")")[lambda t: EmptySequenceConstructor()](name="empty sequence")

atom = (paren_expr | empty_list_constructor | list_constructor
       | empty_object_constructor | object_constructor
       | empty_sequence_constructor | number | string | var_reference
       | function_call | pattern | pair_pattern | context_item | children
       | pair_children)(name="atom")

indexer = ("#" + atom)[Indexer](name="indexer")
pair_indexer = ("@#" + atom)[PairIndexer](name="pair indexer")

infix = (pair_indexer | indexer | atom)(name="term")

infix = (atom + Optional(OneOrMore(
            ("/" + atom)[PathWrapper] |
            ("[" + expr + "]")[PredicateWrapper]
        ), []))[create_path](name="path")

infix = InfixExpr(infix, [
        ("×" | keyword("times") | keyword("mul"), Multiply),
        ("÷"| keyword("div") | (keyword("divided") + keyword("by")), Divide)
        ])

infix = InfixExpr(infix, [
        ("+" | keyword("plus") | keyword("add"), Add),
        ("-"| keyword("minus") | keyword("sub"), Subtract)
        ])

infix = InfixExpr(infix, [
            (keyword("otherwise"), Otherwise)
        ])

infix = InfixExpr(infix, [
            (">=", GreaterOrEqual),
            ("<=", LessOrEqual),
            (">", Greater),
            ("<", Less),
            ("!=", NotEqual),
            ("=", Equal),
        ])

infix = InfixExpr(infix, [
            (keyword("and"), And)
        ])

infix = InfixExpr(infix, [
            (keyword("or"), Or)
        ])

infix = InfixExpr(infix, [
            (":", PairConstructor)
        ])

infix = infix(name="infix")

infix = (infix + ("," + infix)[...])[flatten][SequenceConstructor](name="sequence")

if_then_else = (~keyword("if") + expr + ~keyword("then") + expr + ~keyword("else") + expr
        )[lambda (a, b, c): IfThenElse(a, b, c)](name="if")

satisfies = ((keyword("some") | keyword("every")) + var_name + ~keyword("in") + expr + ~keyword("satisfies") + expr
        )[lambda (a, b, c, d): Satisfies(a, b, c, d)](name="quantifier")

flwor_for = (~keyword("for") + var_name + Optional(~keyword("at") + var_name, "")
        + ~keyword("in") + expr)
flwor_let = (~keyword("let") + var_name + ":=" + expr)
flwor_where = (~keyword("where") + expr)
flwor_order_by = (~keyword("order") + ~keyword("by") + expr)
flwor_at = (~keyword("at") + var_name)
flwor_do = (~keyword("do") + expr)
flwor_return = (~keyword("return") + expr)
flwor_construct = (flwor_for | flwor_let | flwor_where | flwor_order_by | flwor_at | flwor_do)(name="flwor construct")
flwor = (+(flwor_construct) + flwor_return)(name="flwor")

expr << (if_then_else | satisfies | flwor | infix)(name="expr")

module = expr(name="module")




































