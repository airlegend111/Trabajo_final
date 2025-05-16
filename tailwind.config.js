module.exports = {
    content: [
        './pizzeria/templates/**/*.html',
        './pizzeria/static/js/**/*.js',
        './node_modules/flowbite/**/*.js',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('flowbite/plugin'),
    ],
};