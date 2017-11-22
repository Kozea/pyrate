import { List, Map } from 'immutable'

// on créé une liste factice de données
export const categories = List([
  Map({
    id: 1,
    catName: 'Rojin',
    isVisible: false,
    isUpdated: false,
  }),
  Map({
    id: 2,
    catName: 'Samira',
    isVisible: false,
    isUpdated: false,
  }),
])
