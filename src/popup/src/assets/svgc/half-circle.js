import React from 'react';
export const halfCircle = ({ viewBox = '0 0 110 110', fill = 'white', width = '110', height = '220' }) => (
	<svg width={width} height={height} viewBox={viewBox} fill="none" xmlns="http://www.w3.org/2000/svg">
		<path
			d="M110 0C49.2487 0 6.10352e-05 49.2487 6.10352e-05 110C6.10352e-05 170.751 49.2487 220 110 220V200C60.2944 200 20.0001 159.706 20.0001 110C20.0001 60.2944 60.2944 20.0001 110 20V0Z"
			fill={fill}
		/>
	</svg>
);
