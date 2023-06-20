import re
from typing import Dict, List

from words.base import BaseExtract


class KeywordsExtract(BaseExtract):
    def __init__(self, keywords: List[str]):
        _ = '|'.join(keywords)
        self.regex_tmpl = f'({_})'
        self.r = re.compile(self.regex_tmpl, re.M)
        self.word_set = set()

    def add_words_chunks(self, chunks_data: Dict[int, List[str]]):
        for _, words_list in chunks_data.items():
            result = list(filter(self.r.search, words_list))
            self.word_set.update(result)

    def get_format_text(self):
        return ' '.join(self.word_set)
