from django import template
from django.contrib import messages

from wagtail.core import __version__ as WAGTAIL_VERSION

from ..models import WagtailCookieConsent
from ..utils import underscore_string

register = template.Library()


@register.inclusion_tag('wagtailcookieconsent/consent_banner.html', takes_context=True)
def wagtail_cookie_consent_banner(context):
    '''
    Insert the banner html and forms if no cookies were found an ignore the whole thing completely if the settings were not set at all

    Usage:
    {% wagtail_cookie_consent_banner %}

    Arguments:
        context {obj} -- context
        cookie_settings {str} -- Name of the cookie defined in the admin/db and converted into lower case underscore string
        consent_exists {str} -- Returns the value of the cookie or None
    '''
    request = context['request']

    try:
        # Can't access the context['settings'] to get the site settings

        if WAGTAIL_VERSION < '2.10':
            cookie_settings = WagtailCookieConsent.for_site(request.site)
        else:
            cookie_settings = WagtailCookieConsent.for_request(request)
    except WagtailCookieConsent.DoesNotExist:
        cookie_settings = None

    if cookie_settings and cookie_settings.name:
        cookie_name = underscore_string(cookie_settings.name)
        context.update({
            'cookie_name': cookie_name,
            'consent_exists': request.COOKIES.get(cookie_name, None),
        })
    else:
        if request.user.is_authenticated and request.user.is_superadmin:
            messages.warning(request, "WagtalCookieConsent doesn't have any settings.")

        context['no_settings'] = True

    return context


@register.simple_tag(takes_context=True)
def wagtail_cookie_consent_status(context):
    '''
    Just a simple tag to check for an existence of a cookie. Example:

    {% wagtail_cookie_consent_status  %}

    returns 'accepted' | 'declined' | None (if not set at all)
    '''

    request = context['request']

    try:
        if WAGTAIL_VERSION < '2.10':
            cookie_settings = WagtailCookieConsent.for_site(request.site)
        else:
            cookie_settings = WagtailCookieConsent.for_request(request)
    except WagtailCookieConsent.DoesNotExist:
        cookie_settings = None

    if cookie_settings and cookie_settings.name:
        cookie = underscore_string(cookie_settings.name)

    return request.COOKIES.get(cookie, None)
