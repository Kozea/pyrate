import childProcess from 'child_process'
import path from 'path'

import MinifyPlugin from 'babel-minify-webpack-plugin'
import chalk from 'chalk'
import ExtractTextPlugin from 'extract-text-webpack-plugin'
import HtmlWebpackHarddiskPlugin from 'html-webpack-harddisk-plugin'
import HtmlWebpackPlugin from 'html-webpack-plugin'
import ScriptExtHtmlWebpackPlugin from 'script-ext-html-webpack-plugin'
import webpack from 'webpack'
import { BundleAnalyzerPlugin } from 'webpack-bundle-analyzer'
import ManifestPlugin from 'webpack-manifest-plugin'
import nodeExternals from 'webpack-node-externals'

import {
  apiUrl,
  assetsUrl,
  cwd,
  debug,
  dirs,
  forcePolyfill,
  publicPath,
  server,
  serverUrl,
  staging,
  verbose,
} from './lib/frontend/src/config'

const main = server ? 'server' : 'client'

const entry = {}
entry[main] = []

// HMR
if (debug && !server) {
  entry[main].push(`webpack-dev-server/client?${assetsUrl.href}`)
}
if ((!debug || forcePolyfill) && !server) {
  entry[main].push('regenerator-runtime/runtime.js')
}
// Main entry point
entry[main].push(path.resolve(dirs.src, main))

// Loading rules
const rules = [
  {
    test: /\.jsx?$/,
    include: dirs.src,
    use: {
      loader: 'babel-loader',
      options: {
        babelrc: false,
        presets: [
          'react',
          [
            'env',
            {
              targets: server
                ? { node: true }
                : {
                    browsers:
                      debug && !forcePolyfill
                        ? ['last 1 Chrome version']
                        : ['> 3% in FR', 'last 2 versions', 'not ie <= 10'],
                  },
              modules: false,
              debug: verbose,
            },
          ],
        ],
        plugins: ['syntax-dynamic-import', 'transform-object-rest-spread'],
      },
    },
  },
  {
    test: /\.(jpe?g|png|gif|svg|ttf|woff|woff2|eot|pdf)$/i,
    use: {
      loader: 'url-loader',
      options: {
        limit: 2500,
      },
    },
  },
]

if (server) {
  // Ignoring styles on server
  rules.push({ test: /\.(css|sass)$/, use: 'ignore-loader' })
} else {
  // Sass -> Css
  const styleLoader = { loader: 'style-loader' }
  const cssLoader = {
    loader: 'css-loader',
    options: { sourceMap: debug },
  }
  const sassToCssLoaders = [
    cssLoader,
    {
      loader: 'resolve-url-loader',
    },
    {
      loader: 'sass-loader',
      options: {
        sourceMap: true,
        includePaths: [dirs.src, dirs.styles],
      },
    },
  ]
  // Extract it in css files
  rules.push({
    test: /\.sass$/i,
    use: ExtractTextPlugin.extract({
      fallback: 'style-loader',
      use: sassToCssLoaders,
    }),
  })
  // Css for deps
  rules.push({
    test: /\.css$/i,
    use: [styleLoader, cssLoader],
  })
}
// Plugins
const plugins = [
  // Common all
  new ManifestPlugin(),
  // DON'T use JSON stringify and yes it needs multiple quotes
  // (JSON is imported by babel in a file that use module.exports => X[)
  new webpack.DefinePlugin({
    'process.env.NODE_ENV': `"${process.env.NODE_ENV || 'development'}"`,
    'process.env.STAGING': `${staging}`,
  }),
]
if (debug) {
  // Common debug
  plugins.push(
    new webpack.NamedModulesPlugin(),
    new webpack.NoEmitOnErrorsPlugin()
  )
} else {
  plugins.push(new webpack.HashedModuleIdsPlugin())
}
if (!server) {
  // Common client
  plugins.push(
    new HtmlWebpackPlugin({
      alwaysWriteToDisk: true,
      cache: !debug,
      template: `${dirs.src}/index.ejs`,
    }),
    // Puts every deps in a vendor bundle
    // new webpack.optimize.CommonsChunkPlugin({
    //   name: 'vendor',
    //   chunks: ['client', 'Admin'],
    //   minChunks: ({ resource }) => /node_modules/.test(resource)
    // }),
    // Or put only shared deps
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor',
      minChunks: module =>
        module.context && module.context.includes('node_modules'),
    }),
    // manifest contains build changes to keep vendor hash stable (caching)
    new webpack.optimize.CommonsChunkPlugin({
      name: 'manifest',
      minChunks: Infinity,
    }),
    // Inline manifest (~1kb) and defer scripts
    new ScriptExtHtmlWebpackPlugin({
      inline: /manifest.*\.js$/,
      defaultAttribute: 'defer',
      // Remove prefetch for now as it slows the load
      // (and there's too many async)
      // prefetch: {
      //   test: /\.js$/,
      //   chunks: 'async'
      // }
    }),
    new HtmlWebpackHarddiskPlugin(),
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false,
      logLevel: 'error',
    })
  )
}

if (debug && !server) {
  // Client _debug
  plugins.push(new webpack.HotModuleReplacementPlugin())
}

if (debug && server) {
  // Server debug
  // Start and restart server
  class ServerDevPlugin {
    apply(compiler) {
      compiler.plugin('done', () => {
        if (this.server) {
          // eslint-disable-next-line
          console.log(` ${chalk.cyan('↻')} Restarting node server`)
          this.server.kill()
        } else {
          // eslint-disable-next-line
          console.log(` ${chalk.green('⏻')} Starting node server`)
        }

        this.server = childProcess.fork(path.resolve(dirs.dist, 'server.js'), {
          cwd,
          silent: false,
          execArgv: ['--inspect'],
        })
      })
    }
  }
  plugins.push(new ServerDevPlugin())
}

if (!debug && !server) {
  // Client prod
  plugins.push(
    new ExtractTextPlugin({
      filename: '[name].[chunkhash].css',
      allChunks: true,
    }),
    new webpack.optimize.ModuleConcatenationPlugin(),
    new MinifyPlugin()
  )
}
const stats = verbose ? 'verbose' : 'errors-only'
const conf = {
  devtool: debug ? 'cheap-module-source-map' : 'source-map',
  entry,
  // Defines the output file for the html script tag
  output: {
    path: server ? dirs.dist : dirs.assets,
    filename: debug || server ? '[name].js' : '[name].[chunkhash].js',
    chunkFilename: debug ? '[name].js' : '[name].[chunkhash].js',
    publicPath,
    libraryTarget: server ? 'commonjs2' : void 0,
  },
  watch: debug && server ? true : void 0,
  target: server ? 'node' : 'web',

  performance: {
    hints: debug || server ? false : 'warning',
  },

  resolve: {
    extensions: ['.js', '.jsx'],
  },

  // Entry points list, allow to load a file with transforms
  module: { rules },
  stats,
  devServer: {
    host: assetsUrl.hostname,
    port: assetsUrl.port,
    proxy: [
      {
        context: ['/api'],
        target: apiUrl.href,
      },
      {
        context: ['/polyfill.js', '/favicon.ico'],
        target: serverUrl.href,
      },
      {
        context: ['/assets'],
        target: assetsUrl.href,
        pathRewrite: { '^/assets': '' },
      },
    ],
    publicPath: '/',
    disableHostCheck: true,
    compress: true,
    noInfo: !verbose,
    quiet: !verbose,
    hot: true,
    overlay: true,
    historyApiFallback: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    watchOptions: {
      ignored: /node_modules/,
    },
    stats,
  },
  // Webpack plugins
  plugins,
}

if (server) {
  // Options for node target
  conf.node = {
    __dirname: true,
  }
  conf.externals = [
    nodeExternals({
      modulesDir: dirs.modules,
      whitelist: [/\.css$/],
    }),
  ]
}

export default conf