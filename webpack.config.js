const { CheckerPlugin } = require('awesome-typescript-loader');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { optimize } = require('webpack');
const { join } = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');
let prodPlugins = [];
if (process.env.NODE_ENV === 'production') {
    prodPlugins.push(new optimize.AggressiveMergingPlugin(), new optimize.OccurrenceOrderPlugin(), new CopyWebpackPlugin({
        patterns: [{ from: './manifest.json' }, { from: './src/assets' },
        {
            from: './src/popup/build', to: "./popup", globOptions: {
                ignore: ['**/static/**'],
            },
        },
        { from: './src/popup/build/static', to: "./static" }],
    }));
} else {
    prodPlugins.push(new CopyWebpackPlugin({
        patterns: [{ from: './manifest.json' }, { from: './src/assets' }],
    }));
}
module.exports = {
    mode: process.env.NODE_ENV,
    devtool: 'inline-source-map',
    entry: {
        contentscript: join(__dirname, 'src/contentscript/contentscript.ts'),
        contentstyle: join(__dirname, 'src/contentscript/contentscript.scss'),
        background: join(__dirname, 'src/background/background.ts'),
    },
    output: {
        path: join(__dirname, 'dist'),
        filename: '[name].js',
    },
    module: {
        rules: [
            {
                exclude: /node_modules/,
                test: /\.ts?$/,
                use: 'awesome-typescript-loader?{configFileName: "tsconfig.json"}',
            },
            {
                test: /\.s?css$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
            },
        ],
    },
    node: {
        fs: 'empty',
        net: 'empty',
        tls: 'empty',
    },
    plugins: [
        new CheckerPlugin(),
        ...prodPlugins,
        new MiniCssExtractPlugin({
            filename: '[name].css',
            chunkFilename: '[id].css',
        })
    ],
    resolve: {
        extensions: ['.ts', '.js', '.scss'],
    },
};
