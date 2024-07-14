from enum import Enum

class AlgorithmsNames(Enum):

    FPT = 1
    BRUTE_FORCE = 2
    SOCIALLY = 3
    NEW_FPT3 = 4

    def __str__(self):
        return '%s' % self.name