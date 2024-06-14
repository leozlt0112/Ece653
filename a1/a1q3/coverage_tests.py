import unittest

from . import token_with_escape


class CoverageTests(unittest.TestCase):
    """ test 1 satisfies node coverage not edge coverage"""
    """ Node coverage TRnc = [8,10,11,13,14,26,15,16,23,17,18,24,19,21]"""
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
    """test 2 satisfies edge coverage but not edge pair coverage"""
    """edge covered in the below function 
    [8,10] [8,13] [10,11] [10,13] [11,13] 
    [13,14] [14,26] [14, 15] [15,16] 
    [15,23] [23,14] [23,24] [16,17] [16,18]
      [17,14] [18,19] [18,21] [19,24] 
      [21,14]"""
    """edge 24,14 is not covered because the state alternates
    between 0 and 1, there does not exist a case where state is neither 0 or 1 
    when evaluate to line 24, state is either 1 or 0"""
    def test_2(self):
        input = "|^b|b"
        output1 = token_with_escape(input)
        self.assertEqual(output1, ["","b","b"])
        input2 = "^"
        output2 = token_with_escape(input2)
        self.assertEqual(output2, [""])
        input3 = ""
        output3 = token_with_escape(input3)
        self.assertEqual(output3, [""])


    """edge pair covered 
    [8,10,13] [8,10,11] [8,13,14] [10,11,13]
    [10,13,14] [11,13,14] [13,14,15] [13,14,26]
    [14,15,16] [14,15,23] [15,16,17] 
    [15,23,24] [15,16,18] [16,17,14] [16,18,19]
    [16,18,21] [23,24,14] [17,14,26]
    [17,14,15] [24,14,26] [24,14,15]
    [18,19,14] [18,21,14] [19,14,26] [19,14,15]
    [21,14,26] [21,14,15]

    edge pair not covered [15,23,14] [23,14,15] [23,14,26]
    reason: since [23,14] is infeasible so u can't have an edge pair that include 
    [23,14]

    prime path not covered [8,10,11,13,14,26]
    """

    def test_3(self):
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