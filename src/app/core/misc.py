# -*- coding: utf-8 -*-
from typing import Union
from fuzzywuzzy import fuzz
import pandas as pd
import re
import pyphen
from hyphen import Hyphenator
from hyphen.textwrap2 import fill
import math
import logging

h_de = Hyphenator('de_DE')


def __line_threshold(n_lines: int = 4, max_chars: int = 40):
    return math.floor(max_chars / n_lines)


def __split(token: str) -> []:
    return [w for w in token.split(' ') if w != '']


def __clean(token) -> str:
    _t = token
    # remove garbage chars
    _t = re.sub('[!@#$%^&*;<>?|~=_]', '', _t)
    # remove multiple spaces
    _t = re.sub(' +', ' ', _t)
    # replace "-" for " " due exceptions on hyphen lib
    _t = re.sub('-', ' ', _t)
    # strip
    _t = _t.strip()
    return _t


def sanitize(token: str) -> (str, []):
    cleaned = __clean(token)
    splitted = __split(cleaned)
    return cleaned, splitted


def __shorten(description, to_replace, replacement):
    cleaned = __clean(description)
    # TODO: each new word, check if the size fits the threshold.
    #  if so, it is not necessary to keeps shortening...
    return re.sub(rf'\b{to_replace.casefold()}\b', replacement.casefold(),
                  cleaned.casefold(), flags=re.IGNORECASE)


def token_sort_ratio(splitted, clean_description):
    return fuzz.token_sort_ratio('!'.join(splitted), clean_description)


def replace(actual_dsc: str, df: Union[pd.DataFrame, dict], sanitise: bool = True, uppercase: bool = True):
    """
    From the actual_dsc, replace token by token
    :param actual_dsc: The current description, with no modifications
    :param df: the df on a key-value format, to find and replace the existing words
    :param sanitise: Indicates if the actual_dsc should be sanitised. Default = True
    :param uppercase: Indicates if should output in uppercase
    :return: The new sanitised and replaced word
    """

    try:
        new_dsc = sanitize(actual_dsc)[0] if sanitise else actual_dsc
        dict_kv_replace = dict(zip(df['to_replace'], df['replacement'])) if isinstance(df, pd.DataFrame) else df

        # create a pre-filter with the words that may be replaced -- got performance improvement
        pre_filter = []
        for token in new_dsc.split(' '):
            pre_filter.extend(
                list(filter(lambda f: token.casefold() in f[0].casefold(), list(dict_kv_replace.items()))))

        # actually replace the words
        for to_repl, repl in dict(pre_filter).items():
            new_dsc = __shorten(new_dsc, to_repl, repl)

        if uppercase:
            return new_dsc.upper()
        return new_dsc
    except Exception as e:
        logging.error(f'Exception when replacing the term "{actual_dsc}": "{str(e)}"')
        return actual_dsc


# ----------
# tokenize -- approach 2
# ----------
def wrap(prod_description, n_lines=4, max_chars=40) -> []:
    try:
        line_threshold = __line_threshold(n_lines, max_chars)
        prod_description = __clean(prod_description)
        if len(prod_description) <= max_chars:
            r = fill(prod_description, width=line_threshold, use_hyphenator=h_de)
            return r.split('\n')

        return []
    except Exception as e:
        print(str(e))


# ---------
# tokenize - approach 1
# ---------
def tokenize(description: str, n_lines=4, max_chars=40) -> {}:
    _text, description_words = sanitize(description)
    line_threshold = __line_threshold(n_lines, max_chars)
    # if is possible to chunck. before this piece,
    # we suppose that the the words replacement were done
    if len(_text) <= max_chars:
        dic = pyphen.Pyphen(lang='de_DE')
        hyphenated = {}
        for w in description_words:
            hyphenated[w] = dic.inserted(w)

        # rebuild the name, now chuncked
        new_text = []
        for word in hyphenated:
            hyphenated_chuncked = hyphenated[word].split('-')
            # for every piece of the word
            for chunck in hyphenated_chuncked:

                space = ' ' if hyphenated_chuncked[-1] == chunck else ''
                last_word = _text[-(len(word)):] == word

                # if the current chunck fits the threshold size
                if new_text and len(chunck)+len(new_text[-1]) < (line_threshold + (1 if last_word else 0)):
                    new_text[-1] += chunck + space
                else:
                    # if the last char in the last word is not a space
                    if new_text and new_text[-1][-1] != ' ':
                        new_text[-1] += '-'
                    new_text.append(chunck + space)

        return new_text
    else:
        return []


