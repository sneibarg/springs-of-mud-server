"""
Unit tests for RandomNumberGenerator class.
Tests random number generation utilities for MUD game mechanics.
"""
import unittest
from unittest.mock import patch
from numbers import RandomNumberGenerator


class TestRandomNumberGenerator(unittest.TestCase):
    """Test suite for RandomNumberGenerator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.rng = RandomNumberGenerator()

    def test_number_bits_range(self):
        """Test that number_bits returns values in correct range"""
        # Test with width=2 (should return 0-3)
        for _ in range(100):
            result = self.rng.number_bits(2)
            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, 3)

        # Test with width=3 (should return 0-7)
        for _ in range(100):
            result = self.rng.number_bits(3)
            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, 7)

    def test_number_mm_range(self):
        """Test that number_mm returns positive integers"""
        for _ in range(100):
            result = self.rng.number_mm()
            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, 0x7FFFFFFF)

    def test_number_fuzzy_minimum(self):
        """Test that number_fuzzy never returns less than 1"""
        for i in range(1, 10):
            result = self.rng.number_fuzzy(i)
            self.assertGreaterEqual(result, 1)

        # Test with 1 - should never go below 1
        for _ in range(100):
            result = self.rng.number_fuzzy(1)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 2)

    @patch.object(RandomNumberGenerator, 'number_bits')
    def test_number_fuzzy_decrease(self, mock_bits):
        """Test number_fuzzy decreases when bits=0"""
        mock_bits.return_value = 0
        result = self.rng.number_fuzzy(10)
        self.assertEqual(result, 9)

    @patch.object(RandomNumberGenerator, 'number_bits')
    def test_number_fuzzy_unchanged(self, mock_bits):
        """Test number_fuzzy unchanged when bits=1 or bits=2"""
        mock_bits.return_value = 1
        result = self.rng.number_fuzzy(10)
        self.assertEqual(result, 10)

        mock_bits.return_value = 2
        result = self.rng.number_fuzzy(10)
        self.assertEqual(result, 10)

    @patch.object(RandomNumberGenerator, 'number_bits')
    def test_number_fuzzy_increase(self, mock_bits):
        """Test number_fuzzy increases when bits=3"""
        mock_bits.return_value = 3
        result = self.rng.number_fuzzy(10)
        self.assertEqual(result, 11)

    def test_number_range_basic(self):
        """Test basic number_range functionality"""
        # Test zero range
        result = self.rng.number_range(0, 0)
        self.assertEqual(result, 0)

        # Test single value
        result = self.rng.number_range(5, 5)
        self.assertEqual(result, 5)

        # Test range
        for _ in range(100):
            result = self.rng.number_range(1, 10)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 10)

    def test_number_range_negative(self):
        """Test number_range with negative numbers"""
        for _ in range(100):
            result = self.rng.number_range(-10, -5)
            self.assertGreaterEqual(result, -10)
            self.assertLessEqual(result, -5)

    def test_number_range_large(self):
        """Test number_range with large numbers"""
        for _ in range(100):
            result = self.rng.number_range(1000, 2000)
            self.assertGreaterEqual(result, 1000)
            self.assertLessEqual(result, 2000)

    def test_number_range_distribution(self):
        """Test that number_range produces reasonable distribution"""
        # Generate many numbers and check they span the range
        results = [self.rng.number_range(1, 10) for _ in range(1000)]
        unique_values = set(results)

        # Should have hit most values in range with 1000 samples
        self.assertGreater(len(unique_values), 5)
        self.assertLessEqual(max(results), 10)
        self.assertGreaterEqual(min(results), 1)

    def test_number_percent_range(self):
        """Test that number_percent returns values 1-100"""
        for _ in range(100):
            result = self.rng.number_percent()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 100)

    def test_number_percent_distribution(self):
        """Test number_percent produces reasonable distribution"""
        results = [self.rng.number_percent() for _ in range(1000)]

        # Should have values throughout the range
        self.assertGreater(len(set(results)), 50)
        self.assertEqual(max(results), 100) or self.assertGreater(max(results), 90)
        self.assertEqual(min(results), 1) or self.assertLess(min(results), 10)

    def test_dice_basic(self):
        """Test basic dice rolling"""
        # Roll 1d6
        for _ in range(100):
            result = self.rng.dice(1, 6)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 6)

        # Roll 2d6
        for _ in range(100):
            result = self.rng.dice(2, 6)
            self.assertGreaterEqual(result, 2)
            self.assertLessEqual(result, 12)

    def test_dice_zero(self):
        """Test dice with zero values"""
        self.assertEqual(self.rng.dice(0, 6), 0)
        self.assertEqual(self.rng.dice(1, 0), 0)
        self.assertEqual(self.rng.dice(0, 0), 0)

    def test_dice_negative(self):
        """Test dice with negative values"""
        self.assertEqual(self.rng.dice(-1, 6), 0)
        self.assertEqual(self.rng.dice(1, -6), 0)

    def test_dice_large(self):
        """Test dice with many dice"""
        # Roll 10d6 (min 10, max 60)
        for _ in range(100):
            result = self.rng.dice(10, 6)
            self.assertGreaterEqual(result, 10)
            self.assertLessEqual(result, 60)

    def test_coin_flip_distribution(self):
        """Test coin flip produces roughly equal true/false"""
        results = [self.rng.coin_flip() for _ in range(1000)]
        true_count = sum(results)
        false_count = len(results) - true_count

        # Should be roughly 50/50 (allow 40-60% range)
        self.assertGreater(true_count, 350)
        self.assertLess(true_count, 650)
        self.assertGreater(false_count, 350)
        self.assertLess(false_count, 650)

    def test_chance_always_success(self):
        """Test chance with 100% always succeeds"""
        for _ in range(50):
            self.assertTrue(self.rng.chance(100))

    def test_chance_never_success(self):
        """Test chance with 0% never succeeds"""
        for _ in range(50):
            self.assertFalse(self.rng.chance(0))

    def test_chance_distribution(self):
        """Test chance produces reasonable success rate"""
        # Test 50% chance
        results = [self.rng.chance(50) for _ in range(1000)]
        success_count = sum(results)

        # Should be roughly 500 successes (allow 400-600)
        self.assertGreater(success_count, 400)
        self.assertLess(success_count, 600)

    def test_chance_low_percentage(self):
        """Test chance with low percentage"""
        # 10% chance should succeed roughly 100 times in 1000
        results = [self.rng.chance(10) for _ in range(1000)]
        success_count = sum(results)

        # Allow 5-15% success rate
        self.assertGreater(success_count, 50)
        self.assertLess(success_count, 150)

    def test_chance_high_percentage(self):
        """Test chance with high percentage"""
        # 90% chance should succeed roughly 900 times in 1000
        results = [self.rng.chance(90) for _ in range(1000)]
        success_count = sum(results)

        # Allow 85-95% success rate
        self.assertGreater(success_count, 850)
        self.assertLess(success_count, 950)


class TestRandomNumberGeneratorEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def setUp(self):
        """Set up test fixtures"""
        self.rng = RandomNumberGenerator()

    def test_number_fuzzy_edge_cases(self):
        """Test number_fuzzy with edge case values"""
        # Test with 2 (minimum after potential decrease)
        result = self.rng.number_fuzzy(2)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 3)

        # Test with large number
        result = self.rng.number_fuzzy(1000)
        self.assertGreaterEqual(result, 999)
        self.assertLessEqual(result, 1001)

    def test_number_range_reversed(self):
        """Test number_range with from > to"""
        # This should return from_val since span becomes <= 1
        result = self.rng.number_range(10, 5)
        self.assertEqual(result, 10)

    def test_number_range_equal(self):
        """Test number_range with equal values"""
        for val in [1, 10, 100]:
            result = self.rng.number_range(val, val)
            self.assertEqual(result, val)


if __name__ == '__main__':
    unittest.main()
