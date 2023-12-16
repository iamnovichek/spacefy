from django.db import models

from PIL import Image as I

from apps.userauth.models import CustomUser
from .validators import file_size_validator, file_type_validator


class Story(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    story = models.FileField(upload_to='stories', validators=[file_size_validator,
                                                              file_type_validator])
    creared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.userprofile.username + " - " + self.story.name


class Gallery(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.userprofile.username + " - " + self.description


class Image(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos')

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)
        img = I.open(self.image.path)
        img.thumbnail(size=(300, 300))
        img.save(fp=self.image.path)
        return super().save()


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:10] + "..."


class Friend(models.Model):
    ...
# friends = models.IntegerField(default=0, validators=[
#         MinValueValidator(limit_value=0, message="Friends number cannot be negative!")
#     ])
# relate after with userprofile using foreignkey
