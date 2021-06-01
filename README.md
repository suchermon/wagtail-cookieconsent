# Wagtail Cookie Consent 


A very simple Cookie Consent to prompt a visitor to either accept or decline tracking. Silly enough, the only way to know that they accepted or declined is to set a cookie. Once they have accepted or declined, you can use a template tag to include the tracking scripts.


## Requirements and dependencies

* Wagtail (2.11+)
* Django 3.0+

### Installation

`pip install -e 'git+https://github.com/suchermon/wagtail-cookieconsent.git@master#egg=wagtail-cookieconsent'`

OR `pipenv`

`pipenv install -e git+https://github.com/suchermon/wagtail-cookieconsent.git@master#egg=wagtail-cookieconsent`


## Install app to Django

1. Install the app

```
INSTALLED_APPS = [
  ...
  'wagtailcookieconsent',
  ...
]
```

2. Add `path('cookies/', include('wagtailcookieconsent.urls')),` to your urls

3. Run `python manage.py migrate`

4. Add the template tags in the homepage or `base.html` template so it'll be included the same stuff throughout the site. (see [`example/base.html`](https://github.com/suchermon/wagtail-cookieconsent/blob/master/wagtailcookieconsent/example/base.html))

    ```
    {% load wagtailsettings_tags wagtail_cookie_consent_tags %}

    {% get_settings %} // If wagtail settings were not loaded already

    {% wagtail_cookie_consent_status as cookie_consent %}
    {% if cookie_consent == 'accepted' %}
    ... # loads tracking JS codes
    {% endif %}

    # Somewhere below the main content
    {% wagtail_cookie_consent_banner %}
    ```

5. Include `{% static 'wagtailcookieconsent.min.css' %}` or write your own css. I have included SASS in `wagtailcookieconsent/assets/scss` if you prefer that.

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

### Tests

After installation in your local environment:

`python manage.py test wagtailcookieconsent --keepdb` (in your own test environment)

### Contribution

Fork and do whatever you want. I don't have a strong opinion just as long as you don't break it.

#### Changelog

* 5/24/21
    * Replaced `RedirectView` with `FormView` for full validations. Hackers are jerks.
* 12/8/20
    * Version bump and added required wagtail version in `install_requires`
* 9/14/20
    * Added a check for wagtail < 2.10 for `for_site()` because in 2.10+ `for_site()` only needs the `request` vs older version needs `request.site`
* 5/6/20
    * Added `expiration` field in settings to be able to configure when the cookie would expire as well as better `max_age` and `expires` calculations.
    * Fixed the epic bug that crashes the entire thing when there are no settings detected (DOH!)
* 5/31/20
    * Triple checking the cookie name and raise a form error (then into nothingness). The reason is there were multiple attempts that someone tried to XSS and the constant errors bombarded us with bunch of emails. 