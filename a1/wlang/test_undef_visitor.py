import unittest

from . import ast, undef_visitor


class TestUndefVisitor(unittest.TestCase):
    def test1(self):
        prg1 = "havoc x; if x > 10 then z := x + 1 else y := 10; z:=z+1;y:=y+2;if h > 10 then w := h + 1 else p := 10;x:=h+1;x:=w+1;x:=p+1; assert w <1; assume p<2; if x<9 then o:=1 else o:=2; x:=o+1"
        ast1 = ast.parse_string(prg1)
        prg2 = 'while p<10 do x:=x+1'
        ast2 = ast.parse_string(prg2)
        prg3 = 'while p<2 do x:=x+1;p:=x+1'
        ast3 = ast.parse_string(prg3)
        prg4 = 'skip;skip'
        ast4 = ast.parse_string(prg4)
        prg5 = 'x := 10; print_state'
        ast5 = ast.parse_string(prg5)
        prg6 =  'x := 10; if x > 10 then y := 10 else y:=5; print_state'
        ast6 =ast.parse_string(prg6)
        prg7 = "x:=1;assume x=1; assert x=1"
        ast7 =ast.parse_string(prg7)
        prg8 = "x:=2; while x>=1 do x:=x-1; print_state"
        ast8 =ast.parse_string(prg8)
        prg9= "x:=4;if x<2 then x:=2; havoc x=1"
        ast9 =ast.parse_string(prg9)

        visitor = undef_visitor.UndefVisitor()
        stmtlistex = ast.StmtList(s=None)
        visitor.visit_StmtList(stmtlistex)

        uv = undef_visitor.UndefVisitor()
        uv2 = undef_visitor.UndefVisitor()
        uv3 = undef_visitor.UndefVisitor()
        uv4 = undef_visitor.UndefVisitor()
        uv5 = undef_visitor.UndefVisitor()
        uv6 = undef_visitor.UndefVisitor()
        uv7 = undef_visitor.UndefVisitor()
        uv8 = undef_visitor.UndefVisitor()
        uv9 = undef_visitor.UndefVisitor()

        uv.check(ast1)
        uv2.check(ast2)
        uv3.check(ast3)
        uv4.check(ast4)
        uv5.check(ast5)
        uv6.check(ast6)
        uv7.check(ast7)
        uv8.check(ast8)
        uv9.check(ast9)


        # UNCOMMENT to run the test
        self.assertEqual (set([ast.IntVar('p'),ast.IntVar('w'),ast.IntVar('h'),ast.IntVar('z'),ast.IntVar('y')]), uv.get_undefs())
        self.assertEqual (set([ast.IntVar('p')]), uv2.get_undefs())
        self.assertEqual (set([ast.IntVar('p'),ast.IntVar('x')]), uv3.get_undefs())
        self.assertEqual (set(), uv4.get_undefs())
        self.assertEqual (set(), uv5.get_undefs())
        self.assertEqual (set(), uv6.get_undefs())
        self.assertEqual (set(), uv7.get_undefs())
        self.assertEqual (set(), uv8.get_undefs())
        self.assertEqual (set(), uv9.get_undefs())



