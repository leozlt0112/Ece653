import unittest

from . import ast, stats_visitor


class TestStatsVisitor(unittest.TestCase):
    def test_one(self):
        prg1 = "x := 10; print_state"
        ast1 = ast.parse_string(prg1)

        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        prg2 = "x := 10; if x > 10 then y := 10 else y:=5; print_state"
        ast2 = ast.parse_string(prg2)
        sv2 = stats_visitor.StatsVisitor()
        sv2.visit(ast2)
        prg3 = "x:=4;if x<2 then x:=2 else x:=1"
        ast3 = ast.parse_string(prg3)
        sv3 = stats_visitor.StatsVisitor()
        sv3.visit(ast3)

        # UNCOMMENT to run the test
        self.assertEqual(sv.get_num_stmts(), 2)
        self.assertEqual(sv.get_num_vars(), 1)
        print("\nsv2", sv2.get_num_stmts(),"\n")
        print("\nsv3", sv3.get_num_stmts(),"\n")

        
