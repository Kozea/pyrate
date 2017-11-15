import React from 'react'
import { hydrate, render } from 'react-dom'
import RedBox from 'redbox-react'

import App from './components/App'

export const rootNode = document.getElementById('root')

export const renderRoot = handleError => {
  try {
    hydrate(<App />, rootNode)
  } catch (error) {
    handleError(error)
  }
}

/*
██████  ██████   ██████  ██████
██   ██ ██   ██ ██    ██ ██   ██
██████  ██████  ██    ██ ██   ██
██      ██   ██ ██    ██ ██   ██
██      ██   ██  ██████  ██████
*/

if (process.env.NODE_ENV === 'production') {
  // eslint-disable-next-line no-console
  console && console.log('PRODUCTION MODE')
  const handleError = console.error.bind(console)
  renderRoot(handleError)
}

/*
██████  ███████ ██████  ██    ██  ██████
██   ██ ██      ██   ██ ██    ██ ██
██   ██ █████   ██████  ██    ██ ██   ███
██   ██ ██      ██   ██ ██    ██ ██    ██
██████  ███████ ██████   ██████   ██████
*/

if (process.env.NODE_ENV === 'development') {
  // eslint-disable-next-line no-console
  console && console.log('DEVELOPMENT MODE')
  const handleError = error => render(<RedBox error={error} />, rootNode)

  renderRoot(handleError)

  if (module.hot) {
    module.hot.accept('./components/App', () => renderRoot(handleError))
    // module.hot.accept('../reducers', () => {
    //   store.replaceReducer(reducer)
    // })
  }
  window._debug = {
    // store, reducer,  history,
    rootNode,
  }
}
