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
        self._undefined_variables = set()
        self._defined_variables = set()

    def check(self, node):
        """Check for undefined variables starting from a given AST node"""
        self._defined_variables = set()  # Reset defined variables for each check
        self._undefined_variables = set()  # Reset undefined variables for each check
        self.visit(node)

    def get_undefs(self):
        """Return the set of all variables that are used before being defined
        in the program. Available only after a call to check()
        """
        return self._undefined_variables

    def visit_StmtList(self, node, *args, **kwargs):
        if node.stmts is None:
            return
        for s in node.stmts:
            self.visit(s, *args, **kwargs)

    def visit_IntVar(self, node, *args, **kwargs):
        if node not in self._defined_variables:
            self._undefined_variables.add(node)

    def visit_Const(self, node, *args, **kwargs):
        pass

    def visit_Stmt(self, node, *args, **kwargs):
        pass

    def visit_AsgnStmt(self, node, *args, **kwargs):
        self.visit(node.rhs, *args, **kwargs)
        self._defined_variables.add(node.lhs)

    def visit_Exp(self, node, *args, **kwargs):
        for arg in node.args:
            self.visit(arg, *args, **kwargs)

    def visit_HavocStmt(self, node, *args, **kwargs):
        for var in node.vars:
            self._defined_variables.add(var)

    def visit_AssertStmt(self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)

    def visit_AssumeStmt(self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)

    def visit_IfStmt(self, node, *args, **kwargs):
        defined_variables_before_then = set(self._defined_variables)
        """ x"""
        to_be_added = set()
        """ """
        self.visit(node.then_stmt)
        defined_variables_after_then = self._defined_variables.difference(defined_variables_before_then)
        """y """
        self.visit(node.cond)
        if node.has_else():
            """x y """
            self.visit(node.else_stmt)
            if (self._defined_variables == (defined_variables_after_then.union(defined_variables_before_then))):
                after_else = self._defined_variables - defined_variables_before_then
            else: 
                after_else = self._defined_variables-(defined_variables_after_then.union(defined_variables_before_then))

            to_be_added = defined_variables_after_then.intersection(after_else)
            """z ^ y"""

        self._defined_variables = defined_variables_before_then.union(to_be_added)

    def visit_WhileStmt(self, node, *args, **kwargs):
        self.visit(node.cond)