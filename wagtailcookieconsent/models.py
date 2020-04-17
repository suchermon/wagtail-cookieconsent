from django.utils.translation import ugettext_lazy as _
from django.db import models

from wagtail.core.fields import RichTextField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel, HelpPanel, MultiFieldPanel


@register_setting
class WagtailCookieConsent(BaseSetting):
    name = models.CharField(
        verbose_name=_('Cookie Name'),
        max_length=255,
        help_text=_('Give it a name to identify the cookie. The given name will be converted to underscore naming convention to set and retrieve cookies.')
    )
    banner_text = RichTextField(
        verbose_name=_('Banner Text'),
        help_text=_('The text that appears next to the Accept button. For example: `We use cookie to give you a better experience...`')
    )
    description = RichTextField(
        help_text=_('Enter a detailed description of what EXACTLY are we tracking using this cookie and used by whom (For example: Google analytics). This information will be shown via a `What we are tracking` link be listed at the bottom of the acceptance banner for the end-user if they choose to read more. ')
    )

    panels = [
        HelpPanel(
            heading='Wagtail Cookie Consent',
            content='This is a simple way to notify users that we use analytics. If the user does not click the accept button, no tracking scripts will be included on the templates. No GA, GTM, none.'
        ),
        FieldPanel('name'),
        MultiFieldPanel([
            FieldPanel('banner_text', classname='full'),
            FieldPanel('description', classname='full'),
        ], heading=_('Detail')),
    ]
