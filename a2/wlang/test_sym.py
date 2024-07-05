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

import unittest

from . import ast, sym


class TestSym (unittest.TestCase):
    def test_one(self):
        prg1 = "havoc x;while x < 10 do x:=x+1"        
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 11)
    def test_2(self):
        prg1 = "havoc x;while x<10 do x:=x+1; assert x<10; assume x>10"        
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 0)
    def test_4(self):
        prg1 = "if (not false) and true then x:=2"    
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)
    def test_5(self):
        prg1 = "if (not true) and false then x:=2"    
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)
    def test_6(self):
        prg1 = "if (not true) or false then x:=2"    
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)
    def test_7(self):
        prg1 = 'x:=4; if (x=4) and true then x:=5; if x=5 then x:=x-1; if x=4 then x:= x*2; if x=8 then x:= x/2;print_state;skip'
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)
    def test_8(self):
        prg1 = 'x:=4; assume x>2; if x <= 1 then x:=0 else x:=1; if x>= 0 then x:=1 else x:=9; x:=2; assume x>3; x:=1; assert x>0'
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 0)
    def test_9(self):
        prg1 = 'havoc x; assert x>2;y:=2;assert y<3; havoc z; if z>3 then z:=4 else z:=5'
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out),2)
    def test_10(self):
        lhs = ast.IntConst(2)
        rhs = ast.IntConst(5)
        RelExp_node = ast.RelExp(lhs, 'xnor', rhs)
        engine = sym.SymExec()
        st = sym.SymState()
        with self.assertRaises(AssertionError):
            result = engine.visit_RelExp(RelExp_node, state=st)
    def test_11(self):
        lhs = ast.IntConst(2)
        rhs = ast.IntConst(5)
        bexp_node = ast.BExp('lol', [lhs, rhs])          
        engine = sym.SymExec()
        st = sym.SymState()
        with self.assertRaises(AssertionError):
            result = engine.visit_BExp(bexp_node, state=st)
    def test_12(self):
        lhs = ast.IntConst(2)
        rhs = ast.IntConst(4)
        aexp_node = ast.AExp('?', [lhs, rhs])
        engine = sym.SymExec()
        st = sym.SymState()
        with self.assertRaises(AssertionError):
            result = engine.visit_AExp(aexp_node, state=st)
    def test_19(self):
        prg1 = 'x:=1; while x>0 do x:=x+1'
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out),1)
    def test_13(self):
        prg1 = 'x:=1; while x>2 do x:=x+1'
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out),1)
    def test_14(self):
        prg1 = 'havoc x; havoc y; havoc z; while x>100 do { while y> 100 do { while z >100 do {z:=z-1}; y:=y-1}; x:=x-1}'
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out),1111)
    def test_15(self):
        prg1 = 'x:=100; havoc y; if x>10 then {if y > 10 then y:=y-1} else {if y < 10 then y:=y+1}'
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out),2)
    def test_16(self):
        prg1 = 'havoc x; if x>10 then x:=20 else x:=40'
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out),2)
    def test_17(self):
        prg1 = '{\np:=0; \nx:=1; \nn:=2}; while x<=n do skip; print_state'
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out),1)
    
    """
    def test_9(self):
        prg1 = 'havoc x,y;while x > 0 do {while y > 0 do {y := y - 1};x := x -1}'
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 111)
    """

    
