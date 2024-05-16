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
        pass

    def check(self, node):
        """Check for undefined variables starting from a given AST node"""
        # do the necessary setup/arguments and call self.visit (node, args)
        pass

    def get_undefs(self):
        """Return the set of all variables that are used before being defined
        in the program.  Available only after a call to check()
        """
        pass

    def visit_StmtList(self, node, *args, **kwargs):
        pass

    def visit_IntVar(self, node, *args, **kwargs):
        pass

    def visit_Const(self, node, *args, **kwargs):
        pass

    def visit_Stmt(self, node, *args, **kwargs):
        pass

    def visit_AsgnStmt(self, node, *args, **kwargs):
        pass

    def visit_Exp(self, node, *args, **kwargs):
        pass

    def visit_HavocStmt(self, node, *args, **kwargs):
        pass

    def visit_AssertStmt(self, node, *args, **kwargs):
        pass

    def visit_AssumeStmt(self, node, *args, **kwargs):
        pass

    def visit_IfStmt(self, node, *args, **kwargs):
        pass

    def visit_WhileStmt(self, node, *args, **kwargs):
        pass
