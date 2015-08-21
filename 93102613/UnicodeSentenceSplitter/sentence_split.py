# coding=utf-8
###
# AUTHORS: CHRISTIAN GIBSON,
# PROJECT: SENTENCE SPLITTING REGULAR EXPRESSION
# UPDATED: AUGUST 03, 2015
# USAGE:
# EXPECTS: python 2.7.6
#          regex 2015.3.18
###

import regex

### Version 68
# (?x)
# (?P<sentence>
#   # Consume anything that isn't a newline or punctuation.
#   (?:[^\p{Po}\r\n]*)
#   # Once we've found either a newline or punctuation...
#   (?:
#     # If it's punctuation...
#     (?=\p{Po})
#       # But not punctuation used at the end of a sentence...
#       (?=
#         [\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}\/\\#&,*+@$%^'"\-:;\(\)\[\]\{\}•՝،؍߸᠂᠈–—、︐︑・︓\︱︲﹐﹑﹕﹘\﹣，\－：､…]
#       )
#         # Then consume and recurse -- we're still in a sentence.
#         (?P<continuous>
#           .[\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}\/\\#&,*+@$%^'"\-:;\(\)\[\]\{\}•՝،؍߸᠂᠈–—、︐︑・︓\︱︲﹐﹑﹕﹘\﹣，\－：､…]*
#         )
#         (?R)
#       |
#       # Otherwise, it's punctuation used at the end of a sentence.
#       (?!
#         [\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}\/\\#&,*+@$%^'"\-:;\(\)\[\]\{\}•՝،؍߸᠂᠈–—、︐︑・︓\︱︲﹐﹑﹕﹘\﹣，\－：､…]
#       )
#       # English sentences usually don't include characters after a period,
#       #   except in the case of phone numbers, decimals, so we catch those.
#       #   So we consume and recurse.
#       (?=.[A-z0-9])
#         (?P<latin>.{1,4}\p{P}*)
#         (?R)
#       |
#       # Likewise, we don't want to consider an ellipsis as the end of a sentence.
#       #   So we consume and recurse.
#       (?=\.{3})
#         (?P<ellipsis>\.{3})
#         (?R)
#       |
#       # Same with Mr., Ms., Jr., Dr.
#       (?<=\p{Lu}\p{Ll})
#         (?P<honorific>.)
#         (?R)
#       |
#       # And with Mrs., Inc.
#       (?<=\p{Lu}\p{Ll}{2})
#         (?<abbreviation>.)
#         (?R)
#       |
#       # If we've made it this far, then we're probably at the end of the sentence.
#       (?P<terminator>.\p{P}*)
#   )
#   |
#   # If it isn't punctuation, then we're looking at a newline...
#   (?!\p{Po})
#     # If it's a newline (which it should be), then we consume it.
#     (?=[\r\n])
#     (?P<newline>[\r\n])
#   |
#   # If somehow it isn't a newline, then the prior logic failed, are we're
#   #   actually looking at punctuation again. So we consume and recurse.
#   #   Ideally, this segment will never result in a successful match.
#   (?![\r\n])
#     (?P<initial>
#       [\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}\/\\#&,*+@$%^'"\-:;\(\)\[\]\{\}•՝،؍߸᠂᠈–—、︐︑・︓\︱︲﹐﹑﹕﹘\﹣，\－：､…]+
#     )
#     (?R)
# )
###

_PATTERN = ur"""(?x)
                (
                  (?:[^\p{Po}\r\n]*)
                  (?:
                    (?=\p{Po})
                    (?=
                      [\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}\/\\#&,*+@$%^'"\-:;\(\)\[\]\{\}•՝،؍߸᠂᠈–—、︐︑・︓\︱︲﹐﹑﹕﹘\﹣，\－：､…]
                    )
                    (?:
                      .[\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}\/\\#&,*+@$%^'"\-:;\(\)\[\]\{\}•՝،؍߸᠂᠈–—、︐︑・︓\︱︲﹐﹑﹕﹘\﹣，\－：､…]*
                    )
                    (?R)|
                    (?!
                      [\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}\/\\#&,*+@$%^'"\-:;\(\)\[\]\{\}•՝،؍߸᠂᠈–—、︐︑・︓\︱︲﹐﹑﹕﹘\﹣，\－：､…]
                    )
                    (?=.[A-z0-9])
                    (?:.{1,4}\p{P}*)
                    (?R)|
                    (?=\.{3})
                    (?:\.{3})
                    (?R)|
                    (?<=\p{Lu}\p{Ll})
                    (?:.)
                    (?R)|
                    (?<=\p{Lu}\p{Ll}{2})
                    (?:.)
                    (?R)|
                    (?:.\p{P}*)
                  )|
                  (?!\p{Po})
                  (?=[\r\n])
                  (?:[\r\n])|
                  (?![\r\n])
                  (?:
                    [\p{Pd}\p{Ps}\p{Pe}\p{Pi}\p{Pf}\p{Pc}\p{S}\/\\#&,*+@$%^'"\-:;\(\)\[\]\{\}•՝،؍߸᠂᠈–—、︐︑・︓\︱︲﹐﹑﹕﹘\﹣，\－：､…]+
                  )
                  (?R)
                )"""

_REGEX = regex.compile(_PATTERN, regex.UNICODE + regex.V1)

def sentence_split(text):
    return filter(None, [sentence.strip() for sentence in _REGEX.split(text)])