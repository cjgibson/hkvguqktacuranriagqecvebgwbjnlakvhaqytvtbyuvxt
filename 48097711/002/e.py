###
# AUTHORS: CHRISTIAN GIBSON,
# PROJECT: REDDIT CHALLENGES
# UPDATED: FEBURARY 28, 2015
# USAGE:
# EXPECTS: python 2.7.6
###

__task__ = """
Hello, coders! An important part of programming is being able to apply your
programs, so your challenge for today is to create a calculator application
that has use in your life. It might be an interest calculator, or it might
be something that you can use in the classroom. For example, if you were
in physics class, you might want to make a F = M * A calc.
EXTRA CREDIT: make the calculator have multiple functions! Not only should
it be able to calculate F = M * A, but also A = F/M, and M = F/A!
"""

import collections

class calculator():
    def __init__(self):
        self.function = {'+': self._add,
                         '-': self._sub,
                         '*': self._mul,
                         '/': self._div,
                         '^': self._pow,
                         '%': self._mod,
                         '!': self._fac}
        self.factorial_helper = [1, 1, 2]

    def calculate(self, input):
        pass

    def _func(self, a, b, f):
        if not (isinstance(a, (float, complex))
                and isinstance(b, (float, complex))):
            a = self._coerce_numeric(a)
            b = self._coerce_numeric(b)
        return f(a, b)

    def _coerce_numeric(self, v):
        if isinstance(v, (int, float, long, complex)):
            return v
        else:
            try:
                return float(v)
            except:
                return self._coerce_base(v)

    def _coerce_base(self, v, b=None):
        if set(v).issubset(set('-0.')):
            return 0

        negative = 1
        if '-' in v:
            v = v.replace('-', '')
            negative = -1

        digits = '0123456789'
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        m_lookup = dict(zip(list(digits)
                            + list(alphabet.lower())
                            + list(alphabet),
                            range(0, 62)))

        if b:
            if b < 2 or b > 62:
                raise ValueError("only supports bases in range(2, 63).")
            if all([_v.isdigit() or _v in alphabet for _v in v]):
                v = v.lower()
            v = list(v)
            r = 0
            while v:
                n = v.pop(0)
                if m_lookup[n] > b:
                    raise ValueError("digit '%s' out of range for base %s."
                                     % (n, b))
                r += m_lookup[n] * b ** len(v)
            return negative * r
        else:
            import re
            v = re.sub('[^0-9a-zA-Z]', '', v)
            if (all([_v.isdigit() or _v in alphabet.lower() for _v in v])
                or all([_v.isdigit() or _v in alphabet for _v in v])):
                v = v.lower()
                b = m_lookup[max(v)] + 1
                return self._coerce_base(v, b)
            else:
                b = m_lookup[max(v)] + 1
                return self._coerce_base(v, b)

    def _add(self, a, b):
        return a + b

    def _sub(self, a, b):
        return a - b

    def _mul(self, a, b):
        return a * b

    def _div(self, a, b):
        return a / b

    def _pow(self, a, b):
        return a ** b

    def _mod(self, a, b):
        return a % b

    def _fac(self, a):
        if a < 0:
            return None
        l = len(self.factorial_helper)
        while l < a + 1:
            self.factorial_helper.append(l * self.factorial_helper[-1])
            l += 1
        return self.factorial_helper[a]

    def _root(self, a, r):
        return a ** (1 / r)
