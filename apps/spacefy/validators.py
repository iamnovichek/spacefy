from django.core.exceptions import ValidationError

from . import image_file_extensions, video_file_extensions


def file_type_validator(file):
    file_extention = file.name.split('.')[-1]
    if not (file_extention in image_file_extensions or
            file_extention in video_file_extensions):
        raise ValidationError("Upload a mediafile!")


def file_size_validator(file):
    if file.size > 10485760:
        raise ValidationError('Your file size cannot exeed 10Mb!')
