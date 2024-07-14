from enum import Enum

class ManipulatorActions(Enum):
    
    ADD_EDGE_ONLY = 1
    ADD_OR_REMOVE_EDGE = 2
    REMOVE_EDGE_ONLY = 3
    # OTHER_ACTION = 4
    # ...
    # ...
    # ...

    def __str__(self):
        return '%s' % self.name