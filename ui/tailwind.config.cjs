const typography = require('@tailwindcss/typography');
const daisyui = require('daisyui');
const forms = require('@tailwindcss/forms');

const config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {}
	},

	plugins: [forms, typography, daisyui]
};

module.exports = config;
