import unittest
from src.formula import Formula
from src.exception import InvalidPredicate, IncompletePredicate

class FormulaTest(unittest.TestCase):
    def test_parse_0(self):
        input_str = "Q9a (x,a, f(g(x),a) )"
        expected = "Q9a(x,a,f(g(x),a))"
        result = Formula.parse(input_str)
        self.assertEqual(expected, str(result))
    
    def test_parse_1(self):
        invalid_str = "P"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_2(self):
        invalid_str = "P()"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_3(self):
        invalid_str = "Px,y)"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_4(self):
        invalid_str = "P(x,y"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_5(self):
        invalid_str = "(x,y)"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_6(self):
        invalid_str = "P(x,)"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_7(self):
        invalid_str = "9p(x, y)"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_8(self):
        invalid_str = "P_9(x, y)"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_9(self):
        invalid_str = "P(x,(y)"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_10(self):
        invalid_str = "P(x,f(y)"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_11(self):
        invalid_str = "P(x,f(g(y,), a))"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_12(self):
        invalid_str = ""
        with self.assertRaises(IncompletePredicate):
            Formula.parse(invalid_str)

    def test_parse_13(self):
        invalid_str = "  "
        with self.assertRaises(IncompletePredicate):
            Formula.parse(invalid_str)
    
    def test_parse_14(self):
        invalid_str = None
        with self.assertRaises(IncompletePredicate):
            Formula.parse(invalid_str)

    def test_parse_15(self):
        invalid_str = "p 9(x,f(y)"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)


if __name__ == '__main__':
    unittest.main()