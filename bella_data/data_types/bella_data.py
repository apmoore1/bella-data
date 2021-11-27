from dataclasses import dataclass
from typing import List, Optional

from bella_data.data_types import bella_sentiment

@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, 
           frozen=False)
class BellaData:
    id: str
    text: str
    sentiments: Optional[List[bella_sentiment.BellaSentiment]] = None

    def combine_sentiments(self) -> None:
        '''
        This merges the information from sentiments that contain the same target
        span.
        '''
        if self.sentiments is None:
            return None
        print('here')
        temp_sentiments: List[bella_sentiment.BellaSentiment] = []
        for outer_sentiment in self.sentiments:
            same_target_spans: List[bella_sentiment.BellaSentiment] = []

            outer_target_span = outer_sentiment.target_span
            if outer_target_span is not None:
                for inner_sentiment in self.sentiments:
                    if outer_sentiment.id == inner_sentiment:
                        continue
                    if inner_sentiment.target_span == outer_target_span:
                        same_target_spans.append(inner_sentiment)
            if not same_target_spans:
                temp_sentiments.append(outer_sentiment)
            # some checks before mergining the same target spans data
            for same_target in same_target_spans:
                outer_sentiment.test_target_attributes_same(same_target)


            