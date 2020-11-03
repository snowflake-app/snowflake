const path = require('path');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const Manifest = require('webpack-manifest-plugin');

module.exports = {
    'entry': {
        'app': './_frontend/index.js'
    },
    'output': {
        'filename': '[name]-[chunkhash].js',
        'path': path.resolve(__dirname, 'snowflake/static/assets'),
    },
    'module': {
        'rules': [
            {
                'test': /\.js$/,
                'use': [
                    'babel-loader',
                    'source-map-loader'
                ]
            },
            {
                test: /\.s?[ac]ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader',
                    'source-map-loader'
                ],
            },
        ]
    },
    plugins: [
        new CleanWebpackPlugin(),
        new Manifest({writeToFileEmit: true}),
        new MiniCssExtractPlugin({
            filename: '[name]-[chunkhash].css'
        })
    ],
    devServer: {
        contentBase: path.resolve(__dirname, 'snowflake/static/assets'),
    },
};
