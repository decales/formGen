import itertools
from difflib import SequenceMatcher

def ranges(l):
    r = []
    for a, b in itertools.groupby(enumerate(l), lambda pair: pair[1] - pair[0]):
        b = list(b)
        if b[0][1] == b[-1][1]:
            r.append((b[0][1]))
        else:
            r.append((b[0][1], b[-1][1]))
    return r


def getFix(l):
    i = 1
    while len(l[0]) != len(l[i]):
        i = i + 1
    match = SequenceMatcher(None, l[0], l[i]).find_longest_match()
    return l[0][match.a:match.a + match.size]


def getDigits(l):
    digits = []
    for i in l:
        if i.isdigit():
            digits.append(i)
            l.remove(i)
    return digits


def rangify(transfer, l):
    try:
        if len(l) == 0:
            return "Error"
        if len(l) == 1:
            return "'{}'".format(str(l[0]))
        if len(l) == 2:
            return "'{}', '{}'".format(l[0], l[1])

        temp = []
        rangeStr = ""
        fix = getFix(l)
        if fix != '':
            x = l[0].split(fix)
            if x[0] == '':
                for i in range(len(l)):
                    temp.append(int(l[i].split(fix)[1]))
                temp.sort()
                temp = list(ranges(temp))
                for i in temp:
                    if type(i) == tuple:
                        rangeStr += "'{}{}' - '{}{}', ".format(fix, str(i[0]), fix, str(i[1]))
                    else:
                        rangeStr += "'{}{}', ".format(fix, str(i))
            else:
                for i in range(len(l)):
                    temp.append(int(l[i].split(fix)[0]))
                temp.sort()
                temp = list(ranges(temp))
                for i in temp:
                    if type(i) == tuple:
                        rangeStr += "'{}{}' - '{}{}', ".format(str(i[0]), fix, str(i[1]), fix)
                    else:
                        rangeStr += "'{}{}', ".format(str(i), fix)
            return rangeStr[:-2]
        else:
            for i in l:
                temp.append(int(i))
            temp.sort()
            temp = list(ranges(temp))
            for i in temp:
                if type(i) == tuple:
                    rangeStr += "'{}' - '{}', ".format(str(i[0]), str(i[1]))
                else:
                    rangeStr += "'{}',".format(str(i))
        return rangeStr[:-2]
    except Exception:
        print("WARNING: Transfer {} - Failed to create box range. Full list of boxes will be used instead".format(transfer))
        return str(l).strip('[]')