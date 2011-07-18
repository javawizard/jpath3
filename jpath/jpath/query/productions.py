
def init(*names):
    def __init__(self, *args):
        if len(names) != len(args):
            raise Exception("Required " + str(len(names)) + " args but got " + 
                    str(len(args)) + " for constructor for " + str(type(self)))
        for name, arg in zip(names, args):
            setattr(self, name, arg)
    __init__.__doc__ = "__init__(%s)" % ", ".join(names)
    __init__.names = names
    return __init__


class Production(object):
    def __str__(self):
        if getattr(self. __init__, "names", None) is None:
            raise NotImplementedError
        names = self.__init__.names
        return type(self).__name__ + "(" + ", ".join(
                repr(getattr(self, v)) for v in names) + ")"
    
    def __repr__(self):
        return self.__str__()


class NumberLiteral(Production):
    __init__ = init("value")


class StringLiteral(Production):
    __init__ = init("value")
    
    def evaluate(self, static, dynamic, local):
        return None


class BooleanLiteral(Production):
    __init__ = init("value")


class NullLiteral(Production):
    __init__ = init()


class VarReference(Production):
    __init__ = init("name")


class FunctionCall(Production):
    __init__ = init("name", "args")


class Pattern(Production):
    __init__ = init("value")


class PairPattern(Production):
    __init__ = init("value")


class ContextItem(Production):
    __init__ = init()


class Children(Production):
    __init__ = init()


class PairChildren(Production):
    __init__ = init()


class ParenExpr(Production):
    __init__ = init("expr")


class ListConstructor(Production):
    __init__ = init("expr")


class EmptyListConstructor(Production):
    __init__ = init()


class ObjectConstructor(Production):
    __init__ = init("expr")


class EmptyObjectConstructor(Production):
    __init__ = init()


class EmptySequenceConstructor(Production):
    __init__ = init()


class XMLTag(Production):
    __init__ = init("name", "attributes", "contents")


class XMLAttribute(Production):
    __init__ = init("name", "value")


class Indexer(Production):
    __init__ = init("expr")


class PairIndexer(Production):
    __init__ = init("expr")


class Multiply(Production):
    __init__ = init("left", "right")


class Divide(Production):
    __init__ = init("left", "right")


class Add(Production):
    __init__ = init("left", "right")


class Subtract(Production):
    __init__ = init("left", "right")


class Otherwise(Production):
    __init__ = init("left", "right")


class GreaterOrEqual(Production):
    __init__ = init("left", "right")


class LessOrEqual(Production):
    __init__ = init("left", "right")


class Greater(Production):
    __init__ = init("left", "right")


class Less(Production):
    __init__ = init("left", "right")


class NotEqual(Production):
    __init__ = init("left", "right")


class Equal(Production):
    __init__ = init("left", "right")


class And(Production):
    __init__ = init("left", "right")


class Or(Production):
    __init__ = init("left", "right")


class PairConstructor(Production):
    __init__ = init("left", "right")


class SequenceConstructor(Production):
    __init__  = init("exprs")


class IfThenElse(Production):
    __init__  = init("condition", "true", "false")


class Quantifier(Production):
    __init__ = init("type", "name", "expr", "condition")


class FlworFor(Production):
    __init__ = init("var", "counter", "expr")


class FlworLet(Production):
    __init__ = init("var", "expr")


class FlworWhere(Production):
    __init__ = init("expr")


class FlworOrderBy(Production):
    __init__ = init("expr")


class FlworAt(Production):
    __init__ = init("var")


class FlworDo(Production):
    __init__ = init("expr")


class Flwor(Production):
    __init__  = init("constructs", "return_expr")


class Insert(Production):
    __init__ = init("expr", "position")


class Delete(Production):
    __init__ = init("expr")


class Replace(Production):
    __init__ = init("target", "source")


class FunctionDefArg(Production):
    __init__ = init("type", "name", "default")


class FunctionDef(Production):
    __init__ = init("name", "args", "expr")


class Import(Production):
    __init__ = init("type", "source", "target")


class Option(Production):
    __init__ = init("name", "value")


class Module(Production):
    __init__ = init("prolog", "functions", "expr")



















































