import { themeTokens } from 'kolibri-design-system/lib/styles/theme';
import pluginData from 'kolibri-plugin-data';
import themeConfig from 'kolibri/styles/themeConfig';
import { validateObject } from 'kolibri/utils/objectSpecs';
import initializeTheme from '../initializeTheme';
import themeSpec from '../themeSpec';

jest.mock('kolibri-plugin-data', () => ({ __esModule: true, default: {} }));

// Verbatim from DefaultThemeHook.theme in kolibri/plugins/default_theme/kolibri_plugin.py.
function defaultThemeHookTheme() {
  return {
    siteTitle: 'DARE Learning',
    brandColors: {
      primary: {
        v_100: '#ede7f6',
        v_200: '#d1c4e9',
        v_300: '#b39ddb',
        v_400: '#7e57c2',
        v_500: '#5e35b1',
        v_600: '#4527a0',
      },
      secondary: {
        v_100: '#fff8e1',
        v_200: '#ffecb3',
        v_300: '#ffe082',
        v_400: '#ffc107',
        v_500: '#ffb300',
        v_600: '#ff8f00',
      },
    },
    signIn: {
      background: '/static/assets/default_theme/background.jpg',
      backgroundImgCredit: 'Lewa Wildlife Conservancy',
      title: 'DARE Learning',
      topLogo: {
        src: '/static/assets/dare_learning/dare-learning.svg',
        alt: 'DARE Learning',
        style: 'margin-bottom: 5px; width: 50px; height: 50px;',
      },
      titleStyle: { fontWeight: '600', fontSize: '20px' },
    },
    sideNav: {
      title: 'DARE Learning',
      brandedFooter: {
        logo: {
          src: '/static/assets/dare_learning/dare-learning.svg',
          alt: 'DARE Learning',
        },
        paragraphArray: ['African knowledge. African learning.'],
      },
    },
    logos: [
      {
        src: '/static/assets/dare_learning/dare-learning.svg',
        content_type: 'image/svg+xml',
        alt: 'DARE Learning',
        maskable: false,
        size: 'any',
      },
    ],
  };
}

// ThemeHook.get_theme() backfills the top-level sections before this ships as kolibriTheme.
function initializedThemeHookTheme() {
  return {
    ...defaultThemeHookTheme(),
    tokenMapping: {},
    appBar: {},
  };
}

describe('initializeTheme', () => {
  it('populates every section from spec defaults when the server sends no theme', () => {
    pluginData.kolibriTheme = undefined;

    initializeTheme();

    expect(themeConfig.signIn.showTitle).toBe(true);
    expect(themeConfig.signIn.scrimOpacity).toBe(0.2);
    expect(themeConfig.signIn.titleStyle).toBe(null);
    expect(themeConfig.sideNav.showKolibriFooterLogo).toBe(true);
    expect(themeConfig.appBar.background).toBe(themeTokens().appBar);
  });

  it('keeps the bundled default theme intact, defaulting the fields it omits', () => {
    const theme = defaultThemeHookTheme();
    pluginData.kolibriTheme = initializedThemeHookTheme();

    initializeTheme();

    expect(themeConfig.signIn.background).toBe(theme.signIn.background);
    expect(themeConfig.signIn.backgroundImgCredit).toBe(theme.signIn.backgroundImgCredit);
    expect(themeConfig.signIn.topLogo.style).toBe(theme.signIn.topLogo.style);
    expect(themeConfig.signIn.titleStyle).toEqual(theme.signIn.titleStyle);
    expect(themeConfig.signIn.showTitle).toBe(true);
    expect(themeConfig.signIn.scrimOpacity).toBe(0.2);
    expect(themeConfig.signIn.title).toBe('DARE Learning');
    expect(themeConfig.sideNav.title).toBe('DARE Learning');
    expect(themeConfig.sideNav.brandedFooter.paragraphArray).toEqual([
      'African knowledge. African learning.',
    ]);
  });

  it('populates sections the theme hook omits entirely', () => {
    const theme = defaultThemeHookTheme();
    delete theme.sideNav;
    pluginData.kolibriTheme = theme;

    initializeTheme();

    expect(themeConfig.sideNav.showKolibriFooterLogo).toBe(true);
    expect(themeConfig.appBar.textColor).toBe(themeTokens().text);
  });
});

describe('themeSpec', () => {
  // Nothing else catches signIn.titleStyle specced as a String: objectWithDefaults
  // does not type-check, and validateObject's complaint only reaches a silenced logger.
  it('validates the bundled default theme', () => {
    expect(validateObject(initializedThemeHookTheme(), themeSpec)).toBe(true);
  });
});
