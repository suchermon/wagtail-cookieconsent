from unittest import mock
from faker import Faker

from django.test import TestCase, RequestFactory
from django.template import Context, Template
from django.template.loader import render_to_string


from .templatetags.wagtail_cookie_consent_tags import wagtail_cookie_consent_status
from .utils import underscore_string

fake = Faker()


class WagtailCookieConsentUtilTests(TestCase):
    def test_underscore_string_error_if_not_a_string_or_is_empty(self):
        with self.assertRaises(ValueError):
            underscore_string(None)
            underscore_string('')

    def test_undersocre_me_should_remove_special_chars(self):
        test_str = '$*%(Cookie Monster Is Hungry)!!!@'
        self.assertEqual('cookie_monster_is_hungry', underscore_string(test_str))


class WagtailCookieConsentBannerTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.banner_template = 'wagtailcookieconsent/consent_banner.html'

    def render_template(self, template, context=None):
        context = context or {}
        context = Context(context)
        template = '{% load wagtail_cookie_consent_tags wagtailsettings_tags %} {% get_settings use_default_site=True %}' + template
        return Template(template).render(context)

    @mock.patch('wagtailcookieconsent.templatetags.wagtail_cookie_consent_tags.messages')
    @mock.patch('wagtailcookieconsent.templatetags.wagtail_cookie_consent_tags.WagtailCookieConsent')
    def test_wagtail_cookie_consent_banner_with_no_settings_should_not_show_banner_and_error_msg_to_superadmin(self, mock_settings, mock_msg):
        request = self.factory.get('/')
        request.site = mock.Mock(return_value=1)
        request.user = mock.Mock()
        request.user.is_authenticated = True
        request.user.is_superadmin = True

        mock_settings.for_site.return_value.name = ''

        context = {}
        context['request'] = request

        rendered_template = self.render_template(
            '{% wagtail_cookie_consent_banner %}', context
        ).strip()

        cxt = context
        cxt['no_settings'] = True
        assert_template = render_to_string(self.banner_template, cxt).strip()

        self.assertTemplateUsed(template_name=self.banner_template)
        self.assertEqual(rendered_template, assert_template)
        self.assertEqual(0, len(rendered_template))

    @mock.patch('wagtailcookieconsent.templatetags.wagtail_cookie_consent_tags.WagtailCookieConsent')
    def test_wagtail_cookie_consent_banner_has_settings_with_no_cookie_set_should_show_banner(self, mock_settings):
        request = self.factory.get('/test/')
        request.site = mock.Mock()

        mock_settings.for_site.return_value.name = 'Cookie Monster'

        context = {}
        context['request'] = request

        rendered_template = self.render_template(
            '{% wagtail_cookie_consent_banner %}', context
        ).strip()

        cxt = context
        cxt['cookie_name'] = underscore_string('Cookie Monster')
        assert_template = render_to_string(self.banner_template, cxt).strip()

        self.assertTemplateUsed(template_name=self.banner_template)
        self.assertEqual(rendered_template, assert_template)


@mock.patch('wagtailcookieconsent.templatetags.wagtail_cookie_consent_tags.WagtailCookieConsent')
class WagtailCookieConsentGetCookieStatusTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.site = mock.Mock()
        self.context = {}

    def test_wagtail_cookie_status_returns_False_when_no_cookie_detected(self, mock_model):
        self.context['request'] = self.request
        mock_model.for_site.return_value.name = 'Cookie Monster'
        self.assertIsNone(wagtail_cookie_consent_status(self.context))

    def test_wagtail_cookie_status_returns_string_accepted_when_it_was_accepted(self, mock_model):
            self.request.COOKIES['yum_yum_cookie'] = 'accepted'
            self.context['request'] = self.request
            mock_model.for_site.return_value.name = 'Yum Yum Cookie!!'
            self.assertEqual('accepted', wagtail_cookie_consent_status(self.context))

    def test_wagtail_cookie_status_returns_string_declined_when_it_was_declined(self, mock_model):
            self.request.COOKIES['cookie_monster'] = 'declined'
            self.context['request'] = self.request
            mock_model.for_site.return_value.name = 'Cookie Monster'
            self.assertEqual('declined', wagtail_cookie_consent_status(self.context))
