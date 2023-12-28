from django.shortcuts import redirect

from apps.userauth.models import UserProfile

NORMAL_PATHS = frozenset(('/create-post/', '/add-photo/',
                          '/my-posts/', '/my-photos/',
                          '/add-story/', '/my-friends/'))

AJAX_PATHS_WITH_ARGUMENTS = frozenset(('/add-to-friends/',
                                       '/remove-from-friends/'))

NORMAL_AJAX_PATHS = frozenset(('/like/', '/users-search/',
                               '/unlike/'))


class AdminSiteAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.path == '/admin/':
            if request.user.is_authenticated:
                if request.user.is_admin:
                    return self.get_response(request)
                else:
                    return redirect('home')
            else:
                return redirect('home')
        else:
            return self.get_response(request)


class SpacefyPagesAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.path == '/create-profile/':
            if UserProfile.objects.filter(user=request.user).exists():
                return redirect('my-space')
            else:
                return self.get_response(request)

        if request.path in NORMAL_PATHS:
            if UserProfile.objects.filter(user=request.user).exists():
                return self.get_response(request)
            else:
                return redirect('create-profile')

        if "/edit-my-space/" in request.path:
            if UserProfile.objects.filter(slug=request.
               path.split('/')[2]).exists():
                return self.get_response(request)
            else:
                return redirect('create-profile')

        return self.get_response(request)


class AjaxURLsAccessMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        for path in AJAX_PATHS_WITH_ARGUMENTS:
            if path in request.path and \
                    request.path != '/':
                if request.META.get('HTTP_X_REQUESTED_WITH', ''):
                    return self.get_response(request)
                else:
                    return redirect('home')

        if request.path in NORMAL_AJAX_PATHS:
            if request.META.get('HTTP_X_REQUESTED_WITH', ''):
                return self.get_response(request)
            else:
                return redirect('home')

        return self.get_response(request)
