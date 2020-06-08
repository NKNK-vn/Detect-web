import React, { useState, useEffect } from 'react';
import Switch from '@material-ui/core/Switch';
import './App.scss';
import { useTypedTranslation } from '../../languages/typedTranslation';
import { DARK_COLOR, PRIMARY_COLOR, ALLOW_ENABLED } from '../../config';
import {
	getCurrentWebSafeValue,
	getCurrentWebUrl,
	getCurrentWebHideValue,
	setWebHideValue,
	setDisabledValue,
} from '../../manager';
import CircularProgress from '@material-ui/core/CircularProgress';
function App() {
	const [hide, setHide] = useState(true);
	const { t } = useTypedTranslation();
	const [safeValue, setSafeValue] = useState(t('loadingSafe'));
	const [url, setUrl] = useState('<url>');
	const [disabled, setDisabled] = useState(true);
	const [bgColor, setBgColor] = useState('bg-blue');
	const getState = async () => {
		setHide(await getCurrentWebHideValue());
		setUrl(await getCurrentWebUrl());
		let safeValueAPI = await getCurrentWebSafeValue();
		if (safeValueAPI) {
			switch (safeValueAPI.state) {
				case 'critical':
					setSafeValue(t('dangerousWebsite'));
					setBgColor('bg-orange');
					break;
				case 'safe':
					setBgColor('bg-green');
					setSafeValue(t('safeWebsite'));
					break;
				case 'unsafe':
					setBgColor('bg-orange');
					setSafeValue(t('unSafeWebsite'));
					break;
				default:
					setSafeValue(t('loadingSafe'));
					setBgColor('bg-blue');
					setTimeout(() => {
						getState();
					}, 500);
					break;
			}
			switch (safeValueAPI.off) {
				case true:
					setDisabled(true);
					break;

				default:
					setDisabled(false);
					break;
			}
		}
	};
	useEffect(() => {
		getState();
	}, []);
	return (
		<div className="h-100 w-100 bg-white flex flex-column">
			<div
				id="status-container"
				className={`overflow-hidden w-100 h-75 ${bgColor} br4 br--bottom shadow-4 flex justify-center items-center flex-column relative`}>
				{ALLOW_ENABLED && (
					<div
						className={`absolute right-0 top-0 w-30 bg-white flex shadow-4 flex justify-center items-center z-1 grow ${
							!disabled ? 'bg-green' : 'bg-red'
						}`}
						onClick={async () => {
							setDisabled(!disabled);
							await setDisabledValue(!disabled);
						}}
						style={{ height: '25px', borderBottomLeftRadius: '8px' }}>
						<h4 className="ma0 fw1 white">{disabled ? t('disabled') : t('enabled')}</h4>
					</div>
				)}
				<div className="absolute flex justify-center items-center o-50">
					<CircularProgress
						size={156}
						color="secondary"
						disableShrink={bgColor !== 'bg-blue'}
						className={`animate__animated ${bgColor !== 'bg-blue' && 'animate__slower'}`}
					/>
				</div>
				<h2 className="white ma0 tc">{safeValue}</h2>
				<h3 className="white ma0 fw1 tc">{url.domain()}</h3>
			</div>
			<div className="w-100 h-25 pa2 flex items-center">
				<h4 className="ma0 w-100 fw1">{t('hideImage')}</h4>
				<Switch
					checked={hide}
					onChange={async () => {
						setHide(!hide);
						await setWebHideValue(!hide);
					}}
					color="primary"
					name="hideImage"
					inputProps={{ 'aria-label': 'primary checkbox' }}
				/>
			</div>
		</div>
	);
}

export default App;
