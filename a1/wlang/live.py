from . import ast

def main():
    """
    x 1
    if 2 
    z 3 
    print 4
    """
    ast1 = ast.parse_string('x := 10 ; {if x > 5 then y:= 20 else y:=1} ; z:= x+y ; print_state')
    print(ast1)
    print(type(ast1.stmts))

    print("This program has:", len(list(ast1.stmts)), "statements")
class StmtCounter1(ast.AstVisitor):
    def __int__(self):
        super().__init__()

    def visit_StmtList(self, node, *args, **kargs):
        res = 0
        for s in node.stmts:
            res+= self.visit(s,*args,**kargs)
        return res
    def visit_IfStmt(self,node,*args,**kargs):
        res =self.visit_Stmt(self,node,*args, **kargs)
        res += self.visit(node.then_stmt, *args, **kargs)
        res += self.visit(node.else_stmt, *args, **kargs)
        return res
    def visit_Stmt(self, node, *args, **kwargs):
        return 1
        

if __name__ == '__main__':
    main()