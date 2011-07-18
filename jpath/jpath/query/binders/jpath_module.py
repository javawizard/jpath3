from jpath.query import binder, syntax, jpath_module
from jpath.fileutils import File
import os

class JPathBinder(binder.Binder):
    default_name = "jpath"
    
    def __init__(self):
        self.modules = {}
        self.paths = []
        self.interpreter = None
    
    def set_interpreter(self, interpreter):
        self.interpreter = interpreter
    
    def add_path(self, path):
        if path.endswith("/"):
            path = path[:-1]
        if path not in self.paths:
            self.paths.append(path)
    
    def bind_module(self, path):
        if path in self.modules:
            return self.modules[path]
        # Module has not yet been loaded, so we need to do that now.
        if not self.paths:
            raise Exception("No paths have been specified for this instance "
                    "of JPathBinder. If you just created a new Interpreter "
                    "object and tried to get it to load a JPath module, you "
                    'need to call interpreter.get_binder("jpath").add_path'
                    '("/some/folder") to tell the interpreter where to look '
                    "for JPath modules on the filesystem.")
        if not path.startswith("/"):
            raise Exception("JPath module paths must start with a / right "
                    "now. Relative imports will be allowed at some point in "
                    "the future.")
        file = None
        for search_path in self.paths:
            folder = File(search_path)
            test_file = folder.child(path[1:]) # [1:] to get rid of the leading /
            if test_file.is_file:
                file = test_file
                break
        if not file:
            raise Exception('Module "' + path + '" could not be found on the '
                    "search path.")
        # We've found the module file. Now we read it in and parse it.
        with file.open() as file_reader:
            contents = file_reader.read()
        parsed_module = syntax.module.parse_string(contents) #@UndefinedVariable
        # The module has been read in and is syntactically valid. Now we go
        # create a Module object for it.
        module = jpath_module.JPathModule(self.interpreter, path)
        # Now we add the module to our local registry of modules. It's
        # /imperative/ that we do this before initializing the module in case
        # the module contains circular imports. (If you don't believe me, try
        # adding it to the registry of modules /after/ initializing it, and
        # then try writing two modules that circularly import each other, and
        # see what happens.)
        self.modules[path] = module
        # Now we initialize it, and we're done!
        module.load(parsed_module)
        return module

































