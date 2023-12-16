import os

from celery import shared_task

from .models import Story


@shared_task
def remove_story(story_name: str = None) -> None:
    print(f"Removing story: {story_name}")
    Story.objects.get(story=story_name).delete()
    os.remove(path=("media/" + story_name))
