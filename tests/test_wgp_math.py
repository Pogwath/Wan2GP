import unittest
from shared.math.math_utils import compute_sliding_window_no

class TestWgpMath(unittest.TestCase):

    def test_basic_one_window(self):
        self.assertEqual(compute_sliding_window_no(81, 81, 0, 0), 1)
        self.assertEqual(compute_sliding_window_no(40, 81, 0, 0), 1)

    def test_one_window_with_discard(self):
        self.assertEqual(compute_sliding_window_no(81, 81, 1, 0), 2)
        self.assertEqual(compute_sliding_window_no(80, 81, 1, 0), 1)

    def test_two_windows(self):
        self.assertEqual(compute_sliding_window_no(157, 81, 0, 5), 2)
        self.assertEqual(compute_sliding_window_no(158, 81, 0, 5), 3)

    def test_complex_case(self):
        self.assertEqual(compute_sliding_window_no(200, 81, 10, 10), 4)

    def test_zero_length(self):
        self.assertEqual(compute_sliding_window_no(0, 81, 0, 5), 0)

if __name__ == '__main__':
    unittest.main()
