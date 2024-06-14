import unittest

from . import token_with_escape


class CoverageTests(unittest.TestCase):
    def test_1(self):
        """Node Coverage but not Edge Coverage"""
        """find some input"""
        """put it in a variable"""
        """get the output from tokenwithescape """
        """use self.assertEqualto see if equal"""
        input = "|^b|b"
        output = token_with_escape(input)
        self.assertEqual(output, ["","b","b"])
        # YOUR CODE HERE

    
    def test_2(self):
        """Edge Coverage but not Edge Pair Coverage"""
        input = "|^b|b"
        output1 = token_with_escape(input)
        self.assertEqual(output1, ["","b","b"])
        input2 = "^"
        output2 = token_with_escape(input2)
        self.assertEqual(output2, [""])
        input3 = ""
        output3 = token_with_escape(input3)
        self.assertEqual(output3, [""])


        # YOUR CODE HERE


    def test_3(self):
        """Edge Pair Coverage but not Prime Path Coverage"""
        # YOUR CODE HERE
        """Edge Coverage but not Edge Pair Coverage"""
        input1 = "|^b|b"
        output1 = token_with_escape(input1)
        self.assertEqual(output1, ["","b","b"])
        input2 = "^"
        output2 = token_with_escape(input2)
        self.assertEqual(output2, [""])
        input3 = ""
        output3 = token_with_escape(input3)
        self.assertEqual(output3, [""])
        input4 = "^b"
        output4 = token_with_escape(input4)
        self.assertEqual(output4, ["b"])
        input5 = "bb"
        output5 = token_with_escape(input5)
        self.assertEqual(output5, ["bb"])
        input6 = "||"
        output6 = token_with_escape(input6)
        self.assertEqual(output6, ["","",""])

