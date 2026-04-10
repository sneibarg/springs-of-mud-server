import random

from server.LoggerFactory import LoggerFactory


class RandomNumberGenerator:
    def __init__(self):
        self.logger = LoggerFactory.get_logger(__name__)

    @staticmethod
    def number_bits(width: int) -> int:
        max_value = (1 << width) - 1  # 2^width - 1
        return random.randint(0, max_value)

    @staticmethod
    def number_mm() -> int:  # Marsaglia-Multicarry random number generator.
        return random.randint(0, 0x7FFFFFFF)

    def number_fuzzy(self, number: int) -> int:
        bits = self.number_bits(2)  # Returns 0, 1, 2, or 3
        if bits == 0:
            number -= 1
        elif bits == 3:
            number += 1

        return max(1, number)

    def number_range(self, from_val: int, to_val: int) -> int:
        if from_val == 0 and to_val == 0:
            return 0

        span = to_val - from_val + 1
        if span <= 1:
            return from_val

        power = 2
        while power < span:
            power <<= 1  # power *= 2

        while True:
            number = self.number_mm() & (power - 1)
            if number < span:
                break

        return from_val + number

    def number_percent(self) -> int:
        while True:
            percent = self.number_mm() & (128 - 1)  # & 127, range [0, 127]
            if percent <= 99:
                break

        return 1 + percent

    def dice(self, num_dice: int, num_sides: int) -> int:
        if num_dice <= 0 or num_sides <= 0:
            return 0

        total = 0
        for _ in range(num_dice):
            total += self.number_range(1, num_sides)

        return total

    def coin_flip(self) -> bool:
        return self.number_bits(1) == 1

    def chance(self, percentage: int) -> bool:
        return self.number_percent() <= percentage
