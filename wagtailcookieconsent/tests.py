from unittest import mock

from django.test import TestCase, RequestFactory
from django.template import Context, Template
from django.template.loader import render_to_string


from .templatetags.cookie_consent_tags import wagtail_cookie_consent_status, underscore_me


@mock.patch('wagtailcookieconsent.templatetags.cookie_consent_tags.WagtailCookieConsent')
class WagtailCookieConsentBannerTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.context = {}
        self.context['request'] = self.request
        self.banner_template = 'wagtailcookieconsent/consent_banner.html'

    def render_template(self, template, context=None):
        context = context or {}
        context = Context(context)
        template = '{% load cookie_consent_tags wagtailsettings_tags %} {% get_settings use_default_site=True %}' + template
        return Template(template).render(context)

    def test_wagtail_cookie_consent_banner_with_no_cookie_set_should_show_banner(self, mock_model):
        # self.request.COOKIES['cookie_monster'] = 'declined'
        mock_model.objects.all.return_value.first.return_value.name = 'Cookie Monster'

        rendered_template = self.render_template(
            '{% wagtail_cookie_consent_banner %}', self.context
        ).strip()

        cxt = self.context
        cxt['cookie_name'] = underscore_me('Cookie Monster')
        assert_template = render_to_string(self.banner_template, cxt).strip()

        self.assertTemplateUsed(template_name=self.banner_template)
        self.assertEqual(rendered_template, assert_template)

    def test_wagtail_cookie_consent_banner_should_not_insert_html_after_accepted(self, mock_model):
        self.request.COOKIES['me_have_cookie'] = 'accepted'
        mock_model.objects.all.return_value.first.return_value.name = 'Me Have Cookie'

        rendered_template = self.render_template(
            '{% wagtail_cookie_consent_banner %}', self.context
        ).strip()

        cxt = self.context
        cxt['cookie_name'] = underscore_me('Me Have Cookie')
        cxt['consent_exists'] = 'accepted'
        assert_template = render_to_string(self.banner_template, cxt).strip()

        self.assertTemplateUsed(template_name=self.banner_template)
        self.assertEqual(rendered_template.strip(), render_to_string(self.banner_template, cxt).strip())


@mock.patch('wagtailcookieconsent.templatetags.cookie_consent_tags.WagtailCookieConsent')
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

    def test_wagtail_cookie_status_returns_string_accepted_when_it_was_accepted(self, mock_model):
            self.request.COOKIES['yum_yum_cookie'] = 'accepted'
            self.context['request'] = self.request
            mock_model.objects.all.return_value.first.return_value.name = 'Yum Yum Cookie!!'
            self.assertEqual('accepted', wagtail_cookie_consent_status(self.context))

    def test_wagtail_cookie_status_returns_string_declined_when_it_was_declined(self, mock_model):
            self.request.COOKIES['cookie_monster'] = 'declined'
            self.context['request'] = self.request
            mock_model.objects.all.return_value.first.return_value.name = 'Cookie Monster'
            self.assertEqual('declined', wagtail_cookie_consent_status(self.context))
