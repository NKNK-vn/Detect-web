import { DARK_COLOR } from './config';

/**
 * Init interface an types
 */
type webStates = 'safe' | 'unsafe' | 'critical' | 'processing';

// Init core for calling background and content script
const core = chrome;
declare const window: any;

/**
 * Get current web safe value
 */
export function getCurrentWebSafeValue(): Promise<webStates | false> {
	return new Promise((rs, rj) => {
		try {
			core.runtime.sendMessage(
				core.runtime.id,
				{
					from: 'popup',
					action: 'get_safe_value',
				},
				(res: webStates) => {
					rs(res);
				},
			);
		} catch (e) {
			rs(false);
		}
	});
}

/**
 * Get current web hide image value
 */
export function getCurrentWebHideValue(): Promise<boolean> {
	return new Promise((rs, rj) => {
		try {
			core.runtime.sendMessage(
				core.runtime.id,
				{
					from: 'popup',
					action: 'get_hide_value',
				},
				(res: boolean) => {
					rs(res);
				},
			);
		} catch (e) {
			rs(false);
		}
	});
}

/**
 * Get current web hide image value
 */
export function setWebHideValue(val: boolean): Promise<boolean> {
	return new Promise((rs, rj) => {
		try {
			core.runtime.sendMessage(
				core.runtime.id,
				{
					from: 'popup',
					action: 'set_hide_value',
					data: val,
				},
				(res: boolean) => {
					rs(res);
				},
			);
		} catch (e) {
			rs(false);
		}
	});
}

/**
 * Return url of current website
 */
export function getCurrentWebUrl(): Promise<string> {
	return new Promise((rs, rj) => {
		try {
			core.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
				rs(tabs[0].url);
			});
		} catch (e) {
			rs('');
		}
	});
}

export function setBackground(selector: string, color: string) {
	window.VANTA.NET({
		el: selector,
		mouseControls: true,
		touchControls: false,
		minHeight: 250.0,
		minWidth: 300.0,
		scale: 1,
		scaleMobile: 1,
		color: 0xffffff,
		backgroundColor: color,
		maxDistance: 13.0,
		points: 4.0,
		spacing: 20.0,
	});
}
