from dataclasses import dataclass
from typing import Optional, Iterable

from bella_data.data_types import bella_data

@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, 
           frozen=False)
class BellaDataset:
    name: str
    data: Optional[Iterable[bella_data.BellaData]] = None