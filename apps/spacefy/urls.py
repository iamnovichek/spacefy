from django.urls import path
from django.views.generic import TemplateView

from .views import (MySpaceView, EditMySpaceView, CreateMySpaceView,
                    AddPostView, MyPostsView, AddPhotoView,
                    MyPhotosView, AddStoryView, SearchUsersAjaxView,
                    AnotherSpaceView, AnotherSpacePostsView, AnotherSpacePhotosView,
                    AddToFriendsAjaxView, RemoveFromFriendsAjaxView, MySpaceFriendsView,
                    AnotherSpaceFriendsView, LikeAjaxView, UnlikeAjaxView)

urlpatterns = [
    path('', TemplateView.as_view(template_name='apps.spacefy/home.html'), name='home'),
    path('my-space/', MySpaceView.as_view(), name='my-space'),
    path('edit-my-space/<slug:slug>/', EditMySpaceView.as_view(), name='edit-my-space'),
    path('create-profile/', CreateMySpaceView.as_view(), name='create-profile'),
    path('create-post/', AddPostView.as_view(), name='create-post'),
    path('add-photo/', AddPhotoView.as_view(), name='add-photo'),
    path('my-posts/', MyPostsView.as_view(), name='my-posts'),
    path('my-photos/', MyPhotosView.as_view(), name='my-photos'),
    path('add-story/', AddStoryView.as_view(), name='add-story'),
    path('users-search/', SearchUsersAjaxView.as_view(), name='user-search'),
    path('another-space/<str:username>/', AnotherSpaceView.as_view(), name='another-space'),
    path('another-space/posts/<str:username>/', AnotherSpacePostsView.as_view(), name='another-space-posts'),
    path('another-space/photos/<str:username>/', AnotherSpacePhotosView.as_view(), name='another-space-photos'),
    path('add-to-friends/<str:username>/', AddToFriendsAjaxView.as_view(), name='add-2-friends'),
    path('remove-from-friends/<str:username>/', RemoveFromFriendsAjaxView.as_view(), name='remove-from-friends'),
    path('my-friends/', MySpaceFriendsView.as_view(), name='my-friends'),
    path('another-space-friends/<str:username>/', AnotherSpaceFriendsView.as_view(), name='another-space-friends'),
    path('like/', LikeAjaxView.as_view(), name='like'),
    path('unlike/', UnlikeAjaxView.as_view(), name='unlike'),
]
