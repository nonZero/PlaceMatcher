from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

PIC_URL = "http://www.israelalbum.org.il/GetImage.ashx?PicName=multimedia/YBZ/0201-0300/YBZ_0255/YBZ_0255.PHOTO/{}.jpg"


class Country(models.Model):
    name = models.CharField(max_length=250)


class Photo(models.Model):
    class Accuracy:
        EXACT = 1
        ENTITY = 10
        BROAD = 100
        NO_PLACE_INFO = 200

        choices = (
            (EXACT, _('exact')),
            (ENTITY, _('entity')),
            (BROAD, _('broad')),
            (NO_PLACE_INFO, _('no place info')),
        )

    class Status:
        PENDING = 1
        SUGGESTED = 2
        FOUND = 10
        NOT_ENOUGH_INFO = 100
        NA = 200

        choices = (
            (PENDING, 'pending'),
            (SUGGESTED, 'suggested'),
            (FOUND, 'found'),
            (NOT_ENOUGH_INFO, 'no place name'),
            (NA, 'photo should not be associated with a place'),
        )

    class HelpRequest:
        NA = None
        YES = 1
        NO = 2

        choices = (
            (NA, 'N/A'),
            (YES, 'yes'),
            (NO, 'no'),
        )

    uid = models.CharField(max_length=500, unique=True)
    status = models.IntegerField(choices=Status.choices,
                                 default=Status.PENDING)
    title = models.CharField(max_length=2500)
    image_url = models.URLField()
    thumb_url = models.URLField(null=True, blank=True)

    place_name_hint = models.CharField(max_length=300, null=True, blank=True)
    geom_hint = models.PointField(null=True)

    geom = models.PointField(null=True)
    selected_place = models.ForeignKey("Place", on_delete=models.SET_NULL,
                                       related_name="photos", null=True)
    found_at = models.DateTimeField(null=True)

    request_public_help = models.IntegerField(choices=HelpRequest.choices,
                                              null=True, blank=True)

    country = models.ForeignKey(Country, null=True, blank=True,
                                on_delete=models.PROTECT)
    expected_accuracy = models.IntegerField(choices=Accuracy.choices,
                                            null=True, blank=True)

    exact_geom = models.PointField(null=True)
    exact_geom_radius = models.IntegerField(null=True)

    place_name = models.CharField(max_length=300, null=True, blank=True)
    geom_from_osm = models.PointField(null=True)
    osm_id = models.CharField(max_length=500, null=True, blank=True)
    wikidata_id = models.CharField(max_length=500, null=True, blank=True)
    wikipedia_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:detail', args=(self.pk,))

    def pic_url(self):
        return PIC_URL.format(self.uid.replace(".", "_"))

    def pic_thumb_url(self):
        return self.pic_url() + "&width=200&height=200&mr=true"

    def set_place(self, place: 'Place'):
        self.selected_place = place
        self.place_name = place.name
        self.geom_from_osm = place.geom
        self.osm_id = place.osm_id
        # self.wikidata_id = models.CharField(max_length=500, null=True, blank=True)
        # self.wikipedia_url = models.URLField(max_length=500, null=True, blank=True)


class Place(models.Model):
    osm_id = models.CharField(max_length=500, unique=True)
    name = models.CharField(max_length=2500)
    geom = models.PointField()
    raw_data = JSONField()
    active = models.BooleanField(default=True)

    @classmethod
    def from_nominatim_json(cls, info):
        names = info.get('namedetails', {})
        name = names.get('name:he', names.get('name'))
        return cls.objects.create(
            osm_id=f"{info['osm_type']}/{info['osm_id']}",
            geom=Point(float(info['lon']), float(info['lat'])),
            name=name,
        )


class Suggestion(models.Model):
    class Status:
        NEW = 1
        ACCEPTED = 10
        REJECTED = 100

        choices = (
            (NEW, 'new'),
            (ACCEPTED, 'accepted'),
            (REJECTED, 'rejected'),
        )

    photo = models.ForeignKey(Photo, on_delete=models.CASCADE,
                              related_name='suggestions')
    place = models.ForeignKey(Place, on_delete=models.CASCADE,
                              related_name='suggestions')
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()
    status = models.IntegerField(choices=Status.choices, default=Status.NEW)
