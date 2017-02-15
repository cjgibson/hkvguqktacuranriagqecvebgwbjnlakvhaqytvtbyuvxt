# coding=utf-8
###
# AUTHORS: CHRISTIAN GIBSON,
# PROJECT: SENTENCE SPLITTING REGULAR EXPRESSION
# UPDATED: FEBURARY 15, 2017
# USAGE:
# EXPECTS: python 2.7.6
#          regex 2015.3.18
###

import regex

# Version 70
# (?x)
# (?P<sentence>
#   # We start by aggressively consuming all non-terminal characters.
#   (?:[^\p{Po}\r\n]*)
#   (?:
#     # If the discovered non-terminal is punctuation:
#     (?=\p{Po})
#     # And it belongs to our group of non-sentence-terminating punctuation:
#     (?=
#       [\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}/\#&,*+@$%^'"\-:;\(\)\[\]\{\}\u2022\u055d\u060c\u060d\u07f8\u1802\u1808\u2013\u2014\u3001\ufe10\ufe11\u30fb\ufe13\ufe31\ufe32\ufe50\ufe51\ufe55\ufe58\ufe63\uff0c\uff0d\uff1a\uff64\u2026]
#     )
#     # Then we consume it, and any subsequent characters from the same.
#     (?P<continuous>
#       .[\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}/\#&,*+@$%^'"\-:;\(\)\[\]\{\}\u2022\u055d\u060c\u060d\u07f8\u1802\u1808\u2013\u2014\u3001\ufe10\ufe11\u30fb\ufe13\ufe31\ufe32\ufe50\ufe51\ufe55\ufe58\ufe63\uff0c\uff0d\uff1a\uff64\u2026]*
#     )
#     # And recurse to the start of the pattern, continuing the sentence.
#     (?R)|
#     # Otherwise, if the punctuation was considered sentence-terminating, we
#     #   need to ensure that we're actually at the end of the sentence.
#     (?!
#       [\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}/\#&,*+@$%^'"\-:;\(\)\[\]\{\}\u2022\u055d\u060c\u060d\u07f8\u1802\u1808\u2013\u2014\u3001\ufe10\ufe11\u30fb\ufe13\ufe31\ufe32\ufe50\ufe51\ufe55\ufe58\ufe63\uff0c\uff0d\uff1a\uff64\u2026]
#     )
#     # If the punctuation was immediately followed by a character, such as:
#     #   2.5, google.com; then we consume and continue the sentence.
#     (?=.[A-z0-9])
#     (?P<latin>.{1,4}[\p{P}\p{Zs}]*)
#     (?R)|
#     # If the encountered punctuation is an ellipsis (...), then we consume it
#     #   and continue the sentence.
#     (?=\.{3})
#     (?P<ellipsis>\.{3})
#     (?R)|
#     # Otherwise, if the encountered punctuation was part of a honorific, such
#     #  as Mr., Ms., Dr., then we consume it and continue the sentence.
#     (?<=\p{Lu}\p{Ll})
#     (?P<honorific>.)
#     (?R)|
#     # Otherwise, if the encountered punctuation was part of an extended
#     #  abbreviation, such as Esq., Jan., then consume and continue.
#     (?<=\p{Lu}\p{Ll}{2})
#     (?P<abbreviation>.)
#     (?R)|
#     # Otherwise, if the encountered punctuation could be part of an enumerated
#     #  list, such as 1. 2. 3., then we consume it and continue the sentence.
#     (?<=\p{Zs}\p{N})
#     (?P<inner_enumeration>.)
#     (?R)|
#     # We also check to see if our text starts with an enumerated list.
#     (?<=^\p{N})
#     (?P<start_enumeration>.)
#     (?R)|
#     # If we've make it this far, then we're very likely at the end of the
#     #  sentence. We consume all available punctuation and whitespace in order
#     #  to reduce the possibility of backtracking, terminate the sentence, and
#     #  restart the pattern.
#     (?:.[\p{P}\p{Zs}]*)
#   )|
#   # If we didn't match punctuation, then we're at a newline character.
#   (?!\p{Po})
#   (?=[\r\n])
#   # So we consume the newline, and recurse.
#   (?P<newline>[\r\n])|
#   # This logic checks to see if somehow we made it to this point in the
#   #   pattern, but we *did* match punctuation. It should never evaluate.
#   (?![\r\n])
#   (?P<initial>
#     [\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}/\#&,*+@$%^'"\-:;\(\)\[\]\{\}\u2022\u055d\u060c\u060d\u07f8\u1802\u1808\u2013\u2014\u3001\ufe10\ufe11\u30fb\ufe13\ufe31\ufe32\ufe50\ufe51\ufe55\ufe58\ufe63\uff0c\uff0d\uff1a\uff64\u2026]+
#   )
#   (?R)
# )
###

_CHECK = (u"["
          ur"\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}"
          ur"/\#&,*+@$%^'" + u'"' + ur"\-:;\(\)\[\]\{\}"
          ur"\u2022\u055d\u060c\u060d\u07f8\u1802\u1808\u2013"
          ur"\u2014\u3001\ufe10\ufe11\u30fb\ufe13\ufe31\ufe32"
          ur"\ufe50\ufe51\ufe55\ufe58\ufe63\uff0c\uff0d\uff1a"
          ur"\uff64\u2026"
          u"]")
_PATTERN = ur"""(?x)
(
  (?:[^\p{{Po}}\r\n]*)
  (?:
    (?=\p{{Po}})
    (?={0})
    (?:.{0}*)
    (?R)|
    (?!{0})
    (?=.[A-z0-9])
    (?:.{{1,4}}[\p{{P}}\p{{Zs}}]*)
    (?R)|
    (?=\.{{3}})
    (?:\.{{3}})
    (?R)|
    (?<=\p{{Lu}}\p{{Ll}})
    (?:.)
    (?R)|
    (?<=\p{{Lu}}\p{{Ll}}{{2}})
    (?:.)
    (?R)|
    (?<=\p{{Zs}}\p{{N}})
    (?:.)
    (?R)|
    (?<=^\p{{N}})
    (?:.)
    (?R)|
    (?:.[\p{{P}}\p{{Zs}}]*)
  )|
  (?!\p{{Po}})
  (?=[\r\n])
  (?:[\r\n])|
  (?![\r\n])
  (?:{0}+)
  (?R)
)""".format(_CHECK)
_REGEX = regex.compile(_PATTERN, regex.UNICODE + regex.V1)


def sentence_split(text, yield_empty=False):
    for sentence in _REGEX.split(text):
        sentence = sentence.strip()
        if not yield_empty or sentence:
            yield sentence
