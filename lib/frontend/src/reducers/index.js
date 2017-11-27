import { combineReducers } from 'redux'

import algorithmes from './algorithmes'
import categories from './categories'
import generatedText from './generatedText'
import texts from './texts'
import corpus from './corpus'
import isAuthenticated from './user'

const pyrateApp = combineReducers({
  algorithmes,
  categories,
  generatedText,
  texts,
  corpus,
  isAuthenticated
})

export default pyrateApp
