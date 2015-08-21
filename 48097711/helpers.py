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
    texts = s.split('\n')
    for t in texts:
        current = ''
        for _t in t.split(' '):
            current += _t + ' '
            if len(current) > l:
                yield current
                current = '  '
        if current:
            yield current
