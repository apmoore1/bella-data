import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from bella_data.data_types.data_types_util import Span
from bella_data.data_types.bella_sentiment import BellaSentiment
from bella_data.data_types.bella_data import BellaData
from bella_data.data_types.bella_dataset import BellaDataset

def get_and_verify_span(span_name: str,
                        word_span: Tuple[List[str], List[str]],
                        text: str, sentence_id: str) -> Span:
    '''
    :param span_name: The name of the span being extracted. e.g. holder, 
                      opinon, or target. This is used for error messages
    :param word_span: A tuple contain where the first list is a list of words 
                      that match the spans that are in the second list.
    :param text: The text that the spans match/associated with.
    :param sentence_id: The id of the sentence. This is used for error messages.
    :returns: The span of the `word_span` with error checking done.
    :raises AssertionError: If the words in `word_span` does not match the words 
                            produced from the spans using the `text`
    '''
    starts: List[int] = []
    ends: List[int] = []
    for word, span in zip(*word_span):
        start_end = span.split(':')
        assert len(start_end) == 2, (f'When splitting the span {span} it should '
                                     'be split into two based on `:`')
        start, end = int(start_end[0]), int(start_end[1])
        
        offset_word = text[start: end]
        offset_error = (f'{span_name} word {word} is not the same as its '
                        f'offset word {offset_word}. Within the following '
                        f' text {text} for sentence id {sentence_id}')
        assert offset_word == word, offset_error

        starts.append(start)
        ends.append(end)
    return Span(start=starts, end=ends)

data_path = Path('/Users/andrew/Desktop/norec_fine/data/train.json')

bella_datas = []
with data_path.open('r') as data:
    json_data = json.load(data)
    for sentence_data in json_data:
        print(sentence_data)
        sentence_id: str = sentence_data['sent_id']
        text: str = sentence_data['text']
        opinions: List[Dict[str, Any]] = sentence_data['opinions']
        if not opinions:
            bella_data = BellaData(id=sentence_id, text=text)
            bella_datas.append(bella_data)
            continue

        # The same target can occur more than once but with a different 
        # opinion/polar expression
        bella_sentiments: List[BellaSentiment] = []
        for opinion_index, opinion in enumerate(opinions):
            opinion_id = f'{sentence_id}-{opinion_index}' 

            # opinion expression
            opinion_spans: Optional[List[Span]] = None
            if opinion['Polar_expression']:
                opinion_word_span: Tuple[List[str], List[str]] = opinion['Polar_expression']
                opinion_spans = [get_and_verify_span('Opinion', opinion_word_span, 
                                                     text, sentence_id)]
            # holder expression
            holder_spans: Optional[List[Span]] = None
            if opinion['Source']:
                holder_word_span: Tuple[List[str], List[str]] = opinion['Source']
                holder_spans = [get_and_verify_span('Holder', holder_word_span, 
                                                     text, sentence_id)]
            #else:
            #    holder_error = ('Their are neither spans nor `Source_is_author`'
            #                    f' for this sentence {sentence_data}')
            #    assert opinion['Source_is_author'] == True, holder_error
            not_author: Optional[List[bool]] = None
            if 'NFP' in opinion:
                not_author = [True] if opinion['NFP'] == True else None

            # target spans
            target_span: Optional[Span] = None
            if opinion['Target']:
                target_word_span: Tuple[List[str], List[str]] = opinion['Target']
                target_span = get_and_verify_span('Target', target_word_span, 
                                                  text, sentence_id)
            target_being_reviewed: Optional[bool] = None
            if 'Target_is_general' in opinion:
                target_being_reviewed = opinion['Target_is_general']
            
            # opinion Sentiments/Intensity
            opinion_sentiments: Optional[List[str]] = None
            if opinion['Polarity']:
                opinion_sentiments = [opinion['Polarity']]
            implicit_opinion: Optional[List[bool]] = None
            if 'Type' in opinion:
                implicit_opinion = [False] if opinion['Type'] == 'E' else [True]
            opinion_intensity = [opinion['Intensity']]
                
            bella_sentiment = BellaSentiment(id=opinion_id, target_span=target_span, 
                                             target_sentiment=None, 
                                             target_being_reviewed=target_being_reviewed,
                                             opinion_spans=opinion_spans,
                                             opinion_sentiments=opinion_sentiments, 
                                             opinion_intensity=opinion_intensity, 
                                             implicit_opinion=implicit_opinion, 
                                             holder_spans=holder_spans, 
                                             not_author=not_author)
            bella_sentiments.append(bella_sentiment)
        bella_data = BellaData(id=sentence_id, text=text, 
                               sentiments=bella_sentiments)
        bella_data.combine_sentiments()
        bella_datas.append(bella_data)
    print('something')