import datetime
from django.views.generic import FormView
from django.http import HttpResponseRedirect

from .forms import WagtailCookieConsentForm
from .models import WagtailCookieConsent


class CookieMixin:
    """
    Credit: https://gist.github.com/bmispelon/7700152

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

    def days_to_milliseconds(self, days=30):
        """

        Convert number of days into milliseconds. Default is 30 days.

        Keyword Arguments:
            days {number} -- [description] (default: {30})

        Returns:
            number -- in milliseconds
        """
        return days * 24 * 60 * 60

    def calculate_expires(self, days=30):
        """
        Calculate datetime.datetime object in UTC to be used as `expires`

        [description]

        Keyword Arguments:
            days {number} -- [description] (default: {30})

        Returns:
            String -- UTC datetime object
        """

        return datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=days), "%a, %d-%b-%Y %H:%M:%S GMT")

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

    def post(self, request, *args, **kwargs):
        """
        Get the response object from the parent class and sets the cookies on
        it accordingly.
        """
        response = super().dispatch(request, *args, **kwargs)
        for cookie_args, cookie_kwargs in self.get_cookies():
            response.set_cookie(*cookie_args, **cookie_kwargs)
        return response


class WagtailCookieConsentSubmitView(CookieMixin, FormView):
    template_name = 'wagtailcookieconsent/forms/cookie_submit_forms.html'
    form_class = WagtailCookieConsentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_invalid(self, form):
        return HttpResponseRedirect(self.request.POST.get('next_url', '/'))

    def form_valid(self, form):
        cookie_name = form.cleaned_data.get('cookie_name', None)
        cookie_action = form.cleaned_data.get('cookie_action', None)

        if cookie_name and cookie_action:
            try:
                cookie_settings = WagtailCookieConsent.for_request(self.request)
            except WagtailCookieConsent.DoesNotExist:
                pass

            if cookie_settings is not None and cookie_settings.expiration:
                MAX_AGE = self.days_to_milliseconds(cookie_settings.expiration)
                EXPIRES = self.calculate_expires(cookie_settings.expiration)

                self.add_cookie(
                    cookie_name,
                    cookie_action,
                    max_age=MAX_AGE,
                    expires=EXPIRES,
                    secure=True
                )
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.POST.get('next_url', None)

        if next_url:
            return '%s' % (next_url)
        else:
            return '/'
