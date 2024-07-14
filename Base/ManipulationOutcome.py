from enum import Enum

class ManipulationOutcome(Enum):
    
    LB_IMPROVMENT = 1
    UB_IMPROVMENT = 2
    WEAK_IMPROVMENT = 3
    STRICT_IMPROVMENT = 4

    def __str__(self):
        return '%s' % self.name