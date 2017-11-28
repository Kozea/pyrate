import { combineReducers } from 'redux'

import algorithmes from './algorithmes'
import categories from './categories'
import generatedText from './generatedText'
import texts from './texts'
import corpus from './corpus'
import user from './user'
import message from './message'

const pyrateApp = combineReducers({
  algorithmes,
  categories,
  generatedText,
  texts,
  corpus,
  user,
  message
})

export default pyrateApp
