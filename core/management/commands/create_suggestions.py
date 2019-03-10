from collections import Counter, defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction

from core.matching import FuzzyLookup
from core.models import Place, Photo

LIMIT = 8


def get_names():
    qs = Place.objects.filter(active=True)
    d = defaultdict(list)
    for o in qs:
        d[o.name].append(o.id)
    return d


class Command(BaseCommand):
    help = "Create suggestions using fuzzy matching"

    def handle(self, *args, **options):
        c = Counter()
        names = get_names()
        fuzzy = FuzzyLookup(names)

        qs = Photo.objects.filter(status=Photo.Status.PENDING).order_by("?")
        total = qs.count()
        print(total)
        for i, p in enumerate(qs, 1):
            s = p.title
            print(i, total, s)
            results = fuzzy.invoke(s, LIMIT)

            with transaction.atomic():
                p.suggestions.all().delete()

                for j, (name, score) in enumerate(results, 1):
                    print("*", j, name, score)
                    for pid in names[name]:
                        p.suggestions.create(
                            place=Place.objects.get(id=pid),
                            score=score,
                        )
                    c['suggestions'] += 1
                p.status = p.Status.SUGGESTED
                p.save()
            print()
            c['places'] += 1
        print(c)
