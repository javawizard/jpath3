
from jpath.query import interpreter
import sys


def run(script, paths):
    i = interpreter.Interpreter()
    


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "You need to specify the name of a JPath script to run and any "
        print "lookup paths"
        sys.exit()
    run(sys.argv[1], sys.argv[2:])