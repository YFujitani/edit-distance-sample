from collections import namedtuple

import jaconv
import os
import MeCab
import Levenshtein
import time

from keyboard_distance import sort_by_keyboard_distance

MeCabToken = namedtuple('MeCabToken', ['surface', 'features'])

DICTIONARY_PATH = os.environ.get(
    'DICTIONARY_PATH', '/usr/local/lib/mecab/dic/mecab-ipadic-neologd')

tagger = MeCab.Tagger('-d {}'.format(DICTIONARY_PATH))
# 不具合用　https://shogo82148.github.io/blog/2015/12/20/mecab-in-python3-final/
tagger.parse('')

# INPUT = '黒いiPhoneほしい'
# KEYWORD_LIST = [
#     'iPhone X',
#     'iPhone 8',
#     'iPhone 8 Plus',
# ]

# INPUT = '竜宮の乙姫の元結の切外し'
# KEYWORD_LIST = [
#     '流宮の乙姫の元結の切外し',
# ]

# INPUT = 'SHERP'
# KEYWORD_LIST = [
#     'SHARP',
# ]

# INPUT = 'Apple 12W USB電源アダプタがほしい'
# KEYWORD_LIST = [
#     'Apple 12W USB電源アダプタ',
#     '充電器',
#     'アダプター',
#     'ACアダプター',
# ]

INPUT = 'カシオBCアダプタ01がほしい'
KEYWORD_LIST = [
    'カシオVCアダプタ01',
    'カシオGCアダプタ01',
    'カシオUSBケーブル01',
]

NUMBER_OF_TIMES_TO_ADD_TOKEN = 8

class Candidate:
    def __init__(self, keyword, token, distance=9999, similarity=0.0):
        self.keyword = keyword
        self.token = token
        self.distance = distance
        self.similarity = similarity
        self.diff_strings = []
        self.keybord_distance = -1


class Candidates:
    def __init__(self):
        self.candidates = []

    def append(self, candidate):
        self.candidates.append(candidate)

    def sort_by_distance(self):
        return sorted(self.candidates, key=lambda candidate: candidate.distance)

    def sort_by_similarity(self):
        return sorted(self.candidates, key=lambda candidate: candidate.similarity)

    def sort(self):
        sorted_candatetes = sorted(
            self.candidates, key=lambda candidate: (-candidate.similarity, candidate.distance))
        return sort_by_keyboard_distance(sorted_candatetes)


def test():
    tokens = parse(INPUT)
    # print(tokens)
    extract_by_edit_distance(tokens)

def parse(text):
    print('original', text)
    text = normalize_text(text)
    print('normalized', text)
    node = tagger.parseToNode(text)
    tokens = []
    while node:
        print(node.surface, node.feature)
        if node.surface != '':
            tokens.append(MeCabToken(node.surface, node.feature.split(',')))
        node = node.next
    return tokens


def normalize_text(text):
    normalized = text.lower()
    normalized = jaconv.normalize(normalized, mode='NFKC')
    normalized = jaconv.z2h(normalized, digit=True, kana=False, ascii=True)
    normalized = jaconv.h2z(normalized, digit=False, kana=True, ascii=False)
    normalized = jaconv.hira2kata(normalized)
    normalized = normalized.replace(' ', '').replace('　', '')
    return normalized


def extract_by_edit_distance(tokens, keywords=None):
    words = generate_words(tokens)
    print(words)
    candidates = Candidates()

    for keyword in KEYWORD_LIST:
        keyword = normalize_text(keyword)
        for word in words:
            d = Levenshtein.distance(word, keyword)
            s = Levenshtein.jaro_winkler(word, keyword)
            # TODO 同一word（expression）内の最も距離の近いモノのうち距離N以下の単語を抽出結果とする
            candidates.append(Candidate(keyword, word, d, s))
    
    print('result')
    # for c in candidates.sort_by_distance():
    for c in candidates.sort():
        print(vars(c))


def generate_words(tokens):
    words_by_token = [token.surface for token in tokens]
    return_words = []
    for i, token in enumerate(words_by_token):
        for j in range(NUMBER_OF_TIMES_TO_ADD_TOKEN + 1):
            word = ''
            for k in range(j + 1):
                if i + k == len(words_by_token):
                    break
                word += words_by_token[i + k]
            return_words.append(word)
    return sorted(set(return_words), key=return_words.index)


if __name__ == '__main__':
    start = time.time()
    test()
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

