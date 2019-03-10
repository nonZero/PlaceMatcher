from collections import Counter

import pandas as pd
from django.core.management.base import BaseCommand

from core.models import Photo

FILENAME = "./YBZ_0255_Table.xlsx"

COLS = dict((
    ('code', 'קוד תמונה'),
    ('title', 'כותרת '),
    ('desc', 'תיאור'),
    ('notes', 'הערות'),
    ('title_en', 'כותרת בלועזית'),
    ('from_date', 'מתאריך '),
    ('to_date', 'עד תאריך'),
    ('photographer', 'צלם'),
    ('professional_photographer', 'צלם מקצועי'),
    ('archiver_note', 'הערת מקטלג'),
    ('source', 'מקור התמונה'),
    ('place', 'מקום/כתובת'),
    ('latlng', 'נ.צ. גוגל'),
))

URL_TEMPLATE = "http://www.israelalbum.org.il/GetImage.ashx?PicName=multimedia/YBZ/0201-0300/YBZ_0255/YBZ_0255.PHOTO/{}.jpg"


class Command(BaseCommand):
    help = "Import photos from csv file"

    def handle(self, *args, **options):
        c = Counter()
        df = pd.read_excel(FILENAME, sheet_name=1, names=COLS)
        total = len(df)
        for i, row in df.iterrows():
            print(i + 1, total, row.code)
            p, created = Photo.objects.update_or_create(
                uid=row.code,
                defaults=dict(
                    title=row.title,
                    image_url=URL_TEMPLATE.format(row.code),
                    # thumb_url =
                )
            )
            c['created' if created else 'updated'] += 1
        print(c)
