from enum import IntEnum


class BodyParts(IntEnum):
    PART_HEAD = 1 << 0
    PART_ARMS = 1 << 1
    PART_LEGS = 1 << 2
    PART_HEART = 1 << 3
    PART_BRAINS = 1 << 4
    PART_GUTS = 1 << 5
    PART_HANDS = 1 << 6
    PART_FEET = 1 << 7
    PART_FINGERS = 1 << 8
    PART_EAR = 1 << 9
    PART_EYE = 1 << 10
    PART_LONG_TONGUE = 1 << 11
    PART_EYESTALKS = 1 << 12
    PART_TENTACLES = 1 << 13
    PART_FINS = 1 << 14
    PART_WINGS = 1 << 15
    PART_TAIL = 1 << 16
    PART_CLAWS = 1 << 20
    PART_FANGS = 1 << 21
    PART_HORNS = 1 << 22
    PART_SCALES = 1 << 23
    PART_TUSKS = 1 << 24
