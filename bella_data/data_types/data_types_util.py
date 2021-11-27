from dataclasses import dataclass, field
from typing import List

@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, 
           frozen=False)
class Span:
    start: List[int]
    end: List[int]
    is_discontinuous: bool = field(init=False)

    def __post_init__(self):
        if len(self.start) > 1:
            self.is_discontinuous = True
        else:
            self.is_discontinuous = False