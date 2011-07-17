
from jpath.query import syntax

tail = ["number", "alphanum", "alpha", "digit", "upper", "lower"]

if __name__ == "__main__":
    print "Enter a .png filename where syntax diagrams will be written to"
    name = raw_input()
    if not name[-4:] == ".png":
        raise Exception("That doesn't end with .png")
    syntax.module.draw_productions_to_png({}, name, tail=tail) #@UndefinedVariable
    print "done"
    