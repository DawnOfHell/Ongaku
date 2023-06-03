const typography = require('@tailwindcss/typography');
const daisyui = require('daisyui');
const forms = require('@tailwindcss/forms');

const config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {
			gridTemplateColumns: {
				'game': '1fr minmax(400px, 3fr) 1.5fr',
			}
		}
	},

	plugins: [forms, typography, daisyui]
};

module.exports = config;
