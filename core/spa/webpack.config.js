const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
	mode: 'development',
	resolve: {
		alias: {
			'vue': 'vue/dist/vue.esm.js',
		},
	},
	entry: {
		'home': './home_index.js',
		'detail': './detail_index.js',
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
					'css-loader',
				]
			}, {
				test: /\.(png|jpg|gif)$/i,
				use: [
					{
						loader: 'url-loader',
						options: {
							limit: 100000
						}
					}
				]
			}
		]
	},
	plugins: [
		new VueLoaderPlugin(),
	]
};

