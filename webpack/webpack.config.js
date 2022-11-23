const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const TerserWebpackPlugin = require('terser-webpack-plugin');

/* const OptimizeCssAssetsWebpackPlugin = require('optimize-css-assets-webpack-plugin'); для Webpack до 5 версии*/


module.exports = {
    devtool: 'inline-source-map',
    entry: './src/index.js',
    mode: 'development',
    devServer: {
        contentBase: './dist',
        hot: true,
        port: 3001,
        stats: {
            children: false
        },

    },
    output: {
        filename: "main.js"
    },
    plugins:[
        new MiniCssExtractPlugin(),
        new TerserWebpackPlugin(),
        new HtmlWebpackPlugin(),
/*        new HtmlWebpackPlugin({
            title: 'Development',
        }),*/
        /* new OptimizeCssAssetsWebpackPlugin(), */
    ],
    optimization: {
        minimize: true,
        minimizer: [ new TerserWebpackPlugin(), /* new OptimizeCssAssetsWebpackPlugin() */],
    },
    module: {
        rules: [
            {
                /*use: ['style-loader', 'css-loader'],*/
                use: [{
                    loader: MiniCssExtractPlugin.loader,
                    options: {
                        esModule: true,
                    }
                }, 'css-loader'],
                test: /\.css$/
            },
/*            {
                test: /\.ts$/,
                use: 'ts-loader'
            },
            {
                test: /\.js$/,
                exclude: '/node_modules/',
                use: 'eslint-loader'

            }*/
        ]
    }
};