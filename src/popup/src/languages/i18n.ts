import i18n from 'i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import translationVi from './vi';
i18n.use(LanguageDetector).init({
	debug: true,
	lng: 'vi',
	fallbackLng: 'vi', // use en if detected lng is not available
	keySeparator: false, // we do not use keys in form messages.welcome
	interpolation: {
		escapeValue: false, // react already safes from xss
	},
	resources: {
		vi: {
			translations: translationVi,
		},
	},
	// have a common namespace used around the full app
	ns: ['translations'],
	defaultNS: 'translations',
});

export default i18n;
