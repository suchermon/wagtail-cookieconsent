# Wagtail Cookie Consent 


A very simple Cookie Consent to prompt a visitor to either accept or decline tracking. Silly enough, the only way to know that they accepted or declined is to set a cookie. Once they have accepted the declined, the template will now include the tracking scripts.


## Requirements and dependencies

* Wagtail (2.8+)
* Django 3.0+

### Install / Uninstall

`pip install 'git+https://github.com/suchermon/wagtail-cookieconsent.git@master#egg=wagtail-cookieconsent'`

OR `pipenv`

`pipenv install git+https://github.com/suchermon/wagtail-cookieconsent.git@master#egg=wagtail-cookieconsent`


Uninstall: `pip uninstall wagtail-cookieconsent` or `pipenv uninstall wagtail-cookieconsent`

## Installation

1. Install the app

```
INSTALLED_APPS = [
  ...
  'wagtailcookieconsent',
  ...
]
```

2. Add `re_path(r'^cookies/', include('wagtailcookieconsent.urls')),` to your `urls.py`

3. Run `python manage.py migrate`

4. Add the template tags in the homepage or `base.html` template so it'll be included the same stuff throughout the site. (see [`example/base.html`](https://github.com/suchermon/wagtail-cookieconsent/blob/master/wagtailcookieconsent/example/base.html))

    ```
    {% load cookie_consent_tags %}
    
    {% if wagtail_cookie_consent_status == 'accepted' %}
    ... # loads tracking JS codes
    {% endif %}

    # Somewhere below the main content
    {% wagtail_cookie_consent_banner %}
    ```

5. Include `{% static 'cookieconsent.min.css' %}` or write your own css. I have included SASS in `wagtailcookieconsent/assets/scss` if you prefer that.

6. Load some initial data `python manage.py loaddata wagtailcookieconsent` or go to your `wagtail admin > Settings > Cookie Consent `to configure your cookie name, text and description

7. Run it `python manage.py runserver` and see it in actions.

**TIPS**

1. Install [Remove Cookie For Site](https://chrome.google.com/webstore/detail/removecookiesforsite/lmfdblomdpkcniknaenceeogpgepocmm?hl=en) Chrome Extension to quickly test whether it's working or not.

2. For Chrome: you can view the set cookies in `Dev Tools -> Application -> (Left Panel) Storage -> Cookies`

### Template Tags

`{% wagtail_cookie_consent_banner %}`

Will insert `wagtailcookieconsent/consent_banner.html`. Of course, you can override this template anyway you like just as long as you keep the forms.

`{% wagtail_cookie_consent_status %}`

This tag will returns `accepted | declined | None` so you can conditionally include tracking scripts where it needed.

### Contribution

Fork and do whatever you want. I don't have a strong opinion just as long as you don't break it.
