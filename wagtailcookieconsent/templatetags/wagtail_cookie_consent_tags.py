import re
from django import template
from wagtailcookieconsent.models import WagtailCookieConsent

register = template.Library()


def underscore_me(str):
    return re.sub('\W+', ' ', str.lower()).strip().replace(' ', '_')


@register.inclusion_tag('wagtailcookieconsent/consent_banner.html', takes_context=True)
def wagtail_cookie_consent_banner(context):
    '''
    Insert the banner html and forms if no cookies were found

    Usage:
    {% wagtail_cookie_consent_banner %}

    Arguments:
        context {obj} -- context
        cookie_name {str} -- Name of the cookie defined in the admin/db and converted into lower case underscore string
        consent_exists {str} -- Returns value the value of the cookie or None
    '''
    request = context['request']
    # FIXME: Should check for the site's settings just like using {% get_settings %}
    cookie_name = WagtailCookieConsent.objects.all().first().name
    cookie = underscore_me(cookie_name)

    return {
        'request': request,
        'cookie_name': cookie,
        'consent_exists': request.COOKIES.get(cookie, None),
        'settings': context['settings']
    }


@register.simple_tag(takes_context=True)
def wagtail_cookie_consent_status(context):
    '''
    Just a simple tag to check for an existence of a cookie. Example:

    {% wagtail_cookie_consent_status  %}

    returns 'accepted' | 'declined' | False (if not set at all)
    '''
    # FIXME: Should check for the site's settings just like using {% get_settings %}
    cookie_name = WagtailCookieConsent.objects.all().first().name
    cookie = underscore_me(cookie_name)
    return context['request'].COOKIES.get(cookie, None)
