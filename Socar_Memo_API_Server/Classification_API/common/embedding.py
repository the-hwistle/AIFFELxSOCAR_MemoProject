import gensim
import os
from gensim.test.utils import get_tmpfile


class S_FastText:
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), "data/FastTextModel/fasttext.model")
        self.fast_model = gensim.models.fasttext.FastText.load(
            get_tmpfile(self.model_path)
        )

    def get_key_to_index(self, token):
        try:
            return self.fast_model.wb.key_to_index[token]
        except:
            return ""

    def get_embedding(self, tokens):
        return [self.get_key_to_index(token) for token in tokens]
