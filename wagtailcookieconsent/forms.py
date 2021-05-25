from django import forms
from django.core.exceptions import ValidationError


class WagtailCookieConsentForm(forms.Form):
    cookie_name = forms.CharField(widget=forms.HiddenInput())
    cookie_action = forms.CharField(widget=forms.HiddenInput())
    next_url = forms.CharField(widget=forms.HiddenInput())

    def clean_cookie_action(self):
        action = self.cleaned_data['cookie_action']
        if action not in ['accepted', 'declined']:
            raise ValidationError('Invalid action')
        return action
