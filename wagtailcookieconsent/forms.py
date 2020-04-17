from django import forms


class WagtailCookieConsentForm(forms.Form):
    cookie_name = forms.CharField(widget=forms.HiddenInput())
    cookie_value = forms.CharField(widget=forms.HiddenInput())
