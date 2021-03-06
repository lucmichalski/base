const path = require('path');
const autoprefixer = require('autoprefixer');
const merge = require('webpack-merge');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const TARGET = (process.env.npm_lifecycle_event.split(':'))[0];

const basePath = path.resolve(__dirname, '../client/src/frontend/');

const PATHS = {
    app: path.join(__dirname, '../client/src/frontend'),
    build: path.join(__dirname, '../client/dist/frontend')
};

const VENDOR = [
    'babel-polyfill',
    'history',
    'react',
    'react-dom',
    'react-redux',
    'react-router',
    'react-mixin',
    'classnames',
    'redux',
    'react-router-redux',
    'jquery',
    'bootstrap-loader',
    'font-awesome-webpack!./styles/font-awesome.config.prod.js'
];


const config = {
    context: basePath,
    entry: {
        vendor: VENDOR,
        app: PATHS.app
    },
    output: {
        filename: '[name].[hash].js',
        path: PATHS.build,
        publicPath: '/assets/frontend',
    },
    plugins: [
        // extract all common modules to vendor so we can load multiple apps in one page
        // new webpack.optimize.CommonsChunkPlugin({
        //     name: 'vendor',
        //     filename: 'vendor.[hash].js'
        // }),
        new webpack.optimize.CommonsChunkPlugin({
            children: true,
            async: true,
            minChunks: 2
        }),
        new HtmlWebpackPlugin({
            template: path.join(PATHS.app, 'index.html'),
            hash: true,
            chunks: ['vendor', 'app'],
            chunksSortMode: 'auto',
            filename: 'index.html',
            inject: 'body'
        }),
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: TARGET === 'dev' ? '"development"' : '"production"'
            },
            '__DEVELOPMENT__': TARGET === 'dev'
        }),
        new webpack.ProvidePlugin({
            '$': 'jquery',
            'jQuery': 'jquery',
            'window.jQuery': 'jquery'
        }),
        new CleanWebpackPlugin([PATHS.build], {
            root: process.cwd()
        })
    ],
    resolve: {
        extensions: ['.jsx', '.js', '.json', '.scss', '.css'],
        modules: ['node_modules']
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                use: {
                    loader: 'babel-loader'
                },
                exclude: /node_modules/
            },
            {
                test: /\.jpe?g$|\.gif$|\.png$/,
                loader: 'file-loader?name=/images/[name].[ext]?[hash]'
            },
            {
                test: /\.woff(\?.*)?$/,
                loader: 'url-loader?name=/fonts/[name].[ext]&limit=10000&mimetype=application/font-woff'
            },
            {
                test: /\.woff2(\?.*)?$/,
                loader: 'url-loader?name=/fonts/[name].[ext]&limit=10000&mimetype=application/font-woff2'
            },
            {
                test: /\.ttf(\?.*)?$/,
                loader: 'url-loader?name=/fonts/[name].[ext]&limit=10000&mimetype=application/octet-stream'
            },
            {
                test: /\.eot(\?.*)?$/,
                loader: 'file-loader?name=/fonts/[name].[ext]'
            },
            {
                test: /\.otf(\?.*)?$/,
                loader: 'file-loader?name=/fonts/[name].[ext]&mimetype=application/font-otf'
            },
            {
                test: /\.svg(\?.*)?$/,
                loader: 'url-loader?name=/fonts/[name].[ext]&limit=10000&mimetype=image/svg+xml'
            },
            {
                test: /\.json(\?.*)?$/,
                loader: 'file-loader?name=/files/[name].[ext]'
            },
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract([
                    {
                        loader: 'css-loader',
                        options: {
                            importLoaders: 1
                        },
                },
                'postcss-loader'])
            }, {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract([
                    {
                        loader: 'css-loader',
                        options: {
                            importLoaders: 1
                        },
                },
                'postcss-loader',
                    {
                        loader: 'sass-loader',
                        options: {
                            data: `@import "${PATHS.app}/styles/config/_variables.scss";`
                        }
                }])
        }
        ]
    }
};

switch (TARGET) {
    case 'dev':
        module.exports = merge(require('./common/dev.config'), config);
        break;
    case 'prod':
        module.exports = merge(require('./common/prod.config'), config);
        break;
    default:
        console.log('Target configuration not found. Valid targets: "dev" or "prod".');
}
