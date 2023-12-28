from django.shortcuts import redirect

USER_ACCESS_DENIED_PATHS = frozenset((
    '/auth/password-reset/done/', '/auth/password-reset-complete/'
))


class UserauthPagesAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
                request.path == '/auth/password-reset/':
            return redirect('home')

        if request.path in USER_ACCESS_DENIED_PATHS:
            if request.META.get('HTTP_X_REQUESTED_WITH', ''):
                return self.get_response(request)
            else:
                return redirect('home')

        return self.get_response(request)
