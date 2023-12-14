from django.db import models

from PIL import Image as I

from apps.userauth.models import CustomUser


class Story(models.Model):
    ...


# stories = models.IntegerField(default=0, validators=[
#         MinValueValidator(limit_value=0, message="Stories number cannot be negative!")
#     ])


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
