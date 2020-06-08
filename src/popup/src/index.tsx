import React from 'react';
import ReactDOM from 'react-dom';
import 'tachyons';
import 'tachyons-animate';
import 'animate.css';
import 'react-toastify/dist/ReactToastify.css';
import './index.scss';
import './prototype.d.ts';
import * as serviceWorker from './serviceWorker';
import { I18nextProvider } from 'react-i18next';
import i18n from './languages/i18n';
import App from './pages/app/App';

ReactDOM.render(
	<React.StrictMode>
		<I18nextProvider i18n={i18n}>
			<App />
		</I18nextProvider>
	</React.StrictMode>,
	document.getElementById('root'),
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
