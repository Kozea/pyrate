const categories = (state = [], action) => {
  switch (action.type) {
    case 'ADD_CATEGORY':
      return [
        ...state,
        {
          label: action.catLabel,
        },
      ]
    case 'LOAD_CATEGORIES_SUCCESS':
      return action.categories.data.categories
    case 'DEL_CATEGORY':
      return state.filter(category => category.id !== action.categoryId)
    case 'UPDATE_CATEGORY':
      return [
        ...state,
        {
          label: action.catLabel,
        },
      ]
    default:
      return state
  }
}

export default categories
