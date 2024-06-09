import unittest

from . import ast, live


class TestStatsVisitor(unittest.TestCase):
    def test_one(self):
        prg1 = "x := 10; print_state"
        ast1 = ast.parse_string(prg1)

        v = live.StmtCounter1()
        v.visit(ast1)
        self.assertEqual(c,2)
        # UNCOMMENT to run the test
        #self.assertEqual(sv.get_num_stmts(), 2)
        #self.assertEqual(sv.get_num_vars(), 1)
