// definir le type est obligatoire
// le store, c'est-à-dire que le store ne connait que
// les actions à appeler, pas comment elles doivent être prises en charge
const uid = () => new Date().valueOf()

export function addCat(item) {
  return {
    type: 'ADD_CAT',
    item: item,
    id: uid(),
  }
}

export function updateForm(item) {
  return {
    type: 'UPDATE_FORM',
    item: item,
    id: item.id,
  }
}

export const menu = menu => ({
  type: 'UPDATE_MENU',
  menu,
})
