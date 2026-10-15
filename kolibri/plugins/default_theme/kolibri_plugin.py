from django.templatetags.static import static

from kolibri.core import theme_hook
from kolibri.plugins import KolibriPluginBase
from kolibri.plugins.hooks import register_hook
from kolibri.utils.translation import gettext as _


class DefaultThemePlugin(KolibriPluginBase):
    pass


@register_hook(as_default=True)
class DefaultThemeHook(theme_hook.ThemeHook):
    @property
    def theme(self):
        return {
            "siteTitle": "DARE Learning",
            "brandColors": {
                "primary": {
                    "v_100": "#ede7f6",
                    "v_200": "#d1c4e9",
                    "v_300": "#b39ddb",
                    "v_400": "#7e57c2",
                    "v_500": "#5e35b1",
                    "v_600": "#4527a0",
                },
                "secondary": {
                    "v_100": "#fff8e1",
                    "v_200": "#ffecb3",
                    "v_300": "#ffe082",
                    "v_400": "#ffc107",
                    "v_500": "#ffb300",
                    "v_600": "#ff8f00",
                },
            },
            "signIn": {
                "background": static("assets/default_theme/background.jpg"),
                "backgroundImgCredit": "Lewa Wildlife Conservancy",
                "title": "DARE Learning",
                "topLogo": {
                    "src": static("assets/dare_learning/dare-learning.svg"),
                    "alt": "DARE Learning",
                    "style": "margin-bottom: 5px; width: 50px; height: 50px;",
                },
                "titleStyle": {"fontWeight": "600", "fontSize": "20px"},
            },
            "sideNav": {
                "title": "DARE Learning",
                "brandedFooter": {
                    "logo": {
                        "src": static("assets/dare_learning/dare-learning.svg"),
                        "alt": "DARE Learning",
                    },
                    "paragraphArray": [_("African knowledge. African learning.")],
                },
            },
            "logos": [
                {
                    "src": static("assets/dare_learning/dare-learning.svg"),
                    "content_type": "image/svg+xml",
                    "alt": "DARE Learning",
                    "maskable": False,
                    "size": "any",
                },
            ],
        }
