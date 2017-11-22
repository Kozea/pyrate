import React from 'react'
import { hydrate, render } from 'react-dom'
import { Provider } from 'react-redux'
import RedBox from 'redbox-react'
import { createStore, combineReducers } from 'redux'
import { reducer as formReducer } from 'redux-form'

import App from './components/App'
import reducer from './components/reducer'
import { debug } from './config'

// On definit les reducers qui vont se charger de modifier l'état
const reducers = {
  // reducer est le reducer que l'on a définit pour la gestion des categories
  reducer,
  // provient de Redux-Form une lib spécialisée ds le traitement de formulaires
  form: formReducer,
}
// +sieurs reducers donc on "combine"
const reduc = combineReducers(reducers)
// store var conserver l'etat des objets ds l'app
export const store = createStore(reduc)

export const rootNode = document.getElementById('root')

export const renderRoot = handleError => {
  try {
    const renderMode = debug ? render : hydrate
    renderMode(
      <Provider store={store}>
        <App />
      </Provider>,
      rootNode
    )
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
