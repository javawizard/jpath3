
from jpath.query import data as d, utils
import operator

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
    def evaluate(self, static, dynamic, local):
        raise NotImplementedError
    
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
    
    def evaluate(self, static, dynamic, local):
        return d.StandardSequence([d.StandardNumber(self.value)])


class StringLiteral(Production):
    __init__ = init("value")
    
    def evaluate(self, static, dynamic, local):
        return d.StandardSequence([d.StandardString(self.value)])


class BooleanLiteral(Production):
    __init__ = init("value")
    
    def evaluate(self, static, dynamic, local):
        return d.StandardSequence([d.StandardBoolean(self.value)])


class NullLiteral(Production):
    __init__ = init()
    
    def evaluate(self, static, dynamic, local):
        return d.StandardSequence([d.StandardNull()])


class VarReference(Production):
    __init__ = init("name")
    
    def evaluate(self, static, dynamic, local):
        return local.get_var(self.name)


class FunctionCall(Production):
    __init__ = init("name", "args")


class Pattern(Production):
    __init__ = init("value")
    
    def evaluate(self, static, dynamic, local):
        return dynamic.context_item.get_for_pattern(self.value)


class PairPattern(Production):
    __init__ = init("value")
    
    def evaluate(self, static, dynamic, local):
        return dynamic.context_item.get_for_pair_pattern(self.value)


class ContextItem(Production):
    __init__ = init()
    
    def evaluate(self, static, dynamic, local):
        return d.StandardSequence([dynamic.context_item])


class Children(Production):
    __init__ = init()
    
    def evaluate(self, static, dynamic, local):
        return dynamic.context_item.get_children()


class PairChildren(Production):
    __init__ = init()
    
    def evaluate(self, static, dynamic, local):
        return dynamic.context_item.get_pair_children()


class ParenExpr(Production):
    __init__ = init("expr")
    
    def evaluate(self, static, dynamic, local):
        return self.expr.evaluate(static, dynamic, local)


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
    
    def evaluate(self, static, dynamic, local):
        return d.StandardSequence([])


class XMLTag(Production):
    __init__ = init("name", "attributes", "contents")


class XMLAttribute(Production):
    __init__ = init("name", "value")


class Indexer(Production):
    __init__ = init("expr")
    
    def evaluate(self, static, dynamic, local):
        return dynamic.context_item.get_for_indexer(self.expr.evaluate(static, dynamic, local))


class PairIndexer(Production):
    __init__ = init("expr")
    
    def evaluate(self, static, dynamic, local):
        return dynamic.context_item.get_for_pair_indexer(self.expr.evaluate(static, dynamic, local))


class Path(Production):
    __init__ = init("left", "right")
    
    def evaluate(self, static, dynamic, local):
        sequence = self.left.evaluate(static, dynamic, local)
        # TODO: need to change this to take into account if the above sequence
        # is synthetic, and if so, avoid stuffing all the items into a list
        sequence_size = sequence.get_size()
        results = [None for s in xrange(sequence_size)]
        for i in xrange(sequence_size):
            item = sequence.get_item(i)
            new_dynamic = dynamic.new(context_size=sequence_size, context_item=item, context_position=i + 1)
            results[i] = self.right.evaluate(static, new_dynamic, local)
        return utils.flatten(results)


class Predicate(Production):
    __init__ = init("left", "right")
    
    def evaluate(self, static, dynamic, local):
        # TODO: same thing about synthetic lists as with Path
        sequence = self.left.evaluate(static, dynamic, local)
        sequence_size = sequence.get_size()
        results = [None for s in xrange(sequence_size)]
        for i in xrange(sequence_size):
            item = sequence.get_item(i)
            new_dynamic = dynamic.new(context_size=sequence_size, context_item=item, context_position=i + 1)
            if utils.boolean(self.right.evaluate(static, new_dynamic, local)):
                results[i] = item
        return d.StandardSequence([x for x in results if x is not None])


class Multiply(Production):
    __init__ = init("left", "right")
    
    def evaluate(self, static, dynamic, local):
        left = self.left.evaluate(static, dynamic, local)
        right = self.right.evaluate(static, dynamic, local)
        return utils.binary_numeric(left, right, operator.mul)


class Divide(Production):
    __init__ = init("left", "right")
    
    def evaluate(self, static, dynamic, local):
        left = self.left.evaluate(static, dynamic, local)
        right = self.right.evaluate(static, dynamic, local)
        return utils.binary_numeric(left, right, operator.div)


class Add(Production):
    __init__ = init("left", "right")
    
    def evaluate(self, static, dynamic, local):
        left = self.left.evaluate(static, dynamic, local)
        right = self.right.evaluate(static, dynamic, local)
        return utils.binary_numeric(left, right, operator.add)


class Subtract(Production):
    __init__ = init("left", "right")
    
    def evaluate(self, static, dynamic, local):
        left = self.left.evaluate(static, dynamic, local)
        right = self.right.evaluate(static, dynamic, local)
        return utils.binary_numeric(left, right, operator.sub)


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
    __init__ = init("exprs")
    
    def evaluate(self, static, dynamic, local):
        return utils.flatten([p.evaluate(static, dynamic, local) for p in self.exprs])


class IfThenElse(Production):
    __init__ = init("condition", "true", "false")


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
    __init__ = init("constructs", "return_expr")


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
    __init__ = init("binder", "source", "target")


class Option(Production):
    __init__ = init("name", "value")


class Module(Production):
    __init__ = init("prolog", "functions", "expr")



















































