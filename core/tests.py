import pickle

from core.matching import fuzzy


def get_names():
    # qs = Place.objects.filter(active=True)
    # d = defaultdict(list)
    # for o in qs:
    #     d[o.name].append(o.id)
    # return d
    with open("names.pickle", "rb") as f:
        return pickle.load(f)


# @mark.django_db
def test_fuzzy():
    s = "מעברת עולים שעלו מתימן, כסלון בסמוך לרמת רזיאל, הרי יהודה"
    names = get_names()
    results = fuzzy(names, s)
    for t in results:
        print(t)
    # assert False, (names['כסלון'])
    assert False
