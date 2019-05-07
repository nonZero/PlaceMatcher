const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
	mode: 'development',
	entry: {
		'home': './Home.vue',
		'detail': './Detail.vue',
	},
	output: {
		filename: '[name].js',
		path: path.resolve(__dirname, '../static/js')
	},
	module: {
		rules: [
			{
				test: /\.vue$/,
				loader: 'vue-loader'
			},
			// this will apply to both plain `.js` files
			// AND `<script>` blocks in `.vue` files
			{
				test: /\.js$/,
				loader: 'babel-loader'
			},
			// this will apply to both plain `.css` files
			// AND `<style>` blocks in `.vue` files
			{
				test: /\.css$/,
				use: [
					'vue-style-loader',
					'css-loader'
				]
			}
		]
	},
	plugins: [
		new VueLoaderPlugin(),
	]
};
