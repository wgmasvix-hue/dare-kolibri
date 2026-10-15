from unittest.mock import patch

from django.test import SimpleTestCase

from kolibri.core.templatetags.core_tags import theme_favicon


class ThemeFaviconTestCase(SimpleTestCase):
    def test_prefers_ico_favicon_when_available(self):
        with patch(
            "kolibri.core.templatetags.core_tags.ThemeHook.get_theme",
            return_value={
                "logos": [
                    {
                        "src": "/static/theme.svg",
                        "content_type": "image/svg+xml",
                    },
                    {
                        "src": "/static/theme.ico",
                        "content_type": "image/vnd.microsoft.icon",
                    },
                ],
            },
        ):
            self.assertEqual(
                str(theme_favicon()),
                '<link rel="shortcut icon" href="/static/theme.ico">',
            )

    def test_uses_theme_svg_when_ico_is_unavailable(self):
        with patch(
            "kolibri.core.templatetags.core_tags.ThemeHook.get_theme",
            return_value={
                "logos": [
                    {
                        "src": "/static/theme.svg",
                        "content_type": "image/svg+xml",
                    },
                ],
            },
        ):
            self.assertEqual(
                str(theme_favicon()),
                '<link rel="shortcut icon" href="/static/theme.svg">',
            )

    def test_uses_default_favicon_when_theme_has_no_icon(self):
        with patch(
            "kolibri.core.templatetags.core_tags.ThemeHook.get_theme",
            return_value={"logos": []},
        ):
            self.assertEqual(
                str(theme_favicon()),
                '<link rel="shortcut icon" href="/static/assets/favicons/logo.ico">',
            )
