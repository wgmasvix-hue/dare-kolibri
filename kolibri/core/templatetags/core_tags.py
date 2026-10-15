"""
Kolibri template tags
=====================
"""

from django import template
from django.templatetags.static import static
from django.utils.html import format_html

from kolibri.core.hooks import FrontEndBaseHeadHook
from kolibri.core.hooks import FrontEndBaseSyncHook
from kolibri.core.theme_hook import ThemeHook
from kolibri.utils.translation import gettext as _

register = template.Library()


@register.simple_tag()
def frontend_base_assets():
    """
    This is a script tag for all ``FrontEndBaseSyncHook`` hooks - this is used in the
    ``/base.html`` template to populate any Javascript and CSS that should be
    loaded at page load.

    :return: HTML of script tags to insert into base.html
    """
    return FrontEndBaseSyncHook.html()


@register.simple_tag()
def frontend_base_head_markup():
    """
    This is a script tag for all ``FrontEndBaseHeadHook`` hooks that define a
    ``head_html`` property - this is used in the ``/base.html`` template to
    inject arbitrary markup into the ``<head>`` element.

    :return: HTML to insert into head of base.html
    """
    return FrontEndBaseHeadHook.html()


@register.simple_tag()
def theme_favicon():
    """
    Render a favicon link to put in the <head> tag of base.html, if a favicon is
    provided by the theme. If not, a default will be returned.
    """
    logos = ThemeHook.get_theme().get("logos", [])
    favicon_urls = [
        logo["src"]
        for logo in logos
        if logo.get("content_type", "") == "image/vnd.microsoft.icon"
    ]

    # Prefer a raster favicon when available, then fall back to a theme SVG.
    favicon_url = (
        favicon_urls[0]
        if favicon_urls
        else next(
            (
                logo["src"]
                for logo in logos
                if logo.get("content_type", "") == "image/svg+xml"
            ),
            static("assets/favicons/logo.ico"),
        )
    )

    return format_html('<link rel="shortcut icon" href="{}">', favicon_url)


@register.simple_tag()
def site_title():
    """
    Return the text of the site title, if provided by the theme. If not, the
    default will be returned. The site title may be translated, to allow for
    transliteration into other alphabets where needed.
    """
    return ThemeHook.get_theme().get("siteTitle", _("Kolibri"))
