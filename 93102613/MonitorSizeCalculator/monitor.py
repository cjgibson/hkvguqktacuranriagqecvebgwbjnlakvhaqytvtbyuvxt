###
# AUTHORS: CHRISTIAN GIBSON,
# PROJECT: MONITOR SIZE CALCULATOR
# UPDATED: JUNE 23, 2015
# USAGE:
# EXPECTS: python 2.7.6
###

def best_match(odiag, ores, mdiag, masp=None, verbose=False):
    mdiag, mres, masp = match_monitor(odiag, ores, mdiag, masp=masp)
    oppi = calculate_ppi(odiag, ores)
    odim = calculate_side_length(odiag, ores)
    diff = float('inf')
    bmon = None
    for _mres in standard_resolutions(masp):
        _mppi = calculate_ppi(mdiag, _mres)
        if diff > abs(oppi - _mppi):
            diff = abs(oppi - _mppi)
            bmon = (mdiag, _mres, masp, diff, (diff * odim[0], diff * odim[1]))
            if verbose:
                print bmon
        else:
            return bmon


def match_monitor(odiag, ores, mdiag=None, mres=None, masp=None):
    if not any([mdiag, mres]):
        return None
    if not ((mdiag and isinstance(mdiag, (int, float)))
             or (mres and len(mres) == 2)
             or isinstance(odiag, (int, float))
             or len(ores) == 2):
        return None
    oppi = calculate_ppi(odiag, ores)
    if mdiag:
        if masp and len(masp) == 2:
            oasp = masp
        else:
            oasp = simplify_fraction(ores[0], ores[1])
        mres = float(mdiag ** 2 * (ores[0] ** 2 + ores[1] ** 2)) / odiag ** 2
        mres = (mres * (1.0 / (oasp[0] ** 2 + oasp[1] ** 2))) ** 0.5
        mres = (mres * oasp[0], mres * oasp[1])
    else:
        mdiag = float(odiag * (mres[0] ** 2 + mres[1] ** 2) ** 0.5)
        mdiag = mdiag / (ores[0] ** 2 + ores[1] ** 2) ** 0.5
        oasp = simplify_fraction(mres[0], mres[1])
    return (mdiag, mres, oasp)


def calculate_ppi(diag, res):
    if (isinstance(diag, (int, float))
        and isinstance(res, (list, tuple))
        and len(res) > 1):
        return (res[0] ** 2 + res[1] ** 2) ** (0.5) / float(diag)
    else:
        return None


def calculate_side_length(diag, asp):
    if (isinstance(diag, (int, float))
        and isinstance(asp, (list, tuple))
        and len(asp) > 1):
        asp = simplify_fraction(asp[0], asp[1])
        red = float(diag) / (asp[0] ** 2 + asp[1] ** 2) ** 0.5
        return (asp[0] * red, asp[1] * red)
    else:
        return None


def standard_resolutions(asp, limit=float('inf')):
    if not (isinstance(asp, (list, tuple))
            and len(asp) > 1):
        yield None
    x, y = asp[0] * 8, asp[1] * 8
    _x, _y = x, y
    while limit:
        yield (_x, _y)
        _x, _y = (_x + x, _y + y)
        limit -= 1


def simplify_fraction(n, d):
    if d == 0:
        return None
    c = _gcd(n, d)
    return (n / c, d / c)


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a
