const path = require('path');
const webpack = require('webpack');

module.exports = {
    mode: 'development',
	entry: './app/static/js/index.js',
    output: {
        filename: 'main.js',
        path: path.resolve(__dirname, 'app/static/js'),
		publicPath: 'static/js'
    },
    plugins: [
        new webpack.ProvidePlugin({
           $: "jquery",
           jQuery: "jquery"
       })
    ],
    devServer: {
        proxy: {
            '/': 'http://localhost:5000'
        }
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env']
            }
          }
        }
      ]
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: ['style-loader', 'css-loader']
        }
      ]
    }
};
