import React, { useState, useEffect } from 'react';
import Switch from '@material-ui/core/Switch';
import './App.scss';
import { useTypedTranslation } from '../../languages/typedTranslation';
import { DARK_COLOR, PRIMARY_COLOR } from '../../config';
import { setBackground, getCurrentWebSafeValue, getCurrentWebUrl, getCurrentWebHideValue, setWebHideValue } from '../../manager';
function App() {
	const [hide, setHide] = useState(true);
	const { t } = useTypedTranslation();
	const [safeValue, setSafeValue] = useState(t('loadingSafe'));
	const [url, setUrl] = useState('<url>');
	const getState = async () => {
		setHide(await getCurrentWebHideValue());
		setUrl(await getCurrentWebUrl());
	};
	useEffect(() => {
		getState();
	}, []);
	return (
		<div className="h-100 w-100 bg-white flex flex-column">
			<div
				id="status-container"
				className="overflow-hidden w-100 h-75 bg-blue br4 br--bottom shadow-4 flex justify-center items-center flex-column">
				<h1 className="white ma0">{safeValue}</h1>
				<h3 className="white ma0 fw1">{url}</h3>
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
