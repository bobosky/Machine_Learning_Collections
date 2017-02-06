import numpy as np
from scipy import sparse
import re

from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer


class TextFeatureTransformer(BaseEstimator):
    def __init__(self, word_range=(1, 1), char_range=(1, 1), char=False,
            word=True, designed=True, tokenizer_func=None):
        self.word_range = word_range
        self.char_range = char_range
        self.char = char
        self.designed = designed
        self.word = word
        self.tokenizer_func = tokenizer_func

    def get_feature_names(self):
        feature_names = []
        if self.word:
            feature_names.append(self.countvect.get_feature_names())
        if self.char:
            feature_names.append(self.countvect_char.get_feature_names())
        if self.designed:
            feature_names.append(['n_words', 'n_chars', 'allcaps', 'max_len',
                'mean_len', '@', '!', '?', 'dots', 'spaces', 'bad_ratio',
                'n_bad', 'capsratio'])
        feature_names = np.hstack(feature_names)
        return feature_names

    def fit(self, comments, y=None):
        # get the google bad word list
        #with open("google_badlist.txt") as f:
        with open("my_badlist.txt") as f:
            badwords = [l.strip() for l in f.readlines()]
        self.badwords_ = badwords

        print("vecorizing")
        if self.word:
            if self.tokenizer_func != None:
                def build_tokenizer(func):
                    regexp = re.compile(ur"\b\w\w+\b")
                    tokenizer = lambda doc: [func(word) for word in
                            regexp.findall(doc)]
                    return tokenizer
                tokenizer = build_tokenizer(self.tokenizer_func)
            else:
                tokenizer = None
            countvect = TfidfVectorizer(ngram_range=self.word_range,
                    binary=False, tokenizer=tokenizer, min_df=2)
            countvect.fit(comments)
            self.countvect = countvect

        if self.char:
            countvect_char = TfidfVectorizer(ngram_range=self.char_range,
                    analyzer="char", binary=False)
            countvect_char.fit(comments)
            self.countvect_char = countvect_char
        return self

    def transform(self, comments):

        ## some handcrafted features!
        n_words = [len(c.split()) for c in comments]
        n_chars = [len(c) for c in comments]
        # number of uppercase words
        allcaps = [np.sum([w.isupper() for w in comment.split()])
               for comment in comments]
        # longest word
        max_word_len = [np.max([len(w) for w in c.split()]) for c in comments]
        # average word length
        mean_word_len = [np.mean([len(w) for w in c.split()])
                                            for c in comments]
        # number of google badwords:
        n_bad = [np.sum([c.lower().count(w) for w in self.badwords_])
                                                for c in comments]
        exclamation = [c.count("!") for c in comments]
        addressing = [c.count("@") for c in comments]
        question = [c.count("?") for c in comments]
        spaces = [c.count(" ") for c in comments]
        dots = [c.count("...") for c in comments]

        allcaps_ratio = np.array(allcaps) / np.array(n_words, dtype=np.float)
        bad_ratio = np.array(n_bad) / np.array(n_words, dtype=np.float)

        designed = np.array([n_words, n_chars, allcaps, max_word_len,
            mean_word_len, exclamation, question, addressing, dots, spaces,
            bad_ratio, n_bad, allcaps_ratio]).T

        features = []
        if self.word:
            counts = self.countvect.transform(comments).tocsr()
            features.append(counts)
        if self.char:
            counts_char = self.countvect_char.transform(comments).tocsr()
            features.append(counts_char)
        if self.designed:
            features.append(sparse.csr_matrix(designed))
        features = sparse.hstack(features)

        return features.tocsr()
