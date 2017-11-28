import { combineReducers } from 'redux'

import algorithmes from './algorithmes'
import categories from './categories'
import corpusTexts from './corpusTexts'
import generatedText from './generatedText'
import message from './message'
import user from './user'

const pyrateApp = combineReducers({
  algorithmes,
  categories,
  corpusTexts,
  generatedText,
  message,
  user,
})

export default pyrateApp
