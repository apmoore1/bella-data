from dataclasses import dataclass
from typing import List, Optional, Tuple

from bella_data.data_types import data_types_util

# Need to think about whether everything should be opional or if it would be 
# better to make it compulasary
@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, 
           frozen=False)
class BellaSentiment:
    id: str
    target_span: Optional[data_types_util.Span] = None
    target_sentiment: Optional[str] = None
    target_being_reviewed: Optional[bool] = None
    opinion_spans: Optional[List[data_types_util.Span]] = None
    opinion_sentiments: Optional[List[str]] = None
    opinion_intensity: Optional[List[str]] = None
    implicit_opinion: Optional[List[bool]] = None
    holder_spans: Optional[List[data_types_util.Span]] = None
    not_author: Optional[List[bool]] = None

    def get_target_attributes(self) -> Tuple[Optional[str], Optional[bool]]:
        '''
        This is useful for debugging by determining if two BellaSentiment 
        instances have the same target span also have the same target attributes.

        :returns: The attributes associated with the target, which is a tuple 
                  of (target sentiment, if the target is being reviewed) 
        '''
        return (self.target_sentiment, self.target_being_reviewed)
    # Interesting that 
    def test_target_attributes_same(self, other: 'BellaSentiment') -> None:
        '''
        This is useful if you wish to know if self and other contain the same 
        target attributes from `get_target_attributes`. This can be used 
        to test if self and other are the same from a target perspective when 
        self and other contain the same target span.

        :raises AssertionError: If self and other do not contain the same 
                                target attributes from `get_target_attributes`
        '''
        attribute_names = ['Target sentiment', 'Target being reviewed']
        other_attributes = other.get_target_attributes()
        for name, self_attribute, other_attribute in zip(attribute_names, 
                                                         self.get_target_attributes(), 
                                                         other_attributes):
            error_string = (f'self {self} and other {other} do not contain '
                            f'the same target attribute {name}. Self has '
                            f'{self_attribute} and other {other_attribute}. '
                            'These should be the same.')
            assert self_attribute == other_attribute, error_string
        
    