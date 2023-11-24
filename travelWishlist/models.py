from dask.rewrite import args
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

# Create your models here.

# get the length of the model
# get if its true or false if you visted a place
class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

def save(self, args, old_photo=None, **kwargs):
    old_place = Place.objects.filters(pk=self.pk).first()
    if old_place and old_place.photo:
        if old_photo.photo != self.photo:
            self.delete_photo(old_place.photo)

    super().save(*args, **kwargs)

def delete_photo(self, photo):
    if default_storage.exists(photo.name):
        default_storage.delete(photo.name)






def __str__(self):
    photo_str = self.photo.url if self.photo else 'no photo'
    notes_str = self.notes[100:]
    return f'{self.name}, visited? {self.visited}, Notes: {notes_str} , Photo {photo_str}'
