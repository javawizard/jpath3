
def init(*names):
    def __init__(self, *args):
        if len(names) != len(args):
            raise Exception("Required " + len(names) + "args but got " + len(args)
                    + " for constructor for " + str(type(self)))
        for name, arg in zip(names, args):
            setattr(self, name, arg)
    __init__.__doc__ = "__init__(%s)" % ", ".join(names)
    return __init__


class Production(object):
    pass


class NumberLiteral(Production):
    __init__ = init("value")


class StringLiteral(Production):
    __init__ = init("value")
    
    def evaluate(self, static, dynamic, local):
        return None


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


class Satisfies(Production):
    __init__ = init("type", "name", "expr", "condition")



















































