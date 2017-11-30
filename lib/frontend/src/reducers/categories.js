const categories = (state = [], action) => {
  switch (action.type) {
    case 'ADD_CATEGORY':
      return [
        ...state,
        {
          label: action.catLabel,
        },
      ]
    case 'EDIT_CATEGORY':
      return state.map(category => ({
        ...category,
        is_in_edition:
          category.id === action.categoryId
            ? !category.is_in_edition
            : category.is_in_edition,
      }))

    case 'LOAD_CATEGORIES_SUCCESS':
      return action.categories.data.categories.map(category => ({
        id: category.id,
        label: category.label,
        is_in_edition: false,
      }))
    case 'DEL_CATEGORY':
      return state.filter(category => category.id !== action.categoryId)
    case 'LOAD_CATEGORIES_ERROR':
      return state
    case 'UPDATE_CATEGORY':
      return state.map(category => ({
        ...category,
        label:
          category.id === action.categoryId ? action.catLabel : category.label,
        is_in_edition:
          category.id === action.categoryId
            ? !category.is_in_edition
            : category.is_in_edition,
      }))
    case 'DEL_ERROR':
    case 'UPD_ERROR':
    case 'ADD_ERROR':
      return action.message
    default:
      return state
  }
}

export default categories
