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

import sys
import unittest
from unittest.mock import patch

from . import ast, int

import io


class TestInt(unittest.TestCase):
    def test_one(self):
        prg1 = "x := 10"
        # test parser
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        self.assertIsNotNone(st)
        # x is defined
        self.assertIn("x", st.env)
        # x is 10
        self.assertEqual(st.env["x"], 10)
        # no other variables in the state
        self.assertEqual(len(st.env), 1)
    
    def test_Stmt_equal(self):
        prg1 = "x:=10; y:=20"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        self.assertIsNotNone(st)
        # x is defined
        self.assertIn("x", st.env)
        self.assertEqual(st.env["x"], 10)
        # x is defined
        self.assertIn("y", st.env)
        self.assertEqual(st.env["y"], 20)
        self.assertEqual(len(st.env), 2)


        prg2 = "x:=10; y:=20"
        ast2 = ast.parse_string(prg2)
        self.assertEqual(ast1,ast2)

    def test_repr(self):
        prg1 = "x:=20; z:=1;print_state"        
        ast1 = ast.parse_string(prg1)
        output_prg1 = repr(ast1)
        self.assertEqual('{\n  x := 20;\n  z := 1;\n  print_state\n}', output_prg1)
        print(output_prg1)
    def test_repr_int(self):
        prg1 = "x:=20"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        test_repr=repr(st)
        test_str =str(st)
        self.assertEqual('{\'x\': 20}', test_repr)
        self.assertEqual('x: 20\n', test_str)
    
    def testskip(self):
        prg1 = "skip"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        self.assertIsNotNone(st)
        prg2 = "skip"
        ast2 = ast.parse_string(prg2)
        self.assertEqual(ast1,ast2)
    def test_print(self):
        prg1 = "print_state"
        ast1 = ast.parse_string(prg1)
        prg2 = "print_state"
        ast2 = ast.parse_string(prg2)
        self.assertEqual(ast1,ast2)
    def test_if(self):
        prg1 = "if 2<3 then x:=1 else x:=2"        
        ast1 = ast.parse_string(prg1)
        prg2 = "if 2<3 then x:=1 else x:=2"
        ast2 = ast.parse_string(prg2)
        self.assertEqual(ast1,ast2)
    def test_vistIntVarandrelExp(self):
        prg1 = "x:=2; if x < 2 then x:=4"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        prg2 = "x:=2; if x <= 2 then x:=4; if x=4 then x:=5; if x>=3 then x:=7; if x>7 then x:=9; if x<9 then x:=10 else x:=8"
        ast2 = ast.parse_string(prg2)
        
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast2, st)

    def test_Bexp(self):
        prg1 = "if (not false) and true then x:=2"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    def test_Bexp(self):
        prg1 = "if (not false) or true then x:=2"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    def test_vist_Aexp(self):
        prg1 = "x:=2+10+10-2+10*5+10/5"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    def test_visit_PrintStateStmt(self):
        prg1 = "print_state"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    def test_visit_If(self):
        prg1 = "x:=1; if x<1 then x:=3 else x:=4"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    def test_visit_while(self):
        prg1 = 'x:=1; while x<=2 do x:=x+1'   
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st) 
    def test_vistBxp(self):
        prg1 = 'x:=4; if (x=4) and true then x:=5'
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st) 

    def test_visit_Assert(self):
        prg1 = 'x:=1; assert x<2; assume x=1'
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    
    def test_visit_Assert2(self):
        prg1 = 'x:=1; assert x>2;skip'
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)

    def test_havoc(self):
        prg1 = 'havoc x:=1'
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        prg2 = 'havoc x:=2'
        ast2 = ast.parse_string(prg2)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast2, st)
        self.assertEqual(ast1,ast2)
        

    def test_whileStmt(self):
        prg1 = 'x:=1; while x<=2 do x:=x+1'   
        ast1 = ast.parse_string(prg1)
        prg2 = 'x:=1; while x<=2 do x:=x+1'   
        ast2 = ast.parse_string(prg2)
        self.assertEqual(ast1,ast2)
    
    def test_AssertStmt(self):
        prg1 = 'x:=1; assert x>2;skip'
        ast1 = ast.parse_string(prg1)
        prg2 = 'x:=1; assert x>2;skip'
        ast2 = ast.parse_string(prg2)
        self.assertEqual(ast1,ast2)
    
    def test_AssumeStmt(self):
        prg1 = 'assume 1 < 2'
        ast1 = ast.parse_string(prg1)
        prg2 = 'assume 1 < 2'
        ast2 = ast.parse_string(prg2)
        self.assertEqual(ast1,ast2)

    def test_const(self):
        ast1=ast.Const(5)
        print(ast1)
        ast1.__repr__()
        ast1.__str__()
        ast1.__hash__()

    def test_INTVAR(self):
        ast1=ast.IntVar("x")
        print(ast1)
        ast1.__repr__()
        ast1.__str__()
        ast1.__hash__()
    def test_AssumeStmt(self):
        prg1 = "y:=2; assume (y<3)"
        ast1 = ast.parse_string(prg1)
        print(ast1)
    def test_havocStmt(self):
        prg1 = "y:=2; havoc y<3"
        ast1 = ast.parse_string(prg1)
        print(ast1)
    
    def test_ifandwhileStmt(self):
        prg1 = "x:=1; while x<=2 do x:=x+1; if x<=1 then x:= x+1 else x:=x+2;skip"
        ast1 = ast.parse_string(prg1)
        print(ast1)
    
    def test_bool(self):
        node = ast.BoolConst('true')
        as1=ast.PrintVisitor()
        as2=as1.visit_BoolConst(node)

    def test_bool2(self):
        node = ast.BoolConst('')
        as1=ast.PrintVisitor()
        as2=as1.visit_BoolConst(node)



    """
    def test_Exp(self):
        ast1=ast.Exp("not")
    """

   

        
    @patch('sys.argv', ['wlang.int', 'wlang/test1.prg'])
    def test_main(self):
        self.assertEqual(int.main(),0)


