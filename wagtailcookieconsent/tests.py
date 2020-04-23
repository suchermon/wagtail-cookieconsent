from unittest import mock

from django.test import TestCase, RequestFactory
from django.template import Context, Template
from django.template.loader import render_to_string


from .templatetags.wagtail_cookie_consent_tags import wagtail_cookie_consent_status, underscore_me
from .views import WagtailCookieConsentSubmitView


class WagtailCookieMixinTests(TestCase):

    def setUp(self):
        super().setUp()
        self.posted_data = {
            'cookie_name': 'cookie_monster',
            'cookie_action': 'nonomnom',
            'next_url': '/'
        }

        self.factory = RequestFactory()
        self.request = self.factory.post('/cookies/consent/', self.posted_data, follow=True)
        self.view = WagtailCookieConsentSubmitView()
        self.view.setup(self.request)
        self.view.dispatch(self.request)

    def test_form_post_method_get_cookies_should_return_posted_cookie_info(self):
        self.assertEqual(self.view.get_cookies(), [(('cookie_monster', 'nonomnom'), {'max_age': 3600})])

    def test_redirect_should_redirect_to_next_url(self):
        resp = self.client.post('/cookies/consent/', self.posted_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/')


@mock.patch('wagtailcookieconsent.templatetags.wagtail_cookie_consent_tags.WagtailCookieConsent')
class WagtailCookieConsentBannerTests(TestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.context = {}
        self.context['request'] = self.request
        self.banner_template = 'wagtailcookieconsent/consent_banner.html'

    def render_template(self, template, context=None):
        context = context or {}
        context = Context(context)
        template = '{% load wagtail_cookie_consent_tags wagtailsettings_tags %} {% get_settings use_default_site=True %}' + template
        return Template(template).render(context)

    def test_wagtail_cookie_consent_banner_with_no_cookie_set_should_show_banner(self, mock_model):
        mock_model.objects.all.return_value.first.return_value.name = 'Cookie Yum'

        rendered_template = self.render_template(
            '{% wagtail_cookie_consent_banner %}', self.context
        ).strip()

        self.assertTemplateUsed(template_name=self.banner_template)
        self.assertIn('cookieConsentBanner', rendered_template)

    def test_wagtail_cookie_consent_banner_should_not_insert_html_when_it_has_a_value(self, mock_model):
        self.request.COOKIES['cookie_is_yummy'] = 'accepted'
        mock_model.objects.all.return_value.first.return_value.name = 'Cookie Is Yummy!'

        rendered_template = self.render_template(
            '{% wagtail_cookie_consent_banner %}', self.context
        ).strip()

        self.assertTemplateUsed(template_name=self.banner_template)
        self.assertNotIn('cookieConsentBanner', rendered_template)


@mock.patch('wagtailcookieconsent.templatetags.wagtail_cookie_consent_tags.WagtailCookieConsent')
class WagtailCookieConsentGetCookieStatusTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.context = {}

    def test_undersocre_me_should_remove_special_chars(self, mock_model):
        test_str = 'Cookie Monster Is Hungry!!!'
        self.assertEqual('cookie_monster_is_hungry', underscore_me(test_str))

    def test_wagtail_cookie_status_returns_False_when_no_cookie_detected(self, mock_model):
        self.context['request'] = self.request
        mock_model.objects.all.return_value.first.return_value.name = 'Cookie Monster'
        self.assertIsNone(wagtail_cookie_consent_status(self.context))

    def test_wagtail_cookie_status_returns_cookie_value_accepted(self, mock_model):
            self.request.COOKIES['yum_yum_cookie'] = 'accepted'
            self.context['request'] = self.request
            mock_model.objects.all.return_value.first.return_value.name = 'Yum Yum Cookie!!'
            self.assertEqual('accepted', wagtail_cookie_consent_status(self.context))

    def test_wagtail_cookie_status_returns_cookie_value_declined(self, mock_model):
            self.request.COOKIES['cookie_monster'] = 'declined'
            self.context['request'] = self.request
            mock_model.objects.all.return_value.first.return_value.name = 'Cookie Monster'
            self.assertEqual('declined', wagtail_cookie_consent_status(self.context))
