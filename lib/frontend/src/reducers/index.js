import { combineReducers } from 'redux'

import categories from './categories'
import texts from './texts'
import corpus from './corpus'

const pyrateApp = combineReducers({
  categories,
  texts,
  corpus,
})

export default pyrateApp
