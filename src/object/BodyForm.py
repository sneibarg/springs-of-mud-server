from enum import IntEnum


class BodyForm(IntEnum):
    FORM_EDIBLE = 1 << 0
    FORM_POISON = 1 << 1
    FORM_MAGICAL = 1 << 2
    FORM_INSTANT_DECAY = 1 << 3
    FORM_OTHER = 1 << 4
    FORM_ANIMAL = 1 << 6
    FORM_SENTIENT = 1 << 7
    FORM_UNDEAD = 1 << 8
    FORM_CONSTRUCT = 1 << 9
    FORM_MIST = 1 << 10
    FORM_INTANGIBLE = 1 << 11
    FORM_BIPED = 1 << 12
    FORM_CENTAUR = 1 << 13
    FORM_INSECT = 1 << 14
    FORM_SPIDER = 1 << 15
    FORM_CRUSTACEAN = 1 << 16
    FORM_WORM = 1 << 17
    FORM_BLOB = 1 << 18
    FORM_MAMMAL = 1 << 21
    FORM_BIRD = 1 << 22
    FORM_REPTILE = 1 << 23
    FORM_SNAKE = 1 << 24
    FORM_DRAGON = 1 << 25
    FORM_AMPHIBIAN = 1 << 26
    FORM_FISH = 1 << 27
    FORM_COLD_BLOOD = 1 << 28
