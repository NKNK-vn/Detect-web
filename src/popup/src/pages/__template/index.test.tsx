import React from 'react';
import { render } from '@testing-library/react';
import __Template from '.';

test('renders learn react link', () => {
	const { getByText } = render(<__Template />);
	const linkElement = getByText(/learn react/i);
	expect(linkElement).toBeInTheDocument();
});
