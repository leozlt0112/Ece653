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
        uv = undef_visitor.UndefVisitor()
        uv2 = undef_visitor.UndefVisitor()
        uv3 = undef_visitor.UndefVisitor()
        uv.check(ast1)
        uv2.check(ast2)
        uv3.check(ast3)

        # UNCOMMENT to run the test
        self.assertEqual (set([ast.IntVar('p'),ast.IntVar('w'),ast.IntVar('h'),ast.IntVar('z'),ast.IntVar('y')]), uv.get_undefs ())
        self.assertEqual (set([ast.IntVar('p')]), uv2.get_undefs ())
        self.assertEqual (set([ast.IntVar('p'),ast.IntVar('x')]), uv3.get_undefs ())
