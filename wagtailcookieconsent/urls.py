from django.urls import path
from django.views.generic.base import TemplateView

from wagtailcookieconsent.views import WagtailCookieConsentSubmitView


app_name = 'wagtailcookieconsent'

urlpatterns = [
    path('consent/', WagtailCookieConsentSubmitView.as_view(), name='consent'),
    path('info/', TemplateView.as_view(template_name='wagtailcookieconsent/info.html'), name='info'),
]
