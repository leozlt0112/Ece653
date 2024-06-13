# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from . import ast


class UndefVisitor(ast.AstVisitor):
    """Computes all variables that are used before being defined"""

    def __init__(self):
        super(UndefVisitor, self).__init__()
        self._undefined_variables=set()
        self._defined_variables=set()
        pass

    def check(self, node):
        """Check for undefined variables starting from a given AST node"""
        # do the necessary setup/arguments and call self.visit (node, args)
        # self.defined_variables = set()
        self._defined_variables=set()
        print("defined\n", self._defined_variables)
        print("undefined\n", self._undefined_variables)
        self.visit(node)
        

    def get_undefs(self):
        return self._undefined_variables()
        """Return the set of all variables that are used before being defined
        in the program.  Available only after a call to check()
        """

    def visit_StmtList(self, node, *args, **kwargs):
        if node.stmts is None:
            return 
        else:
            for s in node.stmts:
                self.visit(s)

    def visit_IntVar(self, node, *args, **kwargs):
        if node not in self._defined_variables():
            self._undefined_variables.add(node)

    def visit_Const(self, node, *args, **kwargs):
        pass

    def visit_Stmt(self, node, *args, **kwargs):
        pass

    def visit_AsgnStmt(self, node, *args, **kwargs):
        self.visit(node.rhs)
        self.defined_variables.add(node.lhs) 
        

    def visit_Exp(self, node, *args, **kwargs):
        for arg in node.args:
            self.visit(arg)

    def visit_HavocStmt(self, node, *args, **kwargs):
        for var in node.vars:
            self.defined_variables.add(var)

    def visit_AssertStmt(self, node, *args, **kwargs):
        
        pass

    def visit_AssumeStmt(self, node, *args, **kwargs):
        pass

    def visit_IfStmt(self, node, *args, **kwargs):
        pass

    def visit_WhileStmt(self, node, *args, **kwargs):
        pass
