from enum import Enum

class ObjectiveNames(Enum):

    MAX_UTIL = 1
    MAX_EGAL = 2
    AT_LEAST1 = 3
    # OTHER_OBJECTIVE = 4
    # ...
    # ...
    # ...

    def __str__(self):
        return '%s' % self.name