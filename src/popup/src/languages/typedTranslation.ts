import { useTranslation } from 'react-i18next';
import dict from './en';
type Dictionary = string | DictionaryObject;
type DictionaryObject = { [K: string]: Dictionary };

interface TypedTFunction<D extends Dictionary> {
	<K extends keyof D>(args: K): D[K];
	<K extends keyof D, K1 extends keyof D[K]>(...args: [K, K1]): D[K][K1];
	<K extends keyof D, K1 extends keyof D[K], K2 extends keyof D[K][K1]>(...args: [K, K1, K2]): D[K][K1][K2];
	// ... up to a reasonable key parameters length of your choice ...
}

type MyTranslations = {
	/* your concrete type*/
};
// e.g. via const dict = {...}; export type MyTranslations = typeof dict

// import this hook in other modules instead of i18next useTranslation
export function useTypedTranslation(): { t: TypedTFunction<typeof dict> } {
	const { t } = useTranslation();
	// implementation goes here: join keys by dot (depends on your config)
	// and delegate to lib t
	return {
		t(...keys: string[]) {
			return t(keys.join('.'));
		},
	};
}
