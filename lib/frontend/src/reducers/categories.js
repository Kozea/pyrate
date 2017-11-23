const categories = (state = [], action) => {
  switch (action.type) {
    case 'ADD_CATEGORY':
      return [
        ...state,
        {
          id: action.id,
          label: action.label
        }
      ]
    case 'LOAD_CATEGORIES_SUCCESS':
      return action.categories.data.categories
    default:
      return state
  }
}

export default categories