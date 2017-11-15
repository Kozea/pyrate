import fs from 'fs'
import path from 'path'
import { PassThrough } from 'stream'
import { promisify } from 'util'

import fetch from 'isomorphic-fetch'
import Koaze from 'koaze'
import React from 'react'
import { renderToNodeStream } from 'react-dom/server'

import App from './components/App'
import {
  apiUrl,
  assetsUrl,
  debug,
  dirs,
  mockNginx,
  publicPath,
  serverUrl,
  verbose,
} from './config'

const koaze = new Koaze({
  debug,
  mockNginx,
  verbose,
  faviconPath: path.resolve(__dirname, 'favicon.png'),
  staticDirs: [],
  apiUrl,
  assetsUrl,
  assetsDir: dirs.assets,
})

const readIndex = async () => {
  if (debug) {
    const response = await fetch(
      `${assetsUrl.href.replace(/\/$/, '')}${publicPath}index.html`
    )
    return response.text()
  }
  return promisify(fs.readFile)(
    path.resolve(dirs.assets, 'index.html'),
    'utf-8'
  )
}

koaze.router.get('/*', async ctx => {
  const htmlStream = new PassThrough()
  const index = await readIndex()
  const [head, footer] = index.split('<!--REPLACEME-->')
  htmlStream.write(head)
  const stream = renderToNodeStream(<App />)
  stream.pipe(htmlStream, { end: false })
  stream.on('end', () => {
    htmlStream.write(footer)
    htmlStream.end()
  })
  ctx.type = 'text/html'
  ctx.body = htmlStream
})

koaze.serve(serverUrl, console.error.bind(console))
