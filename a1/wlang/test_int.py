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

from . import ast, int, parser

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

    def test_visitRelExp(self):
        lhs = ast.Const(2)
        rhs = ast.Const(5)
        RelExp_node = ast.RelExp(lhs,'xnor',rhs)
        interp=int.Interpreter()
        with self.assertRaises(AssertionError):
            interp.visit_RelExp(RelExp_node)
    
    def test_Bexp(self):
        prg1 = "if (not false) and true then x:=2"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        
        st = interp.run(ast1, st)
    def test_Bexp1(self):
        prg1 = "if (not false) or true then x:=2"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)

    def test_visit_BExp_unsupported_operation(self):
        lhs = ast.Const(1)
        rhs = ast.Const(2)
        
        bexp_node = ast.BExp('xnor', [lhs, rhs])  
        interpreter = int.Interpreter()
        
        with self.assertRaises(AssertionError):
            interpreter.visit_BExp(bexp_node)

    def test_vist_Aexp_unsupported(self):
        lhs = ast.Const(2)
        rhs = ast.Const(4)
        aexp_node = ast.AExp('?', [lhs,rhs])
        interpreter = int.Interpreter()
        with self.assertRaises(AssertionError):
            interpreter.visit_AExp(aexp_node)
    
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
        with self.assertRaises(Exception):
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

    def test_printAssumeStmt(self):
        node = ast.AssumeStmt('assume x<2')
        ast1=ast.PrintVisitor()   
        with self.assertRaises(Exception):
            as2=ast1.visit_AssumeStmt(node)
    def test_havocStmt(self):
        prg1 = "havoc p,d,f"
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
    def test_AssumeStmt(self):
        prg1 = "assume x=1"
        ast1 = ast.parse_string(prg1)
        prg2 = "assume x=1"
        ast2 = ast.parse_string(prg2)
        self.assertEqual(ast1,ast2)
    def test_Exp(self):
        operation1 = ['x', ':=', "2"]
        args1 = [100, 9090]
        expression1 = ast.Exp(operation1, args1)
        expression1.is_binary()
    def test_open_brkt(self):
        ast_print_Visitor = ast.PrintVisitor()
        ast_print_Visitor._open_brkt(no_brkt='')
        ast_print_Visitor._close_brkt(no_brkt='')
    def test_visit_Exp_is_unary(self):
        ast1= ast.PrintVisitor()
        operation1 = ['x', ':=', "2"]
        node = ast.BoolConst('true')
        args1 = [node]
        expression1 = ast.Exp(operation1, args1)
        ast1.visit_Exp(expression1)
    def test_visit_StmtList(self):
        ast_stmtlist=ast.StmtList('')
        ast1_Printvisitor= ast.PrintVisitor()
        ast1_Printvisitor.visit_StmtList(ast_stmtlist)
        
    def test_visit_AssumeStmt(self):
        node = ast.BoolConst('true')
        astassume = ast.AssumeStmt(node)
        ast1_Printvisitor= ast.PrintVisitor()
        ast1_Printvisitor.visit_AssumeStmt(astassume)
    def test_visit_HavocStmt(self):
        node = ast.BoolConst('true')
        node2 = ast.BoolConst('true')
        listofnodes = [node,node2]
        astassume = ast.HavocStmt(listofnodes)
        ast1_Printvisitor= ast.PrintVisitor()
        ast1_Printvisitor.visit_HavocStmt(astassume)

    def test_visit_IntVar(self):
        astIntvar=ast.IntVar("x")
        astvisitor = ast.AstVisitor()
        with self.assertRaises(Exception):
            output = astvisitor.visit_IntVar(astIntvar)
    def test_visit_SkipStmt(self):
        astskip = ast.SkipStmt()
        astvisitor = ast.AstVisitor()
        with self.assertRaises(Exception):
            output=astvisitor.visit_SkipStmt(astskip)
    def test_visit_PrintStateStmt(self):
        astPrint = ast.PrintStateStmt()
        astvisitor = ast.AstVisitor()
        with self.assertRaises(Exception):
            output=astvisitor.visit_PrintStateStmt(astPrint)
    def test_visit_AsgnStmt(self):
        astAssign = ast.AsgnStmt('x', '2')
        astvisitor = ast.AstVisitor()
        with self.assertRaises(Exception):
            output=astvisitor.visit_AsgnStmt(astAssign)
    def test_visit_IfStmt(self):
        astIfStmt= ast.IfStmt('=', 'then')
        astvisitor = ast.AstVisitor()
        with self.assertRaises(Exception):
            output=astvisitor.visit_IfStmt(astIfStmt)
    def test_visit_whilestmt(self):
        astwhileStmt= ast.WhileStmt('=', 'x=2')
        astvisitor = ast.AstVisitor()
        with self.assertRaises(Exception):
            output=astvisitor.visit_WhileStmt(astwhileStmt)
    def test_vist_assertstmt(self):
        astassertStmt=ast.AssertStmt('true')
        astvisitor = ast.AstVisitor()
        with self.assertRaises(Exception):
            output=astvisitor.visit_AssertStmt(astassertStmt)
    
    def test_whileLangBuffer(self):
        whilebuffer=parser.WhileLangBuffer('sss')
    def test_stmt_parser(self):
        p = '?;?'
        with self.assertRaises(Exception):
             ast1 = ast.parse_string(p)
             interp = int.Interpreter()
             st = int.State()
             st = interp.run(ast1, st)
    def test_parser_block_stmt(self):
        p = parser.WhileLangParser()
        with self.assertRaises(Exception):
            c = p._block_stmt_()
    def test_parser_while_stmt(self):
        prg='p:=100;while p>0 inv p>0 do {\n p := p-1\n}; print_state'
        ast1 = ast.parse_string(prg)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    def test__bfactor(self):
        p = 'while 2'
        with self.assertRaises(Exception):
            ast1 = ast.parse_string(p)
            interp = int.Interpreter()
            st = int.State()
            st = interp.run(ast1, st)
    def test_parser_negative(self):
        p = "x:=-1"
        ast1 = ast.parse_string(p)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    """def test_parser_newline(self):
        parser1 = parser.WhileLangParser()
        print(parser1._NEWLINE_())"""
    def test_parser_whilelang(self):
        p = "x:=-1"
        ast1 = ast.parse_string(p)
        c = parser.WhileLangSemantics()
        c.start(p)
        c.stmt_list(p)
        c.stmt(p)
        c.asgn_stmt(p)
        c.print_state_stmt(p)
        c.if_stmt(p)
        c.while_stmt(p)
        c.assert_stmt(p)
        c.assume_stmt(p)
        c.block_stmt(p)
        c.skip_stmt(p)
        c.havoc_stmt(p)
        c.var_list(p)
        c.bexp(p)
        c.bterm(p)
        c.bfactor(p)
        c.batom(p)
        c.bool_const(p)
        c.rexp(p)
        c.rop(p)
        c.aexp(p)
        c.addition(p)
        c.subtraction(p)
        c.term(p)
        c.mult(p)
        c.division(p)
        c.factor(p)
        c.neg_number(p)
        c.atom(p)
        c.name(p)
        c.number(p)
        c.INT(p)
        c.NAME(p)
        c.NEWLINE(p)
    def test_visit_AssumeStmt(self):
        astassertStmt=ast.AssumeStmt('true')
        astvisitor = ast.AstVisitor()
        with self.assertRaises(Exception):
            output=astvisitor.visit_AssumeStmt(astassertStmt)
    def test_visit_HavocStmt(self):
        astHavocStmt=ast.HavocStmt(['x','y'])
        astvisitor = ast.AstVisitor()
        with self.assertRaises(Exception):
            output=astvisitor.visit_HavocStmt(astHavocStmt)
    def test_visit_StmtList_branch(self):
        var_x = ast.IntVar("x")
        const_1 = ast.IntConst(1)
        assign_stmt = ast.AsgnStmt(lhs=var_x, rhs=const_1)

        # Create a StmtList with a list containing one AsgnStmt
        stmtlist_ast = ast.StmtList([assign_stmt])

        # Create a PrintVisitor and use it to visit the StmtList
        visitor_print = ast.PrintVisitor()
        visitor_print.visit(stmtlist_ast)
    def test_print_if_stmt(self):
        prg1='x:=1;if x=1 then x:=2'
        ast1=ast.parse_string(prg1)
        print(ast1)
        
    @patch('sys.argv', ['wlang.int', 'wlang/test1.prg'])
    def test_main1(self):
        self.assertEqual(int.main(),0)
    
    @patch('sys.argv', ['wlang.parser', 'wlang/test1.prg'])
    def test_main2(self):
        filename = 'wlang/test1.prg' 
        result = parser.main(filename)
    
   




