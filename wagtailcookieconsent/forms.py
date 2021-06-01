from django import forms
from django.core.exceptions import ValidationError

from .models import WagtailCookieConsent
from .utils import underscore_string


class WagtailCookieConsentForm(forms.Form):
    cookie_name = forms.CharField(widget=forms.HiddenInput())
    cookie_action = forms.CharField(widget=forms.HiddenInput())
    next_url = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_cookie_name(self):
        cookie = self.cleaned_data['cookie_name']

        try:
            cookie_settings = WagtailCookieConsent.for_request(self.request)
        except WagtailCookieConsent.DoesNotExist:
            raise ValidationError('Invalid cookie name')

        if cookie_settings:
            if cookie != underscore_string(cookie_settings.name):
                raise ValidationError('Invalid cookie name')
        return cookie

    def clean_cookie_action(self):
        action = self.cleaned_data['cookie_action']
        if action not in ['accepted', 'declined']:
            raise ValidationError('Invalid action')
        return action
