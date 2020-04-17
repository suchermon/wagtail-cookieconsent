from django import template
from wagtailcookieconsent.models import WagtailCookieConsent

register = template.Library()


@register.inclusion_tag('wagtailcookieconsent/consent_banner.html', takes_context=True)
def wagtail_cookie_consent_banner(context):
    '''
    Insert the html and forms

    Usage:
    {% wagtail_cookie_consent_banner %}

    Arguments:
        context {[type]} -- [description]
        cookie_name {[type]} -- [description]
    '''
    request = context['request']
    # FIXME: Should check for the site's settings just like using {% get_settings %}
    cookie_name = WagtailCookieConsent.objects.all().first().name
    cookie = cookie_name.lower().replace(' ', '_')

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
    cookie = cookie_name.lower().replace(' ', '_')
    return context['request'].COOKIES.get(cookie, None)
