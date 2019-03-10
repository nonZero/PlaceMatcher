import re
from _operator import itemgetter

from fuzzywuzzy import process


class FuzzyLookup:
    def __init__(self, names):
        self.names = names
        self.suggestions = list(names)

    def _parts(self, a):
        for i in range(len(a), 0, -1):
            for j in range(len(a) - i + 1):
                yield a[j:i + j]

    def invoke(self, s, limit):
        return sorted(
            self._invoke(s, limit),
            key=itemgetter(1),
            reverse=True
        )

    def _invoke(self, t, limit):
        t = t.replace("ג'", "ג")
        a = [w for w in re.split(r"""[-'")(\s,./]+""", t.strip()) if w]

        seen = set()

        for p in self._parts(a):
            w = " ".join(p)
            if w in self.names:
                yield (w, 500)
                seen.add(w)
            if w[1:] in self.names:
                yield (w[1:], 300)
                seen.add(w[1:])
        for n in self.names:
            if n not in seen and n in t:
                yield (n, 200)
                seen.add(n)

        results = process.extract(t, self.suggestions, limit=limit)
        for n, v in results:
            if n not in seen:
                yield n, v
