import { combineReducers } from 'redux'

import algorithmes from './algorithmes'
import categories from './categories'
import texts from './texts'
import corpus from './corpus'

const pyrateApp = combineReducers({
  algorithmes,
  categories,
  texts,
  corpus,
})

export default pyrateApp
