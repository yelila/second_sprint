import unittest
from src.formula import Formula
from src.exception import InvalidPredicate, IncompletePredicate


class FormulaTest(unittest.TestCase):
    def test_parse_0(self):
        input_str = "¬ pq (aa , b0, f ( x1, dd1)) ∨ (p( y) ∧ t(c, g(k)) → q(b ) ∧r (c,d) ↔ s(z)) "
        expected_left_child = "¬(pq(aa,b0,f(x1,dd1)))"
        expected_right_left_child = "((p(y)) ∧ (t(c,g(k)))) → ((q(b)) ∧ (r(c,d)))"
        result = Formula.parse(input_str)
        self.assertEqual(result.left_child, expected_left_child)
        self.assertEqual(result.right_child.left_child, expected_right_left_child)

    def test_parse_1(self):
        input_str = "(Q9a (x,a, f(g(x),a) ))"
        expected = "Q9a(x,a,f(g(x),a))"
        result = Formula.parse(input_str)
        self.assertEqual(result, expected)

    def test_parse_2(self):
        invalid_str = "¬"
        with self.assertRaises(IncompletePredicate):
            Formula.parse(invalid_str)

    def test_parse_3(self):
        invalid_str = " ¬ Q9a (x,a, f(g(x),a)"
        with self.assertRaises(IncompletePredicate):
            Formula.parse(invalid_str)

    def test_parse_4(self):
        invalid_str = "∧P(x,y)"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_5(self):
        invalid_str = "p(x,y)∨"
        with self.assertRaises(IncompletePredicate):
            Formula.parse(invalid_str)

    def test_parse_6(self):
        invalid_str = "P(x) → (q(y) ↔r(x,y)"
        with self.assertRaises(IncompletePredicate):
            Formula.parse(invalid_str)

    def test_parse_7(self):
        invalid_str = "P(x) → (q(y) , r(x,y))"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)

    def test_parse_8(self):
        invalid_str = "P(x) ∨ (q(y) ¬r(x,y))"
        with self.assertRaises(InvalidPredicate):
            Formula.parse(invalid_str)


if __name__ == '__main__':
    unittest.main()