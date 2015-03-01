###
# AUTHORS: CHRISTIAN GIBSON, 
# PROJECT: REDDIT CHALLENGES
# UPDATED: FEBURARY 28, 2015
# USAGE:   
# EXPECTS: python 2.7.6
###

def group(s):
    for g in _group(s):
        print g

def _group(s, l=70):
    import re
    r = ''
    n = [_s for _s in re.split('[ \t]', s)]
    while n:
        r += n.pop(0)
        if '\n' in r or '\r' in r:
            r = re.split('[\n\r]', r)
            yield r[0]
            r = r[1] + ' '
        elif len(r) > l:
            yield r
            r = ''
        else:
            r += ' '
    yield r
