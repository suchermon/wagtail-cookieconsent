from django.views.generic import RedirectView

from .forms import WagtailCookieConsentForm


class CookieMixin(object):
    """
    https://gist.github.com/bmispelon/7700152
    A CBV mixin that adds an `add_cookie` method on the view, allowing the user
    to set cookies on the response without having direct access to the response
    object itself.

    Example usage::

        class SomeFormView(CookieMixin, FormView):
            ...

            def form_valid(self, form):
                self.add_cookie('form_was_sent', True, max_age=3600)
                return super(SomeFormView, self).form_valid(form)

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cookies = []

    def get_cookies(self):
        """
        Return an iterable of (args, kwargs) to be passed to set_cookie.
        """
        return self._cookies

    def add_cookie(self, *args, **kwargs):
        """
        Al given arguments will be passed to response.set_cookie later on.
        """
        self._cookies.append((args, kwargs))

    def dispatch(self, request, *args, **kwargs):
        """
        Get the response object from the parent class and sets the cookies on
        it accordingly.
        """
        response = super().dispatch(request, *args, **kwargs)
        for cookie_args, cookie_kwargs in self.get_cookies():
            response.set_cookie(*cookie_args, **cookie_kwargs)
        return response


class WagtailCookieConsentSubmitView(CookieMixin, RedirectView):
    form_class = WagtailCookieConsentForm

    def post(self, request, *args, **kwargs):
        cookie_name = request.POST.get('cookie_name', None)
        cookie_action = request.POST.get('cookie_action', None)
        if cookie_name and cookie_action:
            self.add_cookie(cookie_name, cookie_action, max_age=3600)
        return super().post(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        next_url = self.request.POST.get('next_url', None)

        if next_url:
            return '%s' % (next_url)
        else:
            return '/'
