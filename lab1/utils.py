from collections import UserDict
import regex as re


class ClobberedDictKey(Exception):
    "A flag that a variable has been assigned two incompatible values."
    pass


class NoClobberDict(UserDict):

    """
    A dictionary-like object that prevents its values from being
    overwritten by different values. If that happens, it indicates a
    failure to match.
    """

    def __init__(self, initial_dict=None):
        if initial_dict == None:
            self._dict = {}
        else:
            self._dict = dict(initial_dict)

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        if key in self._dict and self._dict[key] != value:
            raise ClobberedDictKey((key, value))

        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __contains__(self, key):
        return self._dict.__contains__(key)

    def __iter__(self):
        return self._dict.__iter__()

    def iteritems(self):
        return self._dict.iteritems()

    def keys(self):
        return self._dict.keys()


AIRegex = re.compile(r'\(\?(\S+)\)')


def AIStringToRegex(AIStr):
    res = AIRegex.sub(r'(?P<\1>\\S+)', AIStr) + '$'
    return res


def AIStringToPyTemplate(AIStr):
    return AIRegex.sub(r'%(\1)s', AIStr)


def AIStringVars(AIStr):
    return set([AIRegex.sub(r'\1', x) for x in AIRegex.findall(AIStr)])
