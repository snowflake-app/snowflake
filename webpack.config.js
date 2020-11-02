const path = require('path');
const {CleanWebpackPlugin} = require("clean-webpack-plugin");

const Manifest = require('webpack-manifest-plugin');

const isDev = process.env.NODE_ENV !== 'production';

module.exports = {
    "entry": {
        "main": "./_frontend/index.js"
    },
    "output": {
        "filename": "[name]-[chunkhash].js",
        "path": path.resolve(__dirname, "static/assets"),
    },
    "module": {
        "rules": [
            {
                "test": /\.jsx?$/,
                "use": "babel-loader",
            },
            {
                "test": /\.js$/,
                "use": "source-map-loader",
            },
            {
                "test": /\.css$/,
                "use": [
                    "style-loader",
                    "css-loader"
                ]
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    'style-loader',
                    'css-loader',
                    'sass-loader'
                ],
            },
        ]
    },
    plugins: [
        new CleanWebpackPlugin(),
        new Manifest({writeToFileEmit: true})
    ],
    devServer: {
        contentBase: path.resolve(__dirname, "static/assets"),
    },
};
