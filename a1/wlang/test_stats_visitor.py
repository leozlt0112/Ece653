import unittest
from unittest.mock import patch

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
        prg3 = "x:=4;if x<2 then x:=2 else x:=1; havoc x=1"
        ast3 = ast.parse_string(prg3)
        sv3 = stats_visitor.StatsVisitor()
        sv3.visit(ast3)

        prg4 = "x:=1;assume x=1; assert x=1"
        sv4 = stats_visitor.StatsVisitor()
        ast4 = ast.parse_string(prg4)
        sv4.visit(ast4)

        prg5 = "x:=2; while x>=1 do x:=x-1; print_state"
        ast5 = ast.parse_string(prg5)
        sv5 = stats_visitor.StatsVisitor()
        sv5.visit(ast5)

        prg6= "x:=4;if x<2 then x:=2; havoc x=1"
        ast6 = ast.parse_string(prg6)
        sv6 = stats_visitor.StatsVisitor()
        sv6.visit(ast6)
        """s"""
        aststmtlist=ast.StmtList(None)
        statsvisit=stats_visitor.StatsVisitor()
        statsvisit.visit_StmtList(aststmtlist)
        self.assertEqual(sv.get_num_stmts(), 2)
        self.assertEqual(sv.get_num_vars(), 1)
        self.assertEqual(sv2.get_num_stmts(), 5)
        self.assertEqual(sv2.get_num_vars(), 2)
        self.assertEqual(sv3.get_num_vars(), 1)
        self.assertEqual(sv3.get_num_stmts(), 5)
        self.assertEqual(sv4.get_num_stmts(),3)
        self.assertEqual(sv4.get_num_vars(),1)
        self.assertEqual(sv5.get_num_vars(),1)
        self.assertEqual(sv5.get_num_stmts(),4)
        self.assertEqual(sv6.get_num_stmts(),4)
        self.assertEqual(sv6.get_num_vars(),1)


        # UNCOMMENT to run the test
    @patch('sys.argv', ['wlang.stats_visitor', 'wlang/test1.prg'])
    def test_main(self):
        stats_visitor.main()
        
        
        




        
