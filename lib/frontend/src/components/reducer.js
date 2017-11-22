import Immutable, { Map } from 'immutable'

import { categories } from './fixtures'
import initial from './initial'

// contient les fonctions pures qui vont faire des actions pour produire un
// nouvel etat
export default function(state = categories, action) {
  switch (action.type) {
    // mise a jour des infos apres entrée ds formulaire
    case 'UPDATE_FORM':
      return state.map(item => {
        if (item.get('id') === action.id) {
          return Immutable.fromJS(action.item).set('isUpdated', true)
        }
        return item
      })
    case 'ADD_CAT':
      action.item.id = action.id
      return state.push(
        Map(action.item)
          .set('isVisible', false)
          .set('isUpdated', false)
      )
    default:
      return state
  }
}

const menu = (state = initial.menu, action) => {
  switch (action.type) {
    case 'UPDATE_MENU':
      return action.menu
    default:
      return state
  }
}
