from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse

PIC_URL = "http://www.israelalbum.org.il/GetImage.ashx?PicName=multimedia/YBZ/0201-0300/YBZ_0255/YBZ_0255.PHOTO/{}.jpg"


class Photo(models.Model):
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

    exact_geom = models.PointField(null=True)

    place_name = models.CharField(max_length=300, null=True, blank=True)
    osm_id = models.CharField(max_length=500, null=True, blank=True)
    wikidata_id = models.CharField(max_length=500, null=True, blank=True)
    wikipedia_url = models.URLField(max_length=500, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('core:detail', args=(self.pk,))

    def pic_url(self):
        return PIC_URL.format(self.uid.replace(".", "_"))

    def pic_thumb_url(self):
        return self.pic_url() + "&width=200&height=200&mr=true"


class Place(models.Model):
    osm_id = models.CharField(max_length=500, unique=True)
    name = models.CharField(max_length=2500)
    geom = models.PointField()
    raw_data = JSONField()
    active = models.BooleanField(default=True)


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
