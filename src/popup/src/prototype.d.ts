/* eslint-disable */
interface String {
	/**
	 * Keep only alphabet and number on string
	 */
	normal(): string;
	/**
	 * Keep only alphabet char on string
	 */
	toOnlyWord(): string;
	/**
	 * Keep only alphabet and number on string
	 */
	toOnlyWordAndNumber(): string;
	/**
	 * Keep only digit on string
	 */
	toOnlyDigit(): string;
	/**
	 * Keep only special char on string
	 */
	toOnlySpecialChar(): string;
	/**
	 * Upper first case on string
	 */
	toFirstUpper(): string;
	/**
	 * Format string into human name, upper every first case of word
	 */
	toHumanName(): string;
	/**
	 * Check if string contain special char
	 */
	isContainSpecialChar(): boolean;
	/**
	 * Check if string is an email
	 */
	isEmail(): boolean;
	/**
	 * String to hex
	 */
	enHex(): string;
	/**
	 * Hex to string
	 */
	deHex(): string;
	/**
	 * Get domain from an URL string
	 */
	domain(): string;
}
interface Number {
	/**
	 * Check if number is between two value
	 * @param min Min of value
	 * @param max Max of value
	 */
	inRange(min: number, max: number): boolean;
}

interface Array<T> {
	/**
	 * Merge two array into one and remove duplicated
	 * @param arr2 The other array of same type
	 */
	merge(arr2: []): any[];
	/**
	 * Check if two array is the same
	 * @param arr2 The other array
	 */
	isEqual(arr2: []): boolean;
}

/**
 * String encoded to hex
 */
String.prototype.enHex = function () {
	let hex = '';
	try {
		hex = unescape(encodeURIComponent(this.toString()))
			.split('')
			.map(function (v) {
				return v.charCodeAt(0).toString(16);
			})
			.join('');
	} catch (e) {
		console.log('invalid text input: ' + this.toString());
	}
	return hex;
};

/**
 * Hex decoded to string
 */
String.prototype.deHex = function () {
	let str = this.toString();
	try {
		str = decodeURIComponent(this.toString().replace(/(..)/g, '%$1'));
	} catch (e) {
		console.log('invalid hex input: ' + this.toString());
	}
	return str;
};

/**
 * Normal char to unicode
 */
String.prototype.normal = function (): string {
	return this.toString()
		.normalize('NFD')
		.replace(/[\u0300-\u036f]/g, '')
		.replace(/đ/g, 'd')
		.replace(/Đ/g, 'D');
};

/**
 * Convert string to lower case and keep only A-Z a-z character
 */
String.prototype.toOnlyWord = function () {
	let temp: string = this.toString().toLowerCase().normal();
	return temp.replace(/[^A-Za-z ]+/g, ' ');
};

/**
 * Convert string to lower case and keep only A-Z a-z 0-9 character
 */
String.prototype.toOnlyWordAndNumber = function () {
	let temp: string = this.toString().toLowerCase().normal();
	return temp.replace(/[^A-Za-z0-9 ]+/g, ' ');
};

/**
 * Convert string to only 0-9 character
 */
String.prototype.toOnlyDigit = function () {
	return this.toString().replace(/\D/g, '');
};

/**
 * Convert string to only special character string
 */
String.prototype.toOnlySpecialChar = function () {
	return this.toString().replace(/[A-Za-z0-9 ]+/g, '');
};

/**
 * Convert string to upper first case
 */
String.prototype.toFirstUpper = function () {
	if (!this.toString()[0]) {
		return this.toString();
	}
	let temp = this.toString().toLowerCase();
	return temp[0].toUpperCase() + temp.slice(1);
};

/**
 * Upper first case of each word -> Human name
 */
String.prototype.toHumanName = function (): string {
	let temp: string[] = this.toString().toLowerCase().split(' ');
	let result = temp[0].toFirstUpper();
	temp.slice(1).forEach((word) => {
		result += ' ' + word.toFirstUpper();
	});
	return result;
};

/**
 * Check if string is only contain letters
 */
String.prototype.isContainSpecialChar = function () {
	return !/^[a-zA-Z ]+$/.test(this.toString());
};

/**
 * Check if string is only contain letters
 */
String.prototype.isEmail = function () {
	const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	return re.test(String(this).toLowerCase());
};

/**
 * Check if number in in range min - max
 */
Number.prototype.inRange = function (min: number, max: number): boolean {
	return (this.valueOf() - min) * (this.valueOf() - max) <= 0;
};

/**
 * Merge two array and remove it duplicate items
 */
Array.prototype.merge = function (arr2: []): any[] {
	return Array.from(new Set(this.concat(arr2)));
};

/**
 * Check if two array is equal, and it items like each other
 */
Array.prototype.isEqual = function (arr2: []): boolean {
	return JSON.stringify(this) === JSON.stringify(arr2);
};

String.prototype.domain = function () {
	return this.split('/').slice(0, 3).join('/');
};
