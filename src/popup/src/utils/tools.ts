import '../prototype.d';
import request from 'request';

export interface IError {
	/**
	 * Message of error type from server
	 */
	mess: string;
	/**
	 * Error code from server
	 */
	code: number;
}

export enum EError {
	SUCCESS = 0,
	AUTH = 1,
	DB_ERR = 2,
	PERM_ERR = 3,
	INPUT = 4,
}

/**
 * Secure data before send to client
 * @param s string data need to be secure
 */
export function enData(s: string) {
	return zip(s).enHex();
}

/**
 * Decode an string to data
 * @param s string need to be decoded to data
 */
export function deData(s: string) {
	return unzip(s.deHex());
}

// Apply LZW-compression to a string and return base64 compressed string.
export function zip(s: string) {
	try {
		let dict: any = {};
		let data = (s + '').split('');
		let out = [];
		let currChar;
		let phrase = data[0];
		let code = 256;
		for (let i = 1; i < data.length; i++) {
			currChar = data[i];
			if (dict[phrase + currChar] != null) {
				phrase += currChar;
			} else {
				out.push(phrase.length > 1 ? dict[phrase] : phrase.charCodeAt(0));
				dict[phrase + currChar] = code;
				code++;
				phrase = currChar;
			}
		}
		out.push(phrase.length > 1 ? dict[phrase] : phrase.charCodeAt(0));
		for (let j = 0; j < out.length; j++) {
			out[j] = String.fromCharCode(out[j]);
		}
		return out.join('');
	} catch (e) {
		return '';
	}
}

// Decompress an LZW-encoded base64 string
export function unzip(base64ZippedString: string) {
	try {
		let s = base64ZippedString;
		let dict: any = {};
		let data = (s + '').split('');
		let currChar = data[0];
		let oldPhrase = currChar;
		let out = [currChar];
		let code = 256;
		let phrase;
		for (let i = 1; i < data.length; i++) {
			let currCode = data[i].charCodeAt(0);
			if (currCode < 256) {
				phrase = data[i];
			} else {
				phrase = dict[currCode] ? dict[currCode] : oldPhrase + currChar;
			}
			out.push(phrase);
			currChar = phrase.charAt(0);
			dict[code] = oldPhrase + currChar;
			code++;
			oldPhrase = phrase;
		}
		return out.join('');
	} catch (e) {
		return '';
	}
}
export function delay(ms: number) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

interface IApiConfig {
	method?: 'POST' | 'GET';
	headers?: { [key: string]: string };
	data?: { [key: string]: string | number };
}
export function callAPI(url: string, opts?: IApiConfig) {
	return new Promise((rs, rj) => {
		if (opts?.method === 'GET') {
			let arrayData = [];
			for (let key of Object.keys(opts?.data || {})) {
				arrayData.push(`${key}=${opts?.data?.[key]}`);
			}
			if (arrayData.length > 0) {
				url += `?${arrayData.join('&')}`;
			}
		}
		request(
			url,
			{
				method: opts?.method || 'GET',
				headers: { ...opts?.headers, Accept: 'application/json' },
				json: true,
				body: opts?.data,
			},
			function (error: any, response: any, body: any) {
				if (error) {
					return rj(error);
				} else {
					return rs(body);
				}
			},
		);
	});
}
